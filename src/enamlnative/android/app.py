'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
import jnius
from atom.api import Float, Value, Int, Unicode, Typed, Dict
from enaml.application import ProxyResolver
from . import factories
from .android_activity import Activity
from ..core.app import BridgedApplication
from ..core import bridge


class AppEventListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['com/enaml/MainActivity$AppEventListener']
    __javacontext__ = 'app'

    def __init__(self, handler):
        self.__handler__ = handler
        super(AppEventListener, self).__init__()

    @jnius.java_method('([B)V')
    def onEvents(self, data):
        self.__handler__.on_events(bytearray(data))

    @jnius.java_method('()V')
    def onResume(self):
        self.__handler__.on_resume()

    @jnius.java_method('()V')
    def onPause(self):
        self.__handler__.on_pause()

    @jnius.java_method('()V')
    def onStop(self):
        self.__handler__.on_stop()

    @jnius.java_method('()V')
    def onDestroy(self):
        self.__handler__.on_destroy()


class AndroidApplication(BridgedApplication):
    """ An Android implementation of an Enaml Native BridgedApplication.

    A AndroidApplication uses the native Android widget toolkit to implement an Enaml UI that
    runs in the local process.

    """

    #: Attributes so it can be seralized over the bridge as a reference
    __nativeclass__ = Unicode('android.content.Context')

    #: Bridge widget
    widget = Typed(Activity)

    #: Android Activity (jnius class)
    activity = Value()

    #: Pixel density of the device
    #: Loaded immediately as this is used often.
    dp = Float()

    #: Build info from https://developer.android.com/reference/android/os/Build.VERSION.html
    build_info = Dict()

    #: SDK version
    #: Loaded immediately
    api_level = Int()

    #: Save reference to the event listener
    listener = Typed(AppEventListener)

    # --------------------------------------------------------------------------
    # Defaults
    # --------------------------------------------------------------------------
    def _default_widget(self):
        """ Return a bridge object reference to the MainActivity """
        return Activity(__id__=-1)

    def _default_dp(self):
        return self.activity.getResources().getDisplayMetrics().density

    def _default_build_info(self):
        info = bridge.loads(bytearray(self.activity.getBridge().getBuildInfo()))
        self.api_level = int(info['SDK_INT'])
        return info

    # --------------------------------------------------------------------------
    # AndroidApplication Constructor
    # --------------------------------------------------------------------------
    def __init__(self, activity):
        """ Initialize a AndroidApplication. Uses jnius to retrieve
            an instance of the activity.
        """
        super(AndroidApplication, self).__init__()
        self.activity = jnius.autoclass(activity).mActivity
        self.resolver = ProxyResolver(factories=factories.ANDROID_FACTORIES)

    # --------------------------------------------------------------------------
    # Abstract API Implementation
    # --------------------------------------------------------------------------
    def start(self):
        """ Start the application's main event loop. Bind the Android app event
            listener using jnius.
        """
        activity = self.activity

        #: Hook for JNI using jnius
        self.listener = AppEventListener(self)
        activity.setAppEventListener(self.listener)

        super(AndroidApplication, self).start()

    # --------------------------------------------------------------------------
    # App API Implementation
    # --------------------------------------------------------------------------
    def has_permission(self, permission):
        """ Return a future that resolves with the result of the permission """
        f = self.create_future()

        def on_result(allowed):
            result = allowed == Activity.PERMISSION_GRANTED
            self.set_future_result(f, result)

        self.widget.checkSelfPermission(permission).then(on_result)

        return f

    def request_permissions(self, permissions):
        """ Return a future that resolves with the results of the permission requests"""
        f = self.create_future()

        def on_results(code, perms, results):
            if code != 0xC0DE:
                return
            #: Check permissions
            results = {p: r == Activity.PERMISSION_GRANTED for (p, r) in zip(perms, results)}
            self.set_future_result(f, results)

        #: Setup our listener, and request the permission
        self.widget.setPermissionResultListener(self.widget.getId())
        self.widget.onRequestPermissionsResult.connect(on_results)
        self.widget.requestPermissions(permissions, 0xC0DE)

        return f

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
        self.activity.processEvents(data)

    # --------------------------------------------------------------------------
    # Android utilities API Implementation
    # --------------------------------------------------------------------------
    def _observe_keep_screen_on(self, change):
        """ Sets or clears the flag to keep the screen on. """
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
