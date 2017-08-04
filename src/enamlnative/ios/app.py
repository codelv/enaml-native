'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
from atom.api import Atom, Float, Value, Unicode, Typed, set_default
from enaml.application import ProxyResolver
from . import factories
from .bridge import ObjcBridgeObject
from ..core.app import BridgedApplication
import ctypes
from ctypes.util import find_library


class AppDelegate(ObjcBridgeObject):
    __nativeclass__ = set_default("AppDelegate")

    """ Access ENBridge.m using ctypes.

    Based on:
    https://stackoverflow.com/questions/1490039/calling-objective-c-functions-from-python#1490644

    """
    #: Objc library
    objc = Value()

    #: Bridge.m
    bridge = Value()

    def _default_objc(self):
        objc = ctypes.cdll.LoadLibrary(find_library('objc'))
        objc.objc_getClass.restype = ctypes.c_void_p
        objc.sel_registerName.restype = ctypes.c_void_p
        objc.objc_msgSend.restype = ctypes.c_void_p
        objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        return objc

    def _default_bridge(self):
        objc = self.objc
        ENBridge = objc.objc_getClass('ENBridge')
        return objc.objc_msgSend(ENBridge, objc.sel_registerName('instance'))

    def processEvents(self, data):
        objc = self.objc
        bridge = self.bridge
        #: This must come after the above as it changes the arguments!
        objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
        objc.objc_msgSend(bridge, objc.sel_registerName('processEvents:length:'), data, len(data))


class IPhoneApplication(BridgedApplication):
    """ An iPhone implementation of an Enaml Native BridgedApplication.

    An IPhoneApplication uses the native iOS widget toolkit to implement an Enaml UI that
    runs in the local process.

    Since Objective-C can easily use the Python C-API, much if this classes implementation
    is done directly. For instance, the AppEventListener API is implemented directly in
    Objective-C (in Bridge.m) and invokes methods on this directly.


    """

    #: Attributes so it can be seralized over the bridge as a reference
    __nativeclass__ = Unicode('android.content.Context')

    #: AppDelegate widget
    widget = Typed(AppDelegate)

    #: Android Activity
    activity = Value()

    #: Pixel density of the device
    #: Loaded immediately as this is used often.
    dp = Float()

    # --------------------------------------------------------------------------
    # Defaults
    # --------------------------------------------------------------------------
    def _default_widget(self):
        """ Return a bridge object reference to the MainActivity """
        return AppDelegate(__id__=-1)

    def _default_dp(self):
        #:TODO: return self.activity.getResources().getDisplayMetrics().density
        return 1.0

    # --------------------------------------------------------------------------
    # IPhoneApplication Constructor
    # --------------------------------------------------------------------------
    def __init__(self):
        """ Initialize a IPhoneApplication.
        """
        super(IPhoneApplication, self).__init__()
        self.resolver = ProxyResolver(factories=factories.IOS_FACTORIES)

    # --------------------------------------------------------------------------
    # Bridge API Implementation
    # --------------------------------------------------------------------------
    def show_view(self):
        """ Show the current `app.view`. This will fade out the previous
            with the new view.
        """
        self.widget.setView(self.get_view())

    def dispatch_events(self, data):
        """ Send the data to the Native application for processing """
        self.widget.processEvents(data)

    # --------------------------------------------------------------------------
    # iPhone utilities API Implementation
    # --------------------------------------------------------------------------
    def _observe_keep_screen_on(self, change):
        """ Sets or clears the flag to keep the screen on. """
        raise NotImplementedError
        def set_screen_on(window):
            from .ios_window import Window
            window = Window(__id__=window)
            if self.keep_screen_on:
                window.addFlags(Window.FLAG_KEEP_SCREEN_ON)
            else:
                window.clearFlags(Window.FLAG_KEEP_SCREEN_ON)

        self.widget.getWindow().then(set_screen_on)
