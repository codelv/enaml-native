"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on June 21, 2017
"""
import functools
import msgpack
from asyncio import Future
from contextlib import contextmanager
from typing import Any, ClassVar, Optional, Union, Type
from weakref import WeakValueDictionary
from types import GenericAlias
from atom.api import Atom, Dict, ForwardInstance, Instance, Int, Property, Str

CACHE: WeakValueDictionary[int, Union[Future, "BridgeObject"]] = WeakValueDictionary()
__global_id__: int = 0
__method_id__: int = 0


#: Mapping of nativeclass str to subclasses
REGISTRY: dict[str, "BridgeObject"] = {}


class Command:
    CREATE = "c"
    PROXY = "p"
    METHOD = "m"
    STATIC_METHOD = "sm"
    FIELD = "f"
    DELETE = "d"
    RESULT = "r"
    ERROR = "e"
    DEF = "def"


class ExtType:
    REF = 1
    PROXY = 2


def generate_id() -> int:
    """Generate an id for an object"""
    global __global_id__
    __global_id__ += 1
    return __global_id__


def method_id():
    global __method_id__
    __method_id__ += 1
    return __method_id__


def convert_arg(arg: Any) -> Optional[str]:
    """Convert an argument to a string"""
    if isinstance(arg, str):
        return arg
    if hasattr(arg, "__nativeclass__"):
        return arg.__nativeclass__
    if arg is None:
        return None
    if isinstance(arg, GenericAlias):
        return str(arg)  # eg list[int]
    if isinstance(arg, dict):
        args = tuple(arg.values())
        assert len(args) == 1
        return convert_arg(args[0])
    assert hasattr(arg, "__name__"), "Signature argument must be a type or str"
    return arg.__name__


def tag_object_with_id(obj):
    """Generate and assign a id for the object"""
    obj_id = obj.__id__ = generate_id()
    CACHE[obj_id] = obj
    return obj


def get_object_with_id(id):
    """Get the object with the given id in the cache"""
    return CACHE[id]


def _cleanup_id(obj):
    """Removes the object from the"""
    try:
        del CACHE[obj.__id__]
    except KeyError:
        pass


def get_app_class():
    """Avoid circular import. Probably indicates a
    poor design...
    """
    from .app import BridgedApplication

    return BridgedApplication


def encode(obj):
    """Encode an object for proper decoding by Java or ObjC"""
    if hasattr(obj, "__id__"):
        return msgpack.ExtType(ExtType.REF, msgpack.packb(obj.__id__))
    return obj


def msgpack_encoder(sig, obj):
    """When passing a BridgeObject encode it in a special way so
    it can properly be interpreted as a reference.

    TODO: This should use the object hooks for doing this automatically
    """
    # if isinstance(obj, (list, tuple)):
    #    return sig, [encode(o) for o in obj]
    return sig, encode(obj)


def dumps(data):
    """Encodes events for sending over the bridge"""
    return msgpack.dumps(data)


def loads(data):
    """Decodes and processes events received from the bridge"""
    # if not data:
    #    raise ValueError("Tried to load empty data!")
    return msgpack.loads(data, use_list=False, raw=False)


class BridgeReferenceError(ReferenceError):
    """This exception occurs when an event comes in from the bridge and
    python does not have any reference in the cache.

    """

    pass


class BridgeException(Exception):
    """This exception occurs when a remote method call fails."""

    pass


def get_handler(ptr: int, method: str) -> tuple:
    """Dereference the pointer and return the handler method."""
    obj = CACHE.get(ptr, None)
    if obj is None:
        msg = f"Reference id={ptr} never existed or has already been destroyed"
        raise BridgeReferenceError(msg)
    handler = getattr(obj, method, None)
    if handler is None:
        raise NotImplementedError(f"{obj}.{method} is not implemented.")
    return obj, handler


class BridgeObject(Atom):
    """A proxy to a class in java. This sends the commands over
    the bridge for execution.  The object is stored in a map
    with the given id and is valid until this object is deleted.

    Parameters
    ----------
    __id__: Int, Future, or None
        If an __id__ keyword argument is passed during creation, then

            If the __id__ is an int, this will assume the object was already
            created and only a reference to the object with the given id is
            needed.

            If the __id__ is a Future (as specified by the app event loop),
            then the __id__ of he future will be used. When the future
            completes this object will then be put into the cache. This allows
            passing results directly instead of using the `.then()` method.

    """

    __slots__ = ("__weakref__", "__constructor_ids__")

    #: Native Class name
    __nativeclass__: ClassVar[str] = ""

    #: Constructor signature
    __signature__: ClassVar[list[Union[dict, str, "BridgeObject", type]]] = []

    #: Constructor cache id
    __constructor_ids__: ClassVar[list[int]]

    #: Suppressed methods / fields
    __suppressed__ = Dict()

    #: Callbacks
    __callbacks__ = Dict()

    #: Bridge object ID
    __id__ = Int(0, factory=generate_id)

    #: Prefix to add to all names used during method and property calls
    #: used for nested objects
    __prefix__ = Str()

    #: Bridge
    __app__ = ForwardInstance(get_app_class)

    @classmethod
    def __init_subclass__(cls, *args, **kwargs):
        #: Convert signature to string
        cls.__signature__ = [convert_arg(arg) for arg in cls.__signature__]
        # Create a method id for each signature length as some may be
        # optional. TODO: Rethink this...
        n = max(1, len(cls.__signature__))
        cls.__constructor_ids__ = [method_id() for i in range(n)]
        REGISTRY[cls.__nativeclass__] = cls

    def _default___app__(self):
        return get_app_class().instance()

    def getId(self):
        return self.__id__

    def __init__(self, *args, **kwargs):
        """Sends the event to create this object in Java."""

        #: Send the event over the bridge to construct the view
        __id__ = kwargs.pop("__id__", None)
        cache = True
        if __id__ is not None:
            if isinstance(__id__, int):
                kwargs["__id__"] = __id__
            elif isinstance(__id__, Future):
                #: If a future is given don't store this object in the cache
                #: until after the future completes
                f = __id__

                def set_result(f):
                    CACHE[f.__id__] = self

                f.add_done_callback(set_result)

                #: The future is used to return the result
                kwargs["__id__"] = f.__id__

                #: Save it into the cache when the result from the future
                #: arrives over the bridge.
                cache = False
            else:
                raise TypeError(
                    "Invalid __id__ reference, expected an int or"
                    f"a future/deferred object, got: {__id__}"
                )

        #: Construct the object
        super().__init__(**kwargs)

        if cache:
            CACHE[self.__id__] = self

        if __id__ is None:
            if args:
                constructor_id = self.__constructor_ids__[len(args) - 1]
            else:
                constructor_id = self.__constructor_ids__[0]
            self.__app__.send_event(
                Command.CREATE,  #: method
                self.__id__,  #: id to assign in bridge cache
                constructor_id,
                self.__nativeclass__,
                [
                    msgpack_encoder(sig, arg)
                    for sig, arg in zip(self.__signature__, args)
                ],
            )

    def __del__(self):
        """Destroy this object and send a command to destroy the actual object
        reference the bridge implementation holds (allowing it to be released).
        """
        ref = self.__id__
        self.__app__.send_event(Command.DELETE, ref)
        try:
            del CACHE[ref]
        except KeyError:
            pass


class NestedBridgeObject(BridgeObject):
    """A nested object allows you to invoke methods and set properties
    of an object that is a property of another object using the dot notation.

    Useful for setting nested properties without needing to first create a
    reference bridge object (thus saving the time waiting for the bridge to
    reply) for example:

        UIView view = [UIView new];
                view.yoga.width = YES;

    Would require to create a reference to the "yoga" object first but instead
    we just add our nested object's prefix and let the bridge resolve the
    actual property. It works like a regular BridgeObject but appends the
    "name'.

    This object is NOT in the cache on either side of the bridge.

    """

    #: Reference to the object this is referenced under
    __root__ = Instance(BridgeObject)

    def __init__(self, root, attr, **kwargs):
        kwargs["__id__"] = root.getId()
        kwargs["__prefix__"] = f"{attr}."
        Atom.__init__(self, **kwargs)

    def __del__(self):
        # Not necessary, it's not in the cache
        pass


class BridgeMethod(Property):
    """A method that is callable via the bridge.
    When called, this serializes the call, packs the arguments,
    and delegates handling to a bridge in native code.

    #: Define it
    class View(BridgeObject):
        addView = BridgeMethod('android.view.View')

    #: Create instance
    view = View()
    view2 = View()

    #: Use it
    view.addView(view2)

    """

    __slots__ = ("__signature__", "__returns__", "__cache__", "__method_id__")
    __returns__: Optional[tuple[str, type]]
    __signature__: tuple[str, ...]
    __cache__: dict[int, Future]
    __method_id__: int

    def __init__(self, *args, **kwargs):
        return_type = kwargs.get("returns", None)
        if return_type is None:
            self.__returns__ = None
        else:
            self.__returns__ = (convert_arg(return_type), return_type)
        self.__signature__ = tuple(convert_arg(arg) for arg in args)
        self.__cache__ = {}  # Result cache otherwise gc cleans up
        self.__method_id__ = method_id()
        super().__init__(self.__fget__)

    @contextmanager
    def suppressed(self, obj: BridgeObject):
        """Suppress calls within this context to avoid feedback loops"""
        obj.__suppressed__[self.name] = True
        yield
        obj.__suppressed__[self.name] = False

    def __fget__(self, obj):
        f = functools.partial(self.__call__, obj)
        f.suppressed = functools.partial(self.suppressed, obj)
        return f

    def __call__(self, obj, *args, **kwargs):
        """The Swift like syntax is used"""
        if obj.__suppressed__.get(self.name):
            return

        #: Format the args as needed
        method_name, method_args = self.pack_args(obj, *args, **kwargs)

        #: Create a future to retrieve the result if needed
        app = obj.__app__
        if self.__returns__:
            result = app.create_future(self.__returns__[1])
            #: Store in local cache or global cache (weakref) removes it
            #: resulting in a Reference error when the result is returned
            result_id = result.__id__
            self.__cache__[result_id] = result

            def cleanup(r):
                #: Remove from local cache to free future
                del self.__cache__[result_id]

            #: Delete from the local cache once resolved.
            result.add_done_callback(cleanup)
        else:
            result = None
            result_id = 0

        app.send_event(
            Command.METHOD,  #: method
            obj.__id__,
            result_id,
            self.__method_id__,
            f"{obj.__prefix__}{method_name}",  #: method name
            method_args,  #: args
            **kwargs,  #: kwargs to send_event
        )
        return result

    def pack_args(self, obj, *args, **kwargs):
        """Subclasses should implement this to pack args as needed
        for the native bridge implementation. Must return a tuple containing
        ("methodName", [list, of, encoded, args])

        """
        raise NotImplementedError


class BridgeStaticMethod(Property):
    """A method that is callable via the bridge.
    When called, this serializes the call, packs the arguments,
    and delegates handling to a bridge in native code.

    #: Define it
    class Toast(BridgeObject):
        makeToast = BridgeStaticMethod(*args)

    #: Use
    result = Toast.makeToast(*args)

    """

    __slots__ = (
        "__signature__",
        "__returns__",
        "__cache__",
        "__owner__",
        "__method_id__",
    )
    #: Return type
    __returns__: Optional[tuple[str, type]]

    #: Function signature
    __signature__: tuple[str, ...]

    #: Cache for results
    __cache__: dict[int, Future]
    __owner__: Optional[Type[BridgeObject]]
    __method_id__: int

    def __init__(self, *args, **kwargs):
        return_type = kwargs.get("returns", None)
        if return_type is None:
            self.__returns__ = None
        else:
            self.__returns__ = (convert_arg(return_type), return_type)
        self.__signature__ = tuple(convert_arg(arg) for arg in args)
        self.__owner__ = None
        self.__cache__ = {}  # Result cache otherwise gc cleans up
        self.__method_id__ = method_id()
        super().__init__()

    def __get__(self, instance, owner):
        #: Save the object this class referencesf
        if self.__owner__ is None:
            self.__owner__ = owner
        return super().__get__(instance, owner)

    def __call__(self, *args, **kwargs):
        #: Format the args as needed
        method_name, method_args = self.pack_args(*args, **kwargs)

        app = get_app_class().instance()

        #: Create a future to retrieve the result if needed
        if self.__returns__:
            result = app.create_future(self.__returns__[1])
            result_id = result.__id__
            #: Store in local cache or global cache (weakref) removes it
            #: resulting in a Reference error when the result is returned
            self.__cache__[result_id] = result

            def cleanup(r):
                #: Remove from local cache to free future
                del self.__cache__[result_id]

            #: Delete from the local cache once resolved.
            result.add_done_callback(cleanup)
        else:
            result = None
            result_id = 0

        app.send_event(
            Command.STATIC_METHOD,  #: method
            self.__owner__.__nativeclass__,
            result_id,
            self.__method_id__,  # Function cache
            method_name,  #: method name
            method_args,  #: args
            **kwargs,  #: kwargs to send_event
        )
        return result

    def pack_args(self, obj, *args, **kwargs):
        """Subclasses should implement this to pack args as needed
        for the native bridge implementation. Must return a tuple containing
        ("methodName", [list, of, encoded, args])

        """
        raise NotImplementedError


class BridgeField(Property):
    """Allows you to set fields or properties over the bridge using normal
    python syntax.

    #: Define it
    class View(BridgeObject):
        width = BridgeField('int')

    #: Create instance
    view = View()

    #: Set field
    view.width = 200

    """

    __slots__ = ("__signature__", "__method_id__")
    #: Field type
    __signature__: str
    __method_id__: int

    def __init__(self, arg):
        self.__signature__ = convert_arg(arg)
        self.__method_id__ = method_id()
        super().__init__(self.__fget__, self.__fset__)

    @contextmanager
    def suppressed(self, obj):
        """Suppress calls within this context to avoid feedback loops"""
        obj.__suppressed__[self.name] = True
        yield
        obj.__suppressed__[self.name] = False

    def __fset__(self, obj, arg):
        if obj.__suppressed__.get(self.name):
            return
        obj.__app__.send_event(
            Command.FIELD,  #: method
            obj.__id__,
            self.__method_id__,
            f"{obj.__prefix__}{self.name}",  #: method name
            [msgpack_encoder(self.__signature__, arg)],  #: args
        )

    def __fget__(self, obj):
        """Return an object that can be used to retrieve the value."""
        raise NotImplementedError("Reading attributes is not yet supported")


class BridgeCallback(BridgeMethod):
    """Description of a callback method of a View (or subclass) in
    Objc or Java. When called,it fires the connected callback. If no callback
    is connected it will try to lookup a default callback implementation
    matching the name `_impl_<name>`. If that does not exist, it will simply
    do nothing.

    This is triggered when it receives an event from the bridge indicating the
    call has occurred.


        #: Define it
        class View(BridgeObject):
            onClick = BridgeCallback()

        #: Create instance
        view = View()

        def on_click():
            print("Clicked!")

        #: Connect to callback
        view.onClick.connect(on_click)


    You can define a "default" callback implementation by implementing the
    method with name of `_impl_<name>`. Connecting a callback will override
    this behavior.

    #: Define it
    class LocationManager(BridgeObject):
        hashCode = BridgeCallback()

        def _impl_hashCode(self):
            return self.__id__

    """

    def __fget__(self, obj):
        f = super().__fget__(obj)
        #: Add a method so it can be connected like in Qt
        f.connect = functools.partial(self.connect, obj)
        f.disconnect = functools.partial(self.disconnect, obj)
        return f

    def __call__(self, obj, *args):
        """Fire the callback if one is connected"""
        if obj.__suppressed__.get(self.name):
            return
        callback = obj.__callbacks__.get(self.name)
        if not callback:
            #: Try to get the default callback
            callback = getattr(obj, f"_impl_{self.name}", None)

        if callback:
            return callback(*args)

    def connect(self, obj, callback):
        """Set the callback to be fired when the event occurs."""
        obj.__callbacks__[self.name] = callback

    def disconnect(self, obj, callback=None):
        """Remove the callback to be fired when the event occurs."""
        del obj.__callbacks__[self.name]


class BridgeFuture(Future):
    """A future which automatically resolves to the return type"""

    __id__: int
    __returns__: Optional[type]

    def __init__(self, return_type: Optional[type] = None):
        result_id = self.__id__ = generate_id()
        CACHE[result_id] = self
        self.__returns__ = return_type
        super().__init__()

    def set_result(self, result):
        return_type = self.__returns__
        if (
            isinstance(result, int)
            and isinstance(return_type, type)
            and issubclass(return_type, BridgeObject)
        ):
            result = return_type(__id__=result)
        super().set_result(result)
