'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 21, 2017

@author: jrm
'''
import msgpack
from atom.api import Atom, ForwardInstance, Dict, Unicode, Tuple, Int
from weakref import WeakValueDictionary

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
    """ Encode an object for proper decoding by Java
    """
    if hasattr(obj, '__nativeclass__'):
        return msgpack.ExtType(ExtType.REF, msgpack.packb(obj.__id__))
    return obj


def msgpack_encoder(sig, obj):
    """ When passing a JavaBridgeObject encode it in a special way so
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

    #: Java object ID
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
        self.__app__.send_event(
            Command.DELETE,  #: method
            self.__id__,  #: id to assign in java
        )
        _cleanup_id(self)
