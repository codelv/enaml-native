"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 24, 2017

@author: jrm
"""

from atom.api import Int, Typed, Instance
from enamlnative.widgets.activity import ProxyActivity
from .android_content import Context, Intent
from .android_view import View
from .android_utils import HashMap
from .bridge import JavaCallback, JavaMethod


class Activity(Context):
    """Access to the activity over the bridge"""

    #: As long as the user subclasses the EnamlActivity
    #: everything in this class will work
    __nativeclass__ = "com.codelv.enamlnative.EnamlActivity"

    #: ID of -1 is a special reference on the bridge to the activity.
    __id__ = Int(-1)

    ORIENTATIONS = ("square", "portrait", "landscape")

    #: Tracing methods
    startTrace = JavaMethod(str)
    stopTrace = JavaMethod(str)
    resetBridgeStats = JavaMethod()
    resetBridgeCache = JavaMethod()

    setView = JavaMethod(View)
    showLoading = JavaMethod(str)
    setActionBar = JavaMethod("android.widget.Toolbar")
    setSupportActionBar = JavaMethod("androidx.appcompat.widget.Toolbar")
    setContentView = JavaMethod(View)
    getWindow = JavaMethod(returns="android.view.Window")

    getSupportFragmentManager = JavaMethod(
        returns="androidx.fragment.app.FragmentManager"
    )
    getBuildInfo = JavaMethod(returns=HashMap)

    #: Permissions
    checkSelfPermission = JavaMethod(str, returns=int)
    requestPermissions = JavaMethod(list[str], int)
    onRequestPermissionsResult = JavaCallback(int, list[str], list[int])

    #: Method added so we can listen externally
    setPermissionResultListener = JavaMethod(
        "com.codelv.enamlnative.EnamlActivity$PermissionResultListener"
    )

    PERMISSION_GRANTED = 0
    PERMISSION_DENIED = -1

    #: Activity results
    addActivityResultListener = JavaMethod(
        "com.codelv.enamlnative.EnamlActivity$ActivityResultListener"
    )
    removeActivityResultListener = JavaMethod(
        "com.codelv.enamlnative.EnamlActivity$ActivityResultListener"
    )
    onActivityResult = JavaCallback(int, int, Intent, returns=bool)

    #: Activity lifecycle listener
    addActivityLifecycleListener = JavaMethod(
        "com.codelv.enamlnative.EnamlActivity$ActivityLifecycleListener"
    )
    removeActivityLifecycleListener = JavaMethod(
        "com.codelv.enamlnative.EnamlActivity$ActivityLifecycleListener"
    )
    #: Called with the lifecycle state like 'pause', 'resume', etc...
    onActivityLifecycleChanged = JavaCallback(str)

    #: Back pressed listener
    addBackPressedListener = JavaMethod(
        "com.codelv.enamlnative.EnamlActivity$BackPressedListener"
    )
    removeBackPressedListener = JavaMethod(
        "com.codelv.enamlnative.EnamlActivity$BackPressedListener"
    )

    #: Called with the lifecycle state like 'pause', 'resume', etc...
    onBackPressed = JavaCallback(returns=bool)

    #: Back pressed listener
    addConfigurationChangedListener = JavaMethod(
        "com.codelv.enamlnative.EnamlActivity$ConfigurationChangedListener"
    )
    removeConfigurationChangedListener = JavaMethod(
        "com.codelv.enamlnative.EnamlActivity$ConfigurationChangedListener"
    )

    #: Called with the lifecycle state like 'pause', 'resume', etc...
    onConfigurationChanged = JavaCallback(HashMap)


class AndroidActivity(ProxyActivity):

    #: Reference to the activty
    widget = Typed(Activity)

    #: Default window id
    window_id = Int()

    #: View currently displayed
    view = Instance(View)

    def create_widget(self):
        self.widget = Activity(__id__=-1)

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

    async def start(self):
        """Start the activity and retrieve the window id"""
        # NOTE: This does NOT inherit from the AndroidToolkitObject
        # so it must be initialized here
        self.create_widget()
        self.init_widget()
        activity = self.widget
        d = self.declaration
        info = d.build_info = await activity.getBuildInfo()
        d.dp = info["DISPLAY_DENSITY"]
        d.width = info["DISPLAY_WIDTH"]
        d.height = info["DISPLAY_HEIGHT"]
        d.orientation = Activity.ORIENTATIONS[info["DISPLAY_ORIENTATION"]]
        d.api_level = info["SDK_INT"]
        self.window_id = await activity.getWindow()

    def activate_bottom_up(self):
        """Show the first child view of the window"""
        self.reload_view()

    def child_added(self, child):
        super().child_added(child)
        if self.window_id:
            self.reload_view()

    def reload_view(self):
        activity = self.widget
        window = next(self.children())
        view = self.view = next(window.child_widgets())
        activity.setView(view)

    def show_loading(self, message):
        self.widget.showLoading(message)

    def on_activity_lifecycle_changed(self, state):
        """Update the state when the android app is paused, resumed, etc..

        Widgets can observe this value for changes if they need to react
        to app lifecycle changes.

        """

        d = self.declaration
        d.state = state
        if state == "started":
            d.started()
        elif state == "paused":
            d.paused()
        elif state == "resumed":
            d.resumed()
        elif state == "stopped":
            d.stopped()

    def on_back_pressed(self):
        """Fire the `back_pressed` event with a dictionary with a 'handled'
        key when the back hardware button is pressed

        If 'handled' is set to any value that evaluates to True the
        default event implementation will be ignored.

        """
        d = self.declaration
        try:
            return bool(d.on_back_pressed())
        except Exception as e:
            d.app.show_error(f"Error handling back press: {e}")
            #: Must return a boolean or we will cause android to abort
            return True

    def on_configuration_changed(self, config):
        """Handles a screen configuration change."""
        self.width = config["width"]
        self.height = config["height"]
        self.orientation = Activity.ORIENTATIONS[config["orientation"]]
