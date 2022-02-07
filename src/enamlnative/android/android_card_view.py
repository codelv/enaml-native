"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on June 7, 2017

@author: jrm
"""
from atom.api import Typed

from enamlnative.widgets.card_view import ProxyCardView

from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaMethod


class CardView(FrameLayout):
    package = "androidx.cardview.widget"
    __nativeclass__ = f"{package}.CardView"
    setCardBackgroundColor = JavaMethod("android.graphics.Color")
    setCardElevation = JavaMethod("float")
    setContentPadding = JavaMethod("int", "int", "int", "int")
    setMaxCardElevation = JavaMethod("float")
    setPreventCornerOverlap = JavaMethod("boolean")
    setRadius = JavaMethod("float")
    setUseCompatPadding = JavaMethod("boolean")


class AndroidCardView(AndroidFrameLayout, ProxyCardView):
    """An Android implementation of an Enaml ProxyCardView."""

    #: A reference to the widget created by the proxy.
    widget = Typed(CardView)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = CardView(self.get_context(), None, d.style)

    # -------------------------------------------------------------------------
    # ProxyCardView API
    # -------------------------------------------------------------------------
    def set_elevation(self, elevation):
        self.widget.setCardElevation(elevation)

    def set_radius(self, radius):
        self.widget.setRadius(radius)

    def set_content_padding(self, padding):
        dp = self.dp
        l, t, r, b = padding
        self.widget.setContentPadding(
            int(l * dp), int(t * dp), int(r * dp), int(b * dp)
        )
