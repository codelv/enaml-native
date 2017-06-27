'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 21, 2017

@author: jrm
'''
import ctypes
import msgpack
import traceback
from pprint import pprint
from contextlib import contextmanager

def get_app_class():
    """ Avoid circular import. Probably indicates a
        poor design...
    """
    from .app import AndroidApplication
    return AndroidApplication


def msgpack_encoder(sig, obj):
    """ When passing a JavaBridgeObject encode it in a special way so
        it can properly be interpreted as a reference.
    """
    if isinstance(obj, JavaBridgeObject):
        return (sig, obj.__id__)
    elif isinstance(obj, get_app_class()):
        return (sig, -1)
    return (sig, obj)


def dumps(data):
    """ Encodes events for sending over the bridge """
    if get_app_class().instance().debug:
        print "======== Py --> Java ======"
        pprint(data)
        print "==========================="
    return msgpack.dumps(data)


def loads(data):
    """ Decodes and processes events received from the bridge """
    events = msgpack.loads(data)
    if get_app_class().instance().debug:
        print "======== Py <-- Java ======"
        pprint(events)
        print "==========================="
    for event in events:
        if event[0] == 'event':
            ptr, method, args = event[1]
            invoke(ptr, method, *[v for t, v in args])


def invoke(ptr, method, *args):
    """ Dereference the pointer and call the handler method. """
    try:
        obj = ctypes.cast(ptr, ctypes.py_object).value
        if not hasattr(obj, method):
            raise NotImplementedError("{}.{} is not implemented.".format(type(obj), method))
        handler = getattr(obj, method)
        return handler(*args)
    except:
        traceback.print_exc()
        return


class JavaMethod(object):
    """ Description of a method of a View (or subclass) in Java. When called, this
        serializes call, packs the arguments, and delegates handling to a bridge in Java.
    """
    __slots__ = ('__signature__', '__javaobj__', '__name__', '__suppressed__', '__returns__')

    def __init__(self, *args, **kwargs):
        self.__returns__ = kwargs.get('returns', None)
        self.__signature__ = args
        self.__suppressed__ = False

    @contextmanager
    def suppressed(self):
        """ Suppress calls within this context to avoid feedback loops"""
        self.__suppressed__ = True
        yield
        self.__suppressed__ = False

    def __call__(self, *args):
        if self.__suppressed__:
            return

        vargs = self.__signature__ and self.__signature__[-1].endswith("...")
        if not vargs and (len(args) != len(self.__signature__)):
            raise ValueError("Invalid number of arguments: Given {}, expected {}"
                             .format(args, self.__signature__))
        if vargs:
            bridge_args = []
            varg = self.__signature__[-1].replace('...', '')
            for i in range(len(args)):
                sig = self.__signature__[i] if i+1 < len(self.__signature__) else varg
                bridge_args.append(msgpack_encoder(sig, args[i]))
        else:
            bridge_args = [msgpack_encoder(sig, arg) for sig, arg in zip(self.__signature__, args)]

        self.__javaobj__.__app__.send_event(
            'updateObject',  #: method
            self.__javaobj__.__id__,
            self.__name__,  #: method name
            bridge_args  #: args
        )

    def clone(self, owner):
        obj = type(self)(*self.__signature__)
        obj.__name__ = self.__name__
        obj.__javaobj__ = owner
        return obj


class JavaField(JavaMethod):
    def __init__(self, arg):
        super(JavaField, self).__init__(arg)

    def __set__(self, obj, arg):
        #: Get the cloned field
        if self.__suppressed__:
            return
        obj.__app__.send_event(
            'updateObjectField',  #: method
            obj.__id__,
            self.__name__,  #: method name
            [msgpack_encoder(self.__signature__[0], arg)]  #: args
        )

    def __get__(self, obj, objtype=None):
        raise NotImplementedError("Reading attributes is not yet supported")

    def __call__(self, *args, **kwargs):
        return object.__call__(self, *args, **kwargs)


class JavaCallback(JavaMethod):
    """ Description of a callback method of a View (or subclass) in Java. When called,
        it fires the connected callback. This is triggered when it receives an event from
        the bridge indicating the call has occured.
    """
    __slots__ = ('__callback__', )

    def __init__(self, *args):
        super(JavaCallback, self).__init__(*args)
        self.__callback__ = None

    def __call__(self, *args):
        """ Fire the callback if one is connected """
        if self.__callback__ and not self.__suppressed__:
            self.__callback__(*args)

    def connect(self, callback):
        """ Set the callback to be fired when the event occurs. """
        self.__callback__ = callback


class JavaBridgeObject(object):
    """ A proxy to a class in java. This sends the commands over
        the bridge for execution.

    """
    __slots__ = ('__app__', '__id__')
    __javaclass__ = 'java.lang.Object'
    __signature__ = ()
    __global_id__ = 0

    def __init__(self, *args):
        """ Sends the event to create this View in Java """

        #: Set the object id
        JavaBridgeObject.__global_id__ +=1
        self.__id__ = JavaBridgeObject.__global_id__  #: id(self)

        #: Set the app instance
        self.__app__ = get_app_class().instance()

        #: Get declared methods
        for base in reversed(type(self).__mro__):
            for name, method in base.__dict__.iteritems():
                if isinstance(method, JavaField):
                    method.__name__ = name
                    #: Do not clone
                elif isinstance(method, JavaMethod):
                    method.__name__ = name
                    setattr(self, name, method.clone(self))

        #: Send the event over the bridge to construct the view
        self.__app__.send_event(
            'createObject', #: method
            self.__id__, #: id to assign in java
            self.__javaclass__,
            [msgpack_encoder(sig, arg) for sig, arg in zip(self.__signature__, args)],
        )

    def __del__(self):
        self.__app__.send_event(
            'deleteObject', #: method
            self.__id__, #: id to assign in java
        )
