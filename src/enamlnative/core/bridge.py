'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 21, 2017

@author: jrm
'''
import msgpack
import functools
from atom.api import Atom, Property, ForwardInstance, Dict, Unicode, Tuple, Int
from weakref import WeakValueDictionary
from contextlib import contextmanager

CACHE = WeakValueDictionary()
__global_id__ = 0


class Command:
    CREATE = "c"
    METHOD = "m"
    FIELD = "f"
    DELETE = "d"
    RESULT = "r"
    ERROR = "e"


class ExtType:
    REF = 1


def _generate_id():
    """ Generate an id for an object """
    global __global_id__
    __global_id__ += 1
    return __global_id__


def tag_object_with_id(obj):
    """ Generate and assign a id for the object"""
    obj.__id__ = _generate_id()
    CACHE[obj.__id__] = obj


def _cleanup_id(obj):
    """ Removes the object from the """
    try:
        del CACHE[obj.__id__]
    except KeyError:
        pass


def get_app_class():
    """ Avoid circular import. Probably indicates a
        poor design...
    """
    from .app import BridgedApplication
    return BridgedApplication


def encode(obj):
    """ Encode an object for proper decoding by Java or ObjC
    """
    if hasattr(obj, '__nativeclass__'):
        return msgpack.ExtType(ExtType.REF, msgpack.packb(obj.__id__))
    return obj


def msgpack_encoder(sig, obj):
    """ When passing a BridgeObject encode it in a special way so
        it can properly be interpreted as a reference.

        TODO: This should use the object hooks for doing this automatically
    """
    #if isinstance(obj, (list, tuple)):
    #    return sig, [encode(o) for o in obj]
    return sig, encode(obj)


def dumps(data):
    """ Encodes events for sending over the bridge """
    return msgpack.dumps(data)


def loads(data):
    """ Decodes and processes events received from the bridge """
    if not data:
        raise ValueError("Tried to load empty data!")
    return msgpack.loads(data)


class BridgeReferenceError(ReferenceError):
    pass


def get_handler(ptr, method):
    """ Dereference the pointer and return the handler method. """
    obj = CACHE.get(ptr, None)
    if obj is None:
        raise BridgeReferenceError("Reference id={} never existed or has already been destroyed"
                       .format(ptr))
    elif not hasattr(obj, method):
        raise NotImplementedError("{}.{} is not implemented.".format(obj, method))
    return obj, getattr(obj, method)


class BridgeMethod(Property):
    """ A method that is callable via the bridge.
        When called, this serializes the call, packs the arguments,
            and delegates handling to a bridge in native code.

        Example:
            #: Define it
            class View(BridgeObject):
                addView = BridgeMethod('android.view.View')

            #: Create instance
            view = View()
            view2 = View()

            #: Use it
            view.addView(view2)

    """
    __slots__ = ('__signature__', '__returns__', '__cache__')

    def __init__(self, *args, **kwargs):
        self.__returns__ = kwargs.get('returns', None)
        self.__signature__ = args
        self.__cache__ = {}  # Result cache otherwise gc cleans up
        super(BridgeMethod, self).__init__(self.__fget__)

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

        #: Format the args as needed
        method_name, method_args = self.pack_args(obj, *args, **kwargs)

        #: Create a future to retrieve the result if needed
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
            method_name,  #: method name
            method_args,  #: args
            **kwargs  #: kwargs to send_event
        )
        return result

    def pack_args(self, obj, *args, **kwargs):
        """ Subclasses should implement this to pack args as needed
            for the native bridge implementation. Must return a tuple containing
            ("methodName", [list, of, encoded, args])
        """
        raise NotImplementedError


class BridgeField(Property):
    """ Allows you to set fields or properties over the bridge using normal python syntax.

        Example:
            #: Define it
            class View(BridgeObject):
                width = BridgeField('int')

            #: Create instance
            view = View()

            #: Set field
            view.width = 200

    """
    __slots__ = ('__signature__',)

    def __init__(self, arg):
        self.__signature__ = arg
        super(BridgeField, self).__init__(self.__fget__, self.__fset__)

    def __fset__(self, obj, arg):
        obj.__app__.send_event(
            Command.FIELD,  #: method
            obj.__id__,
            self.name,  #: method name
            [msgpack_encoder(self.__signature__, arg)]  #: args
        )

    def __fget__(self, obj):
        raise NotImplementedError("Reading attributes is not yet supported")


class BridgeCallback(BridgeMethod):
    """ Description of a callback method of a View (or subclass) in Objc. When called,
        it fires the connected callback. This is triggered when it receives an event from
        the bridge indicating the call has occurred.

        Example:
            #: Define it
            class View(BridgeObject):
                onClick = BridgeCallback()

            #: Create instance
            view = View()

            def on_click():
                print("Clicked!")

            #: Connect to callback
            view.onClick.connect(on_click)
    """

    def __fget__(self, obj):
        f = super(BridgeCallback, self).__fget__(obj)
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


class BridgeObject(Atom):
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
    __slots__ = ('__weakref__',)

    #: Native Class name
    __nativeclass__ = Unicode()

    #: Constructor signature
    __signature__ = Tuple()

    #: Suppressed methods / fields
    __suppressed__ = Dict()

    #: Callbacks
    __callbacks__ = Dict()

    #: Bridge object ID
    __id__ = Int(0, factory=_generate_id)

    #: Bridge
    __app__ = ForwardInstance(get_app_class)

    def _default___app__(self):
        return get_app_class().instance()

    def getId(self):
        return self.__id__

    def __init__(self, *args, **kwargs):
        """ Sends the event to create this View in Java """
        super(BridgeObject, self).__init__(**kwargs)

        #: Send the event over the bridge to construct the view
        __id__ = kwargs.get('__id__', None)
        CACHE[self.__id__] = self
        if __id__ is None:
            self.__app__.send_event(
                Command.CREATE,  #: method
                self.__id__,  #: id to assign in bridge cache
                self.__nativeclass__,
                [msgpack_encoder(sig, arg) for sig, arg in zip(self.__signature__, args)],
            )

    def __del__(self):
        """ Destroy this object and send a command to destroy the actual object
            reference the bridge implementation holds (allowing it to be released).
        """
        self.__app__.send_event(
            Command.DELETE,  #: method
            self.__id__,  #: id to assign in java
        )
        _cleanup_id(self)
