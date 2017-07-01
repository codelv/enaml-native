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
import functools
from pprint import pprint
from contextlib import contextmanager
from atom.api import Atom, ForwardInstance, Dict, Property, Callable, Unicode, Tuple, Int,  Instance, set_default

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
    if hasattr(obj, '__javaclass__'):
        return (sig, obj.__id__)
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


class JavaMethod(Property):
    """ Description of a method of a View (or subclass) in Java. When called, this
        serializes call, packs the arguments, and delegates handling to a bridge in Java.
    """
    __slots__ = ('__signature__', '__returns__')

    def __init__(self, *args, **kwargs):
        self.__returns__ = kwargs.get('returns', None)
        self.__signature__ = args
        super(JavaMethod, self).__init__(self.__fget__)

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

    def __call__(self, obj, *args):
        if obj.__suppressed__.get(self.name):
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

        obj.__app__.send_event(
            'updateObject',  #: method
            obj.__id__,
            self.name,  #: method name
            bridge_args  #: args
        )


class JavaField(Property):
    __slots__ = ('__signature__',)

    def __init__(self, arg):
        self.__signature__ = arg
        super(JavaField, self).__init__(self.__fget__, self.__fset__)

    def __fset__(self, obj, arg):
        obj.__app__.send_event(
            'updateObjectField',  #: method
            obj.__id__,
            self.name,  #: method name
            [msgpack_encoder(self.__signature__, arg)]  #: args
        )

    def __fget__(self, obj):
        raise NotImplementedError("Reading attributes is not yet supported")


class JavaCallback(JavaMethod):
    """ Description of a callback method of a View (or subclass) in Java. When called,
        it fires the connected callback. This is triggered when it receives an event from
        the bridge indicating the call has occured.
    """

    def __fget__(self, obj):
        f = super(JavaCallback, self).__fget__(obj)
        #: Add a method so it can be connected like in Qt
        f.connect = functools.partial(self.connect, obj)
        return f

    def __call__(self, obj, *args):
        """ Fire the callback if one is connected """
        if obj.__suppressed__.get(self.name):
            return
        callback = obj.__callbacks__.get(self.name)
        if callback:
            callback(*args)

    def connect(self, obj, callback):
        """ Set the callback to be fired when the event occurs. """
        obj.__callbacks__[self.name] = callback


__global_id__ = 0

class JavaBridgeObject(Atom):
    """ A proxy to a class in java. This sends the commands over
        the bridge for execution.

    """
    #: Java Class name
    __javaclass__ = Unicode('java.lang.Object')

    #: Constructor signature
    __signature__ = Tuple()

    #: Suppressed methods / fields
    __suppressed__ = Dict()

    #: Callbacks
    __callbacks__ = Dict()

    #: Java object ID
    __id__ = Int(0)

    #: Bridge
    __app__ = ForwardInstance(get_app_class)

    def _default___id__(self):
        global __global_id__
        __global_id__ += 1
        return __global_id__

    def _default___app__(self):
        return get_app_class().instance()

    def __init__(self, *args):
        """ Sends the event to create this View in Java """
        super(JavaBridgeObject, self).__init__()
        # #: Get declared methods
        # for base in reversed(type(self).__mro__):
        #     for name, method in base.__dict__.iteritems():
        #         if isinstance(method, JavaField):
        #             method.__name__ = name
        #             #: Do not clone
        #         elif isinstance(method, JavaMethod):
        #             method.__name__ = name
        #             setattr(self, name, method.clone(self))

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

# def test_bridge():
#     """ Nothing beats tests with actual usage :) """
#     class Widget(JavaBridgeObject):
#         pass
#
#     class View(Widget):
#         __javaclass__ = set_default('android.view.View')
#         __signature__ = set_default(('android.content.Context',))
#
#         def getId(self):
#             return self.__id__
#
#         addView = JavaMethod('android.view.View')
#         onClick = JavaCallback('android.view.View')
#         setOnClickListener = JavaMethod('android.view.View$OnClickListener')
#         setLayoutParams = JavaMethod('android.view.ViewGroup.LayoutParams')
#         setBackgroundColor = JavaMethod('android.graphics.Color')
#         setClickable = JavaMethod('boolean')
#         setTop = JavaMethod('int')
#         setBottom = JavaMethod('int')
#         setLeft = JavaMethod('int')
#         setRight = JavaMethod('int')
#         setLayoutDirection = JavaMethod('int')
#         setLayoutParams = JavaMethod('android.view.ViewGroup$LayoutParams')
#         setPadding = JavaMethod('int', 'int', 'int', 'int')
#
#         setX = JavaMethod('int')
#         setY = JavaMethod('int')
#         setZ = JavaMethod('int')
#         setMaximumHeight = JavaMethod('int')
#         setMaximumWidth = JavaMethod('int')
#         setMinimumHeight = JavaMethod('int')
#         setMinimumWidth = JavaMethod('int')
#         setEnabled = JavaMethod('boolean')
#         setTag = JavaMethod('java.lang.Object')
#         setToolTipText = JavaMethod('java.lang.CharSequence')
#         setVisibility = JavaMethod('int')
#         removeView = JavaMethod('android.view.View')
#
#         LAYOUT_DIRECTIONS = {
#             'ltr': 0,
#             'rtl': 1,
#             'locale': 3,
#             'inherit': 2,
#         }
#
#     class ViewGroup(View):
#         __javaclass__ = set_default('android.view.ViewGroup')
#
#     class FrameLayout(ViewGroup):
#         __javaclass__ = set_default('android.widget.FrameLayout')
#         setForegroundGravity = JavaMethod('int')
#         setMeasureAllChildren = JavaMethod('boolean')
#
#
#     class DrawerLayout(ViewGroup):
#         __javaclass__ = set_default('android.support.v4.widget.DrawerLayout')
#         openDrawer = JavaMethod('android.view.View')
#         closeDrawer = JavaMethod('android.view.View')
#         addDrawerListener = JavaMethod('android.support.v4.widget.DrawerLayout$DrawerListener')
#         onDrawerClosed = JavaCallback('android.view.View')
#         onDrawerOpened = JavaCallback('android.view.View')
#         onDrawerSlide = JavaCallback('android.view.View', 'float')
#         onDrawerStateChanged = JavaCallback('int')
#
#         setDrawerElevation = JavaMethod('float')
#         setDrawerTitle = JavaMethod('int', 'java.lang.CharSequence')
#         setDrawerLockMode = JavaMethod('int')
#         setScrimColor = JavaMethod('android.graphics.Color')
#         setStatusBarBackgroundColor = JavaMethod('android.graphics.Color')
#
#         LOCK_MODES = {
#             'unlocked': 0,
#             'locked_closed': 1,
#             'locked_open': 2,
#             'undefined': 3,
#         }
#
#     return DrawerLayout