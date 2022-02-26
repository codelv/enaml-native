"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on June 21, 2017

@author: jrm
"""
from typing import Optional
from atom.api import Atom
from enamlnative.core.bridge import (
    BridgeCallback,
    BridgeField,
    BridgeMethod,
    BridgeObject,
    BridgeStaticMethod,
    Command,
    CACHE,
    msgpack_encoder,
)


def encode_args(method: BridgeMethod, args: tuple, encoder=msgpack_encoder):
    """Common function for packing method arguments."""
    signature = method.__signature__
    name = method.name.rstrip("_")
    if not signature:
        return (name, [])  # No arguments
    if signature[-1].endswith("..."):
        nargs = len(args)
        nparams = len(signature)
        if nargs > nparams:
            msg = f"Invalid number of arguments: Got {args}, expected {signature}"
            raise ValueError(msg)
        varg = signature[-1][0:-3]
        end = nparams - 1
        return (
            name,
            [encoder(signature[i] if i < end else varg, args[i]) for i in range(nargs)],
        )
    return (name, [encoder(sig, arg) for sig, arg in zip(signature, args)])


class JavaMethod(BridgeMethod):
    """Description of a method of a View (or subclass) in Java. When called,
    this serializes call, packs the arguments, and delegates handling to a
    bridge in Java.

    """

    def pack_args(self, obj: BridgeObject, *args, **kwargs):
        # The obj param is handled by the superclass
        return encode_args(self, args)


class JavaStaticMethod(BridgeStaticMethod):
    def pack_args(self, *args, **kwargs):
        return encode_args(self, args)


class JavaField(BridgeField):
    """The superclass implementation is sufficient but extend for possible
    future modification.

    """


class JavaCallback(BridgeCallback, JavaMethod):
    """Description of a callback method of a View (or subclass) in Java.
    When called, it fires the connected callback. This is triggered when
    it receives an event from the bridge indicating the call has occured.

    """

    def pack_args(self, obj: BridgeObject, *args, **kwargs):
        return encode_args(self, args)


class JavaBridgeObject(BridgeObject):
    """A proxy to a class in java. This sends the commands over
    the bridge for execution.  The object is stored in a map
    with the given id and is valid until this object is deleted.

    Parameters
    ----------
    __id__: Int
        If an __id__ keyward argument is passed during creation,
        this will assume the object was already created and
        only a reference to the object with the given id is needed.

    """

    #: Java Class name
    __nativeclass__ = "java.lang.Object"

    #: A callback with an implementation built in
    hashCode = JavaCallback(returns=int)
    toString = JavaCallback(returns=str)
    equals = JavaCallback(returns=bool)

    def _impl_hashCode(self):
        #: Add a default callback for hashCode
        return self.__id__

    def _impl_toString(self):
        #: Add a default callback for toString
        return f"{self}"

    def _impl_equals(self, other):
        #: Add a default callback for toString
        return other == self.__id__


class JavaProxy(JavaBridgeObject):
    """A bridge object that creates a Proxy for the given ref. This should NOT
    be given any JavaMethods or JavaFields, however JavaCallbacks are fine.

    These are generally throw away usages. Only save them if you need to
    use them as a reference later (such as when removing a listener).

    Parameters
    -------------

    ref: JavaBridgeObject
        The bridge object that should receive all of the callbacks
        invocations. If none is given it will send them to the proxy
        itself.


    """

    def __init__(self, ref: Optional[BridgeObject] = None, **kwargs):
        """Sends the event to create this View in Java"""
        # Skip the subclass
        super(Atom, self).__init__(**kwargs)

        # Send the event over the bridge to construct the view
        __id__ = kwargs.get("__id__", None)
        CACHE[self.__id__] = self
        if __id__ is None:
            ref = ref or self
            app = self.__app__
            assert app is not None
            app.send_event(
                Command.PROXY,  #: method
                self.__id__,  #: id to assign in bridge cache
                self.__nativeclass__,
                ref.__id__,  #: Reference ID
            )
