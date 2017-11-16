"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

"""
import ctypes
from ctypes.util import find_library
from atom.api import Atom, Float, Value, Unicode, Int, Typed
from enaml.application import ProxyResolver
from . import factories
from .bridge import ObjcBridgeObject, ObjcMethod
from ..core.app import BridgedApplication


class ENBridge(ObjcBridgeObject):
    """ Access ENBridge.m using ctypes.

    Based on:
    https://stackoverflow.com/questions/1490039/
    calling-objective-c-functions-from-python#1490644

    """
    #: Objc library
    objc = Value()

    #: Bridge.m access via ctypes
    bridge = Value()

    def _default_objc(self):
        """ Load the objc library using ctypes. """
        objc = ctypes.cdll.LoadLibrary(find_library('objc'))
        objc.objc_getClass.restype = ctypes.c_void_p
        objc.sel_registerName.restype = ctypes.c_void_p
        objc.objc_msgSend.restype = ctypes.c_void_p
        objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        return objc

    def _default_bridge(self):
        """ Get an instance of the ENBridge object using ctypes. """
        objc = self.objc
        ENBridge = objc.objc_getClass('ENBridge')
        return objc.objc_msgSend(ENBridge, objc.sel_registerName('instance'))

    def processEvents(self, data):
        """ Sends msgpack data to the ENBridge instance
            by calling the processEvents method via ctypes. """
        objc = self.objc
        bridge = self.bridge
        #: This must come after the above as it changes the arguments!
        objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                      ctypes.c_char_p, ctypes.c_int]
        objc.objc_msgSend(
            bridge, objc.sel_registerName('processEvents:length:'),
            data, len(data))

    #: Add a target to a UIControl that invokes a python callback
    addTarget = ObjcMethod('UIControl',
                           dict(forControlEvents="enum"),#""UIControlEvents"),
                           dict(andCallback="int"),
                           dict(usingMethod="NSString"),
                           dict(withValues="NSArray"))


class AppDelegate(ObjcBridgeObject):
    pass


class ViewController(ObjcBridgeObject):
    displayView = ObjcMethod('UIView')


class IPhoneApplication(BridgedApplication):
    """ An iPhone implementation of an Enaml Native BridgedApplication.

    An IPhoneApplication uses the native iOS widget toolkit to implement an 
    Enaml UI that runs in the local process.

    Since Objective-C can easily use the Python C-API, much if this classes 
    implementation is done directly. For instance, the AppEventListener API is 
    implemented directly in Objective-C (in Bridge.m) and invokes methods 
    on this directly.

    """

    #: AppDelegate widget
    app_delegate = Typed(AppDelegate)

    #: ViewControler
    view_controller = Typed(ViewController)

    #: ENBridge
    bridge = Typed(ENBridge)

    #: Pixel density of the device
    #: Loaded immediately as this is used often.
    dp = Float()

    # --------------------------------------------------------------------------
    # Defaults
    # --------------------------------------------------------------------------
    def _default_app_delegate(self):
        """ Return a bridge object reference to the AppDelegate
        this bridge sets this using a special id of -1
        
        """
        return AppDelegate(__id__=-1)

    def _default_view_controller(self):
        """ Return a bridge object reference to the ViewController
        the bridge sets this using a special id of -2
        
        """
        return ViewController(__id__=-2)

    def _default_bridge(self):
        """ Access the bridge using ctypes. Everything else should use 
        bridge objects. 
        
        """
        return ENBridge(__id__=-4)

    def _default_dp(self):
        return 1.0

    # -------------------------------------------------------------------------
    # IPhoneApplication Constructor
    # -------------------------------------------------------------------------
    def __init__(self):
        """ Initialize a IPhoneApplication.
        
        """
        super(IPhoneApplication, self).__init__()
        self.resolver = ProxyResolver(factories=factories.IOS_FACTORIES)

    # -------------------------------------------------------------------------
    # Bridge API Implementation
    # -------------------------------------------------------------------------
    def show_view(self):
        """ Show the current `app.view`. This will fade out the previous
        with the new view.
        """
        self.view_controller.displayView(self.get_view())

    def dispatch_events(self, data):
        """ Send the data to the Native application for processing """
        self.bridge.processEvents(data)

    # -------------------------------------------------------------------------
    # iPhone utilities API Implementation
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Plugin API Implementation
    # -------------------------------------------------------------------------
    def load_plugin_factories(self):
        """ Add any plugin toolkit widgets to the ANDROID_FACTORIES """
        for plugin in self.get_plugins(group='enaml_native_ios_factories'):
            get_factories = plugin.load()
            PLUGIN_FACTORIES = get_factories()
            factories.IOS_FACTORIES.update(PLUGIN_FACTORIES)
