"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

@author jrm

"""
import nativehooks  #: Created by the ndk-build in pybridge.c
from asyncio import Future
from atom.api import Float, Value, Int, List, Str, Typed, Dict, Event
from enaml.application import ProxyResolver
from . import factories
from .android_activity import Activity
from .android_window import Window
from ..core.app import BridgedApplication
from ..core import bridge

ORIENTATIONS = ("square", "portrait", "landscape")


class AndroidApplication(BridgedApplication):
    """An Android implementation of an Enaml Native BridgedApplication.

    A AndroidApplication uses the native Android widget toolkit to implement
    an Enaml UI that runs in the local process.

    """

    #: Attributes so it can be serialized over the bridge as a reference
    __nativeclass__ = "android.content.Context"

    #: Bridge widget
    widget = Typed(Activity)

    #: Application Window
    window = Typed(Window)

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

    #: Triggered when the back button is pressed. This can be observed
    #: to handle back presses.
    back_pressed = Event(dict)

    #: Permission code increments on each request
    _permission_code = Int()

    #: Pending permission request listeners
    _permission_requests = Dict(int, Future)

    # -------------------------------------------------------------------------
    # Defaults
    # -------------------------------------------------------------------------
    def _default_widget(self):
        """Return a bridge object reference to the MainActivity"""
        return Activity(__id__=-1)

    # -------------------------------------------------------------------------
    # AndroidApplication Constructor
    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Initialize a AndroidApplication. Uses jnius to retrieve
        an instance of the activity.

        """
        super().__init__(*args, **kwargs)
        self.resolver = ProxyResolver(factories=factories.ANDROID_FACTORIES)

    def init_widget(self):
        """Initialize on the first call"""
        #: Add a ActivityLifecycleListener to update the application state
        activity = self.widget
        activity.addActivityLifecycleListener(activity.getId())
        activity.onActivityLifecycleChanged.connect(self.on_activity_lifecycle_changed)

        #: Add BackPressedListener to trigger the event
        activity.addBackPressedListener(activity.getId())
        activity.onBackPressed.connect(self.on_back_pressed)

        #: Add ConfigurationChangedListener to trigger the event
        activity.addConfigurationChangedListener(activity.getId())
        activity.onConfigurationChanged.connect(self.on_configuration_changed)

        self.deferred_call(self.init_window)

    async def init_window(self):
        """ """
        window_id = await self.widget.getWindow()
        self.window = Window(__id__=window_id)
        self.set_keep_screen_on(self.keep_screen_on)
        if self.statusbar_color:
            self.set_statusbar_color(self.statusbar_color)

    # -------------------------------------------------------------------------
    # App API Implementation
    # -------------------------------------------------------------------------
    async def has_permission(self, permission: str) -> bool:
        """Return a future that resolves with the result of the permission"""
        # Old versions of android did permissions at install time
        if self.api_level < 23:
            return True
        result = await self.widget.checkSelfPermission(permission)
        return result == Activity.PERMISSION_DENIED

    async def request_permissions(self, *permissions) -> dict[str, bool]:
        """Return a future that resolves with the results
        of the permission requests

        """
        # Old versions of android did permissions at install time
        if self.api_level < 23:
            return {p: True for p in permissions}

        w = self.widget
        request_code = self._permission_code
        self._permission_code += 1  #: So next call has a unique code

        # On first request, setup our listener, and request the permission
        if request_code == 0:
            w.setPermissionResultListener(w.getId())
            w.onRequestPermissionsResult.connect(self._on_permission_result)

        #: Save a reference
        f = self.widget.requestPermissions(permissions, request_code)
        self._permission_requests[request_code] = f

        #: Send out the request
        code, perms, results = await f
        granted = Activity.PERMISSION_GRANTED
        return {p: r == granted for p, r in zip(perms, results)}

    async def show_toast(self, msg, long=True):
        """Show a toast message for the given duration.
        This is an android specific api.

        Parameters
        -----------
        msg: str
            Text to display in the toast message
        long: bool
            Display for a long or short (system defined) duration

        """
        from .android_toast import Toast

        toast_id = await Toast.makeText(self, msg, 1 if long else 0)
        t = Toast(__id__=toast_id)
        t.show()

    def on_activity_lifecycle_changed(self, state):
        """Update the state when the android app is paused, resumed, etc..

        Widgets can observe this value for changes if they need to react
        to app lifecycle changes.

        """
        self.state = state

    def on_back_pressed(self):
        """Fire the `back_pressed` event with a dictionary with a 'handled'
        key when the back hardware button is pressed

        If 'handled' is set to any value that evaluates to True the
        default event implementation will be ignored.

        """
        try:
            event = {"handled": False}
            self.back_pressed(event)
            return bool(event.get("handled", False))
        except Exception as e:
            self.show_error(f"Error handling back press: {e}")
            #: Must return a boolean or we will cause android to abort
            return False

    def on_configuration_changed(self, config):
        """Handles a screen configuration change."""
        self.width = config["width"]
        self.height = config["height"]
        self.orientation = ORIENTATIONS[config["orientation"]]

    # --------------------------------------------------------------------------
    # Bridge API Implementation
    # --------------------------------------------------------------------------
    def show_view(self):
        """Show the current `app.view`. This will fade out the previous
        with the new view.

        """
        if not self.build_info:

            def on_build_info(f):
                """Make sure the build info is ready before we
                display the view

                """
                info = f.result()
                self.dp = info["DISPLAY_DENSITY"]
                self.width = info["DISPLAY_WIDTH"]
                self.height = info["DISPLAY_HEIGHT"]
                self.orientation = ORIENTATIONS[info["DISPLAY_ORIENTATION"]]
                self.api_level = info["SDK_INT"]
                self.build_info = info
                self._show_view()

            self.init_widget()
            self.widget.getBuildInfo().add_done_callback(on_build_info)
        else:
            self._show_view()

    def _show_view(self):
        """Show the view"""
        self.widget.setView(self.get_view())

    def dispatch_events(self, data):
        """Send the data to the Native application for processing"""
        nativehooks.publish(data)

    # -------------------------------------------------------------------------
    # Android utilities API Implementation
    # -------------------------------------------------------------------------
    def _on_permission_result(self, code, perms, results):
        """Handles a permission request result by passing it to the
        handler with the given code.

        """
        #: Get the handler for this request
        f = self._permission_requests.pop(code, None)
        if f is not None:
            #: Invoke that handler with the permission request response
            f.set_result((code, perms, results))

    def _observe_keep_screen_on(self, change):
        """Sets or clears the flag to keep the screen on."""
        self.set_keep_screen_on(self.keep_screen_on)

    def set_keep_screen_on(self, keep_on):
        """Set or clear the window flag to keep the screen on"""
        window = self.window
        if not window:
            return
        if keep_on:
            window.addFlags(Window.FLAG_KEEP_SCREEN_ON)
        else:
            window.clearFlags(Window.FLAG_KEEP_SCREEN_ON)

    def _observe_statusbar_color(self, change):
        """Sets or clears the flag to keep the screen on."""
        self.set_statusbar_color(self.statusbar_color)

    def set_statusbar_color(self, color):
        """Set the color of the system statusbar."""
        window = self.window
        if not window:
            return
        window.setStatusBarColor(color)

    async def get_system_service(self, cls):
        """Wrapper for getSystemService. You MUST
        wrap the class with the appropriate object.

        """
        service = cls.instance()
        if service:
            return service
        service_id = await self.widget.getSystemService(cls.SERVICE_TYPE)
        return cls(__id__=service_id)

    # -------------------------------------------------------------------------
    # Plugin API Implementation
    # -------------------------------------------------------------------------
    def load_plugin_factories(self):
        """Add any plugin toolkit widgets to the ANDROID_FACTORIES"""
        for plugin in self.get_plugins(group="enaml_native_android_factories"):
            get_factories = plugin.load()
            PLUGIN_FACTORIES = get_factories()
            factories.ANDROID_FACTORIES.update(PLUGIN_FACTORIES)
