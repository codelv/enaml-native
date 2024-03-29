"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Typed, set_default
from enamlnative.widgets.frame_layout import ProxyFrameLayout
from .android_view_group import AndroidViewGroup, MarginLayoutParams, ViewGroup
from .bridge import JavaField, JavaMethod


class FrameLayout(ViewGroup):
    __nativeclass__ = "android.widget.FrameLayout"
    setForegroundGravity = JavaMethod(int)
    setMeasureAllChildren = JavaMethod(bool)


class FrameLayoutParams(MarginLayoutParams):
    """Update the child widget with the given params"""

    __nativeclass__ = "android.widget.FrameLayout$LayoutParams"
    gravity = JavaField(int)


class AndroidFrameLayout(AndroidViewGroup, ProxyFrameLayout):
    """An Android implementation of an Enaml ProxyFrameLayout."""

    #: A reference to the widget created by the proxy.
    widget = Typed(FrameLayout)

    #: Update default
    layout_param_type = set_default(FrameLayoutParams)  # type: ignore

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = FrameLayout(self.get_context(), None, d.style)

    # -------------------------------------------------------------------------
    # ProxyFrameLayout API
    # -------------------------------------------------------------------------
    def set_foreground_gravity(self, gravity):
        self.widget.setForegroundGravity(gravity)

    def create_layout_params(self, child, layout):
        params = super().create_layout_params(child, layout)
        if "gravity" in layout:
            params.gravity = layout["gravity"]
        return params
