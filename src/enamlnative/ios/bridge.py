"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 21, 2017

@author: jrm
"""
from atom.api import Atom, Int
from ..core import bridge
from ..core.bridge import (
    Command, msgpack_encoder,
    BridgeMethod, BridgeField, BridgeCallback, BridgeObject, NestedBridgeObject
)


class ObjcMethod(BridgeMethod):
    """ Description of a method of a View (or subclass) in Objc. When called, 
    this serializes the call, packs the arguments, and delegates handling to a 
    bridge in Objc.

    To keep method calling similar to Swift instead of defining a method 
    matching the signature with underscores like pyobjc and pyobjus the 
    signature should be defined as follows:

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
    def pack_args(self, obj, *args, **kwargs):
        """ Arguments must be packed according to the kwargs passed and
        the signature defined.

        """
        signature = self.__signature__
        #: No arguments expected
        if not signature:
            return (self.name, [])

        #: Build args, first is a string, subsequent are dictionaries
        method_name = [self.name]
        bridge_args = []
        for i, sig in enumerate(signature):
            if i == 0:
                method_name.append(":")
                bridge_args.append(msgpack_encoder(sig, args[0]))
                continue

            #: Sig is a dict so we must pull out the matching kwarg
            found = False
            for k in sig:
                if k in kwargs:
                    method_name.append("{}:".format(k))
                    bridge_args.append(msgpack_encoder(sig[k], kwargs[k]))
                    found = True
                    break
            if not found:
                #: If we get here something is wrong
                raise ValueError("Unexpected or missing argument at index {}. "
                                 "Expected {}".format(i, sig))

        return ("".join(method_name), bridge_args)


class ObjcProperty(BridgeField):
    """ The superclass implementation is sufficient

    """


class ObjcCallback(BridgeCallback, ObjcMethod):
    """ Description of a callback method of a View (or subclass) in Objc. 
    When called, it fires the connected callback. This is triggered when it 
    receives an event from the bridge indicating the call has occured.
    
    """
    def pack_args(self, obj, *args, **kwargs):
        return ObjcMethod.pack_args(self, obj, *args, **kwargs)


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

    def __init__(self, *args, **kwargs):
        """ Sends the event to create this View in Java """
        __id__ = kwargs.get('__id__', None)

        #: Note: We SKIP the superclass here!
        if __id__ is not None:
            super(Atom, self).__init__(__id__=__id__)
        else:
            super(Atom, self).__init__()

        #: Send the event over the bridge to construct the view
        bridge.CACHE[self.__id__] = self
        if __id__ is None:
            self.__app__.send_event(
                Command.CREATE,  #: method
                self.__id__,  #: id to assign in bridge cache
                self.__nativeclass__,
                *self._pack_args(**kwargs)
            )

    def _pack_args(self, *args, **kwargs):
        """ Arguments must be packed according to the kwargs passed and
        the signature defined.

        """
        signature = self.__signature__
        #: No arguments expected
        if not signature or not kwargs:
            return ("init", [])

        #: Build args, first is a string, subsequent are dictionaries
        method_name = []
        bridge_args = []
        for i, sig in enumerate(signature):
            #if i == 0:
            #    method_name.append(":")
            #    bridge_args.append(msgpack_encoder(sig, args[0]))
            #    continue

            #: Sig is a dict so we must pull out the matching kwarg
            found = False
            for k in sig:
                if k in kwargs:
                    method_name.append("{}:".format(k))
                    bridge_args.append(msgpack_encoder(sig[k], kwargs[k]))
                    found = True
                    break
            if not found:
                #: If we get here something is wrong
                raise ValueError("Unexpected or missing argument at index {}. "
                                 "Expected {}".format(i, sig))

        return ("".join(method_name), bridge_args)
