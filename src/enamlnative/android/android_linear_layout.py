"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Typed, set_default
from enamlnative.widgets.linear_layout import ProxyLinearLayout
from .android_view_group import AndroidViewGroup, MarginLayoutParams, ViewGroup
from .bridge import JavaField, JavaMethod


class LinearLayout(ViewGroup):
    __nativeclass__ = "android.widget.LinearLayout"
    setOrientation = JavaMethod(int)
    setGravity = JavaMethod(int)


class LinearLayoutParams(MarginLayoutParams):
    __nativeclass__ = "android.widget.LinearLayout$LayoutParams"
    gravity = JavaField(int)
    weight = JavaField(int)


class AndroidLinearLayout(AndroidViewGroup, ProxyLinearLayout):
    """An Android implementation of an Enaml ProxyLinearLayout."""

    #: A reference to the widget created by the proxy.
    widget = Typed(LinearLayout)

    #: Use LinearLayout params
    layout_param_type = set_default(LinearLayoutParams)  # type: ignore

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = LinearLayout(self.get_context(), None, d.style)

    # -------------------------------------------------------------------------
    # ProxyLinearLayout API
    # -------------------------------------------------------------------------
    def set_orientation(self, orientation):
        """Set the text in the widget."""
        self.widget.setOrientation(0 if orientation == "horizontal" else 1)

    def create_layout_params(self, child, layout):
        params = super().create_layout_params(child, layout)
        if "gravity" in layout:
            params.gravity = layout["gravity"]
        return params
