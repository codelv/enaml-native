"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 21, 2017

@author: jrm
"""
from atom.api import Atom, Int, set_default
from ..core import bridge
from ..core.bridge import (
    Command, msgpack_encoder, BridgeMethod, BridgeStaticMethod,
    BridgeField, BridgeCallback, BridgeObject, encode
)


class JavaMethod(BridgeMethod):
    """ Description of a method of a View (or subclass) in Java. When called, 
    this serializes call, packs the arguments, and delegates handling to a 
    bridge in Java.
    
    """

    def pack_args(self, obj, *args, **kwargs):
        signature = self.__signature__

        vargs = signature and signature[-1].endswith("...")
        if not vargs and (len(args) != len(signature)):
            raise ValueError(
                "Invalid number of arguments: Given {}, expected {}"
                .format(args, signature))
        if vargs:
            varg = signature[-1].replace('...', '')
            return (self.name, [
                msgpack_encoder(
                    signature[i] if i+1 < len(signature) else varg, args[i])
                for i in range(len(args))
            ])

        return (self.name, [msgpack_encoder(sig, arg)
                            for sig, arg in zip(signature, args)])


class JavaStaticMethod(BridgeStaticMethod):

    def pack_args(self, *args, **kwargs):
        signature = self.__signature__

        vargs = signature and signature[-1].endswith("...")
        if not vargs and (len(args) != len(signature)):
            raise ValueError(
                "Invalid number of arguments: Given {}, expected {}"
                .format(args, signature))
        if vargs:
            varg = signature[-1].replace('...', '')
            return (self.name, [
                msgpack_encoder(signature[i]
                                if i+1 < len(signature) else varg, args[i])
                for i in range(len(args))
                ])

        return (self.name, [msgpack_encoder(sig, arg)
                            for sig, arg in zip(signature, args)])


class JavaField(BridgeField):
    """ The superclass implementation is sufficient but extend for possible 
    future modification.

    """


class JavaCallback(BridgeCallback, JavaMethod):
    """ Description of a callback method of a View (or subclass) in Java. 
    When called, it fires the connected callback. This is triggered when 
    it receives an event from the bridge indicating the call has occured.
    
    """
    def pack_args(self, obj, *args, **kwargs):
        return JavaMethod.pack_args(self, obj, *args, **kwargs)


class JavaBridgeObject(BridgeObject):
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
    #: Java Class name
    __nativeclass__ = set_default('java.lang.Object')

    #: A callback with an implementation built in
    hashCode = JavaCallback(returns="int")

    def _impl_hashCode(self):
        #: Add a default callback for hashCode
        return self.__id__


class JavaProxy(JavaBridgeObject):
    """ A bridge object that creates a Proxy for the given ref. This should NOT
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

    def __init__(self, ref=None, **kwargs):
        """ Sends the event to create this View in Java """
        super(Atom, self).__init__(**kwargs)

        #:
        ref = ref or self

        #: Send the event over the bridge to construct the view
        __id__ = kwargs.get('__id__', None)
        bridge.CACHE[self.__id__] = self
        if __id__ is None:
            self.__app__.send_event(
                Command.PROXY,  #: method
                self.__id__,  #: id to assign in bridge cache
                self.__nativeclass__,
                ref.__id__, #: Reference ID
            )

