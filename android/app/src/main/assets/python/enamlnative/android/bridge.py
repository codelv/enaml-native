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


def msgpack_encoder(sig, obj):
    """ When passing a JavaBridgeObject encode it in a special way so
        it can properly be interpreted as a reference.
    """
    if isinstance(obj, JavaBridgeObject):
        return (sig, obj.__view_id__)
    return (sig, obj)


def dumps(data):
    """ Encodes events for sending over the bridge """
    print "======== Py --> Java ======"
    pprint(data)
    print "==========================="
    return msgpack.dumps(data)


def loads(data):
    """ Decodes and processes events received from the bridge """
    events = msgpack.loads(data)
    print "======== Py <-- Java ======"
    pprint(events)
    print "==========================="
    for event in events:
        if event[0]=='viewEvent':
            ptr, method, args = event[1]
            invoke(ptr, method, *[v for t,v in args])


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
    __slots__ = ('__signature__', '__view__', '__name__','__suppressed__')

    def __init__(self, *args):
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
        elif len(args) != len(self.__signature__):
            raise ValueError("Invalid number of arguments: Given {}, expected {}"
                             .format(args, self.__signature__))
        self.__view__.__app__.send_event(
            'updateView',  #: method
            self.__view__.__view_id__,
            self.__name__,  #: method name
            [msgpack_encoder(sig, arg) for sig, arg in zip(self.__signature__, args)]  #: args
        )

    def clone(self):
        cls = type(self)
        return cls(*self.__signature__)


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
    __slots__ = ('__app__', '__view_id__')
    __javaclass__ = 'java.lang.Object'

    def __init__(self, context):
        """ Sends the event to create this View in Java """
        self.__app__ = context
        self.__view_id__ = id(self)

        #: Get declared methods
        for base in reversed(type(self).__mro__):
            for name, method in base.__dict__.iteritems():
                if isinstance(method, JavaMethod):
                    clone = method.clone()
                    clone.__name__ = name
                    clone.__view__ = self
                    setattr(self, name, clone)

        #: Send the event over the bridge to construct the view
        self.__app__.send_event(
            'createView', #: method
            self.__javaclass__,
            self.__view_id__ #: args
        )
