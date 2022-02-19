"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed
from enamlnative.widgets.button import (
    ProxyButton,
    ProxyFloatingActionButton,
    ProxyImageButton,
)
from .android_image_view import AndroidImageView, ImageView
from .android_text_view import AndroidTextView, TextView
from .bridge import JavaMethod


class Button(TextView):
    __nativeclass__ = "android.widget.Button"
    __signature__ = [
        "android.content.Context",
        "android.util.AttributeSet",
        "android.R",
    ]
    STYLE_NORMAL = 0x01010048
    STYLE_FLAT = 0x0101032B
    STYLES = {
        "": STYLE_NORMAL,
        "borderless": STYLE_FLAT,
        "inset": 0x0101004A,
        "small": 0x01010049,
    }


class ImageButton(ImageView):
    __nativeclass__ = "android.widget.ImageButton"


class FloatingActionButton(ImageButton):
    package = "com.google.android.material.floatingactionbutton"
    __nativeclass__ = f"{package}.FloatingActionButton"

    SIZE_NORMAL = 0
    SIZE_MINI = 1
    SIZE_AUTO = -1

    SIZES = {"normal": SIZE_NORMAL, "mini": SIZE_MINI, "auto": SIZE_AUTO}

    setSize = JavaMethod("int")
    setRippleColor = JavaMethod("android.graphics.Color")
    setCompatElevation = JavaMethod("float")
    show = JavaMethod()
    hide = JavaMethod()


class AndroidButton(AndroidTextView, ProxyButton):
    """An Android implementation of an Enaml ProxyButton."""

    #: A reference to the widget created by the proxy.
    widget = Typed(Button)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        style = (
            d.style
            if d.style
            else ("@attr/borderlessButtonStyle" if d.flat else "@attr/buttonStyle")
        )
        self.widget = Button(self.get_context(), None, style)

    def init_widget(self):
        super().init_widget()

        w = self.widget
        w.setOnClickListener(w.getId())
        w.onClick.connect(self.on_click)

    # -------------------------------------------------------------------------
    # ProxyButton API
    # -------------------------------------------------------------------------
    def set_flat(self, flat):
        pass


class AndroidImageButton(AndroidImageView, ProxyImageButton):
    """An Android implementation of an Enaml ProxyImageButton."""

    #: A reference to the widget created by the proxy.
    widget = Typed(ImageButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        self.widget = ImageButton(self.get_context())

    def init_widget(self):
        super().init_widget()

        w = self.widget
        w.setOnClickListener(w.getId())
        w.onClick.connect(self.on_click)


class AndroidFloatingActionButton(AndroidImageButton, ProxyFloatingActionButton):
    """An Android implementation of an Enaml ProxyImageButton."""

    #: A reference to the widget created by the proxy.
    widget = Typed(FloatingActionButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = FloatingActionButton(self.get_context(), None, d.style)

    # -------------------------------------------------------------------------
    # ProxyFloatingActionButton API
    # -------------------------------------------------------------------------
    def set_size(self, size):
        self.widget.setSize(FloatingActionButton.SIZES[size])

    def set_elevation(self, elevation):
        self.widget.setCompatElevation(elevation)

    def set_ripple_color(self, color):
        self.widget.setRippleColor(color)

    def set_show(self, show):
        if show:
            self.widget.show()
        else:
            self.widget.hide()
