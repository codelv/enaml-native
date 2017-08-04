'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 21, 2017

@author: jrm
'''
import functools
from contextlib import contextmanager
from atom.api import Property, Int, set_default
from ..core.bridge import Command, msgpack_encoder, BridgeObject


class ObjcMethod(Property):
    """ Description of a method of a View (or subclass) in Objc. When called, this
        serializes the call, packs the arguments, and delegates handling to a bridge in Objc.

        To keep method calling similar to Swift instead of defining a method matching the
        signature with underscores like pyobjc and pyobjus the signature should be
        defined as follows:

        1. The first argument, if any, should be a string.
        2. Subsequent arguments should each be a dictionary of the available
           `subnames` and their types.

        For instance:

            UIView `insertSubview` has the following signatures:

                - (void)insertSubview:(UIView *)view
                        atIndex:(NSInteger)index;

                - (void)insertSubview:(UIView *)view
                        aboveSubview:(UIView *)siblingSubview;

                - (void)insertSubview:(UIView *)view
                        belowSubview:(UIView *)siblingSubview;

            This is defined in python like:

                insertSubview = ObjcMethod('UIView',
                                            dict(atIndex='NSInteger',
                                                 aboveSubview='UIView',
                                                 belowSubview='UIView'))

            Doing it this way it can be called like Swift, using kwargs

                view.insertSubview(subview, atIndex=3)
                view.insertSubview(subview, aboveSubview=above_view)




    """
    __slots__ = ('__signature__', '__returns__', '__cache__')

    def __init__(self, *args, **kwargs):
        self.__returns__ = kwargs.get('returns', None)
        self.__signature__ = args
        self.__cache__ = {}  # Result cache otherwise gc cleans up
        super(ObjcMethod, self).__init__(self.__fget__)

    @contextmanager
    def suppressed(self, obj):
        """ Suppress calls within this context to avoid feedback loops"""
        obj.__suppressed__[self.name] = True
        yield
        obj.__suppressed__[self.name] = False

    def __fget__(self, obj):
        f = functools.partial(self.__call__, obj)
        f.suppressed = functools.partial(self.suppressed, obj)
        return f

    def __call__(self, obj, *args, **kwargs):
        """ The Swift like syntax is used"""
        if obj.__suppressed__.get(self.name):
            return

        signature = self.__signature__

        #vargs = signature and signature[-1].endswith("...")
        #if not vargs and (len(args) != len(signature)):
        #    raise ValueError("Invalid number of arguments: Given {}, expected {}"
        #                     .format(args, signature))
        #if vargs:
        #    varg = signature[-1].replace('...', '')
        #    bridge_args = [
        #        msgpack_encoder(signature[i] if i+1 < len(signature) else varg, args[i])
        #        for i in range(len(args))
        #        ]
        #else:
        bridge_args = [msgpack_encoder(sig, arg) for sig, arg in zip(signature, args)]

        result = obj.__app__.create_future() if self.__returns__ else None

        if result:
            #: Store in local cache or global cache (weakref) removes it
            #: resulting in a Reference error when the result is returned
            self.__cache__[result.__id__] = result

            def resolve(r, f=result):
                #: Remove from local cache to free future
                del self.__cache__[f.__id__]

            #: Delete from the local cache once resolved.
            result.then(resolve)

        obj.__app__.send_event(
            Command.METHOD,  #: method
            obj.__id__,
            result.__id__ if result else 0,
            self.name,  #: method name
            bridge_args, #: args
            **kwargs #: kwargs to send_event
        )
        return result


class ObjcProperty(Property):
    __slots__ = ('__signature__',)

    def __init__(self, arg):
        self.__signature__ = arg
        super(ObjcProperty, self).__init__(self.__fget__, self.__fset__)

    def __fset__(self, obj, arg):
        obj.__app__.send_event(
            Command.FIELD,  #: method
            obj.__id__,
            self.name,  #: method name
            [msgpack_encoder(self.__signature__, arg)]  #: args
        )

    def __fget__(self, obj):
        raise NotImplementedError("Reading attributes is not yet supported")


class ObjcCallback(ObjcMethod):
    """ Description of a callback method of a View (or subclass) in Objc. When called,
        it fires the connected callback. This is triggered when it receives an event from
        the bridge indicating the call has occured.
    """

    def __fget__(self, obj):
        f = super(ObjcCallback, self).__fget__(obj)
        #: Add a method so it can be connected like in Qt
        f.connect = functools.partial(self.connect, obj)
        return f

    def __call__(self, obj, *args):
        """ Fire the callback if one is connected """
        if obj.__suppressed__.get(self.name):
            return
        callback = obj.__callbacks__.get(self.name)
        if callback:
            return callback(*args)

    def connect(self, obj, callback):
        """ Set the callback to be fired when the event occurs. """
        obj.__callbacks__[self.name] = callback


class ObjcBridgeObject(BridgeObject):
    """ A proxy to a class in java. This sends the commands over
        the bridge for execution.  The object is stored in a map
        with the given id and is valid until this object is deleted.
    Parameters
    ----------
    __id__: Int
        If an __id__ keyward argument is passed during creation,
        this will assume the object was already created and
        only a reference to the object with the given id is needed.

    """
    def _default___nativeclass__(self):
        """ Use the class name by default as everything should be unique. """
        return self.__class__.__name__

