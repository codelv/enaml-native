"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 9, 2018
"""
from atom.api import Typed, set_default
from enamlnative.widgets.surface_view import ProxySurfaceView
from .android_view import AndroidView, View
from .bridge import JavaBridgeObject, JavaCallback, JavaMethod


class SurfaceView(View):
    __nativeclass__ = "android.view.SurfaceView"
    __signature__ = ["android.content.Context"]  # type: ignore
    setSecure = JavaMethod(bool)
    getHolder = JavaMethod(returns="android.view.SurfaceHolder")


class SurfaceHolder(JavaBridgeObject):
    __nativeclass__ = "android.view.SurfaceHolder"
    addCallback = JavaMethod("android.view.SurfaceHolder$Callback")
    removeCallback = JavaMethod("android.view.SurfaceHolder$Callback")
    setKeepScreenOn = JavaMethod(bool)
    setFormat = JavaMethod(int)
    setFixedSize = JavaMethod(int, int)

    #: SurfaceHolder.Callback
    surfaceChanged = JavaCallback("android.view.SurfaceHolder", int, int, int)
    surfaceCreated = JavaCallback("android.view.SurfaceHolder")
    surfaceDestroyed = JavaCallback("android.view.SurfaceHolder")
    surfaceRedrawNeeded = JavaCallback("android.view.SurfaceHolder")
    surfaceRedrawNeededAsync = JavaCallback(
        "android.view.SurfaceHolder", "java.lang.Runnable"
    )


class Surface(JavaBridgeObject):
    __nativeclass__ = "android.view.Surface"
    __signature__ = ["android.graphics.SurfaceTexture"]


class AndroidSurfaceView(AndroidView, ProxySurfaceView):
    """An Android implementation of an Enaml ProxySurfaceView"""

    #: A reference to the widget created by the proxy.
    widget = Typed(SurfaceView)

    #: Default layout params
    default_layout = set_default(  # type: ignore
        {"width": "match_parent", "height": "match_parent"}
    )

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        self.widget = SurfaceView(self.get_context())

    def init_layout(self):
        """Add all child widgets to the view"""
        super().init_layout()

        # Force layout using the default params
        if not self.layout_params:
            self.set_layout({})

    def set_secure(self, secure):
        self.widget.setSecure(secure)
