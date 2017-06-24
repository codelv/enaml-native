'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 21, 2017

@author: jrm
'''


def msgpack_encoder(sig, obj):
    """ When passing a JavaBridgeObject encode it in a special way so
        it can properly be interpreted as a reference.
    """
    if isinstance(obj, JavaBridgeObject):
        return (sig, obj.__view_id__)
    return (sig, obj)


class JavaMethod(object):
    __slots__ = ('__signature__', '__view__', '__name__')

    def __init__(self, *args):
        self.__signature__ = args

    def __call__(self, *args):
        if len(args) != len(self.__signature__):
            raise ValueError("Invalid number of arguments: Given {}, expected {}"
                             .format(args,self.__signature__))
        self.__view__.__app__.send_event(
            'updateView',  #: method
            self.__view__.__view_id__,
            self.__name__,  #: method name
            [msgpack_encoder(sig, arg) for sig, arg in zip(self.__signature__, args)]  #: args
        )


class JavaCallback(JavaMethod):
    __slots__ = ('__signature__', '__view__', '__name__')

    def connect(self, callback):
        self.__callback__ = callback
        self.__view__.__app__.send_event(
            'connectCallback',  #: method
            self.__view__.__view_id__,
            self.__name__,  #: method name
            [msgpack_encoder(sig, arg) for sig, arg in zip(self.__signature__, args)]  #: args
        )

class MetaJavaBridgeObject(type):
    """

    """
    def __new__(mcs, name, bases, dct):
        if '__slots__' not in dct:
            dct['__slots__'] = ()

        methods = {}
        #: Get superclass methods
        for b in reversed(bases):
            if hasattr(b, '__java_methods__'):
                for prop, val in b.__java_methods__.iteritems():
                    clone = JavaMethod(*val.__signature__)
                    clone.__name__ = prop
                    methods[prop] = clone

        #: Get declared methods
        for prop, val in dct.iteritems():
            if isinstance(val, JavaMethod):
                clone = JavaMethod(*val.__signature__)
                clone.__name__ = prop
                methods[prop] = clone

        #: Update methods
        dct.update(methods)

        cls = super(MetaJavaBridgeObject, mcs).__new__(mcs, name, bases, dct)
        cls.__java_methods__ = methods
        return cls

class JavaBridgeObject(object):
    """ A proxy to a class in java. This sends the commands over
        the bridge for execution.

    """
    __slots__ = ('__app__', '__view_id__')
    __metaclass__ = MetaJavaBridgeObject
    __javaclass__ = 'java.lang.Object'
    __id__ = 0

    def __init__(self, context):
        """ Sends the event to create this View in Java """
        self.__app__ = context
        JavaBridgeObject.__id__ += 1
        self.__view_id__ = JavaBridgeObject.__id__

        for m in self.__java_methods__.itervalues():
            m.__view__ = self



        #: Send the event over the bridge to construct the view
        self.__app__.send_event(
            'createView', #: method
            self.__javaclass__,
            self.__view_id__ #: args
        )

    # def __getattr__(self, item):
    #     """ Send the event to call this method in Java.
    #         This is write only!
    #     """
    #     def method(*args):
    #         #: Send the event over the bridge to update the view
    #         self.__app__.send_event(
    #             'updateView', #: method
    #             self.__view_id__,
    #             item,
    #             [msgpack_encoder(arg) for arg in args] #: args
    #         )
    #     return method
