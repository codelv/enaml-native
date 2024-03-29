"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 9, 2018
"""
from atom.api import Bool, Int, Typed, set_default
from enamlnative.widgets.view import ProxyView
from enamlnative.core.bridge import generate_id
from .android_content import Context
from .android_view import AndroidView, View
from .bridge import JavaBridgeObject, JavaCallback, JavaMethod


class SurfaceTexture(JavaBridgeObject):
    __nativeclass__ = "android.graphics.SurfaceTexture"
    setDefaultBufferSize = JavaMethod(int, int)
    available = Bool()
    onSurfaceTextureAvailable = JavaCallback(
        "android.graphics.SurfaceTexture", int, int
    )
    onSurfaceTextureDestroyed = JavaCallback(
        "android.graphics.SurfaceTexture", returns=bool
    )
    onSurfaceTextureChanged = JavaCallback("android.graphics.SurfaceTexture", int, int)
    onSurfaceTextureUpdated = JavaCallback("android.graphics.SurfaceTexture")


class TextureView(View):
    __nativeclass__ = "android.view.TextureView"
    __signature__ = [Context]
    getSurfaceTexture = JavaMethod(returns=SurfaceTexture)
    setTransform = JavaMethod("android.graphics.Matrix")
    setDefaultBufferSize = JavaMethod(int, int)
    setSurfaceTextureListener = JavaMethod(
        "android.view.TextureView$SurfaceTextureListener"
    )


class AndroidTextureView(AndroidView, ProxyView):
    """An Android implementation of an Enaml ProxyTextureView"""

    #: A reference to the widget created by the proxy.
    widget = Typed(TextureView)

    #: A reference to the texture
    texture = Typed(SurfaceTexture)

    #: Texture size
    width = Int()
    height = Int()

    #: Default layout params
    default_layout = set_default({"width": "match_parent", "height": "match_parent"})  # type: ignore

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        self.widget = TextureView(self.get_context())

    def init_widget(self):
        """Initialize the underlying widget."""
        super().__init__()
        w = self.widget

        # Create a new reference because it creates passes a new texture in
        # the callback
        tid = generate_id()
        t = self.texture = SurfaceTexture(__id__=tid)
        w.setSurfaceTextureListener(tid)

        t.onSurfaceTextureAvailable.connect(self.on_surface_texture_available)
        t.onSurfaceTextureDestroyed.connect(self.on_surface_texture_destroyed)
        t.onSurfaceTextureChanged.connect(self.on_surface_texture_changed)
        t.onSurfaceTextureUpdated.connect(self.on_surface_texture_updated)

    def init_layout(self):
        """Add all child widgets to the view"""
        super().init_layout()

        # Force layout using the default params
        if not self.layout_params:
            self.set_layout({})

    # -------------------------------------------------------------------------
    # SurfaceTextureListener API
    # -------------------------------------------------------------------------
    def on_surface_texture_available(self, surface, width, height):
        self.texture.available = True
        self.width = width
        self.height = height

    def on_surface_texture_changed(self, surface, width, height):
        self.width = width
        self.height = height

    def on_surface_texture_updated(self, surface):
        pass

    def on_surface_texture_destroyed(self, surface):
        self.texture.available = False
        return True
