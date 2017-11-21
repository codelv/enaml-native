"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

"""
import nativehooks #: Created by the ndk-build in pybridge.c
from atom.api import Float, Value, Int, List, Unicode, Typed, Dict
from enaml.application import ProxyResolver
from . import factories
from .android_activity import Activity
from ..core.app import BridgedApplication
from ..core import bridge


class AndroidApplication(BridgedApplication):
    """ An Android implementation of an Enaml Native BridgedApplication.

    A AndroidApplication uses the native Android widget toolkit to implement 
    an Enaml UI that runs in the local process.

    """

    #: Attributes so it can be serialized over the bridge as a reference
    __nativeclass__ = Unicode('android.content.Context')

    #: Bridge widget
    widget = Typed(Activity)

    #: Android Activity (jnius class)
    activity = Value()

    #: Pixel density of the device
    #: Loaded immediately as this is used often.
    dp = Float()

    #: Build info from
    #: https://developer.android.com/reference/android/os/Build.VERSION.html
    build_info = Dict()

    #: SDK version
    #: Loaded immediately
    api_level = Int()

    #: Permission code increments on each request
    _permission_code = Int()

    #: Pending permission request listeners
    _permission_requests = Dict()

    # -------------------------------------------------------------------------
    # Defaults
    # -------------------------------------------------------------------------
    def _default_widget(self):
        """ Return a bridge object reference to the MainActivity
         
         """
        return Activity(__id__=-1)

    # -------------------------------------------------------------------------
    # AndroidApplication Constructor
    # -------------------------------------------------------------------------
    def __init__(self, activity=None):
        """ Initialize a AndroidApplication. Uses jnius to retrieve
            an instance of the activity.
            
        """
        super(AndroidApplication, self).__init__()
        self.resolver = ProxyResolver(factories=factories.ANDROID_FACTORIES)

        #: Add a ActivityLifecycleListener to update the application state
        self.widget.addActivityLifecycleListener(self.widget.getId())
        self.widget.onActivityLifecycleChanged.connect(
            self.on_activity_lifecycle_changed)

    # -------------------------------------------------------------------------
    # App API Implementation
    # -------------------------------------------------------------------------
    def has_permission(self, permission):
        """ Return a future that resolves with the result of the permission 
        
        """
        f = self.create_future()

        #: Old versions of android did permissions at install time
        if self.api_level < 23:
            f.set_result(True)
            return f

        def on_result(allowed):
            result = allowed == Activity.PERMISSION_GRANTED
            self.set_future_result(f, result)

        self.widget.checkSelfPermission(permission).then(on_result)

        return f

    def request_permissions(self, permissions):
        """ Return a future that resolves with the results 
        of the permission requests
        
        """
        f = self.create_future()

        #: Old versions of android did permissions at install time
        if self.api_level < 23:
            f.set_result({p: True for p in permissions})
            return f

        w = self.widget
        request_code = self._permission_code
        self._permission_code += 1  #: So next call has a unique code

        #: On first request, setup our listener, and request the permission
        if request_code == 0:
            w.setPermissionResultListener(w.getId())
            w.onRequestPermissionsResult.connect(self._on_permission_result)

        def on_results(code, perms, results):
            #: Check permissions
            f.set_result({p: r == Activity.PERMISSION_GRANTED
                          for (p, r) in zip(perms, results)})

        #: Save a reference
        self._permission_requests[request_code] = on_results

        #: Send out the request
        self.widget.requestPermissions(permissions, request_code)

        return f

    def show_toast(self, msg, long=True):
        """ Show a toast message for the given duration.
        This is an android specific api.

        Parameters
        -----------
        msg: str
            Text to display in the toast message
        long: bool
            Display for a long or short (system defined) duration

        """
        from .android_toast import Toast

        def on_toast(ref):
            t = Toast(__id__=ref)
            t.show()

        Toast.makeText(self, msg, 1 if long else 0).then(on_toast)

    def on_activity_lifecycle_changed(self, state):
        """ Update the state when the android app is paused, resumed, etc..
        
        Widgets can observe this value for changes if they need to react
        to app lifecycle changes.
        
        """
        self.state = state

    # --------------------------------------------------------------------------
    # Bridge API Implementation
    # --------------------------------------------------------------------------
    def show_view(self):
        """ Show the current `app.view`. This will fade out the previous
            with the new view.
            
        """
        if not self.build_info:
            def on_build_info(info):
                """ Make sure the build info is ready before we 
                display the view 
                
                """
                self.dp = info['DISPLAY_DENSITY']
                self.api_level = info['SDK_INT']
                self.build_info = info
                self._show_view()

            self.widget.getBuildInfo().then(on_build_info)
        else:
            self._show_view()

    def _show_view(self):
        """ Show the view """
        self.widget.setView(self.get_view())

    def dispatch_events(self, data):
        """ Send the data to the Native application for processing """
        nativehooks.publish(data)

    # -------------------------------------------------------------------------
    # Android utilities API Implementation
    # -------------------------------------------------------------------------
    def _on_permission_result(self, code, perms, results):
        """ Handles a permission request result by passing it to the
         handler with the given code.
         
        """
        #: Get the handler for this request
        handler = self._permission_requests.get(code, None)
        if handler is not None:
            del self._permission_requests[code]

            #: Invoke that handler with the permission request response
            handler(code, perms, results)

    def _observe_keep_screen_on(self, change):
        """ Sets or clears the flag to keep the screen on. 
        
        """
        def set_screen_on(window):
            from .android_window import Window
            window = Window(__id__=window)
            if self.keep_screen_on:
                window.addFlags(Window.FLAG_KEEP_SCREEN_ON)
            else:
                window.clearFlags(Window.FLAG_KEEP_SCREEN_ON)

        self.widget.getWindow().then(set_screen_on)

    def get_system_service(self, service):
        """ Wrapper for getSystemService. You MUST
        wrap the class with the appropriate object.
        
        """
        return self.widget.getSystemService(service)

    # -------------------------------------------------------------------------
    # Plugin API Implementation
    # -------------------------------------------------------------------------
    def load_plugin_factories(self):
        """ Add any plugin toolkit widgets to the ANDROID_FACTORIES 
        
        """
        for plugin in self.get_plugins(group='enaml_native_android_factories'):
            get_factories = plugin.load()
            PLUGIN_FACTORIES = get_factories()
            factories.ANDROID_FACTORIES.update(PLUGIN_FACTORIES)
