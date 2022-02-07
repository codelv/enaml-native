"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Mar 13, 2018

@author: jrm
"""
from atom.api import Typed

from enamlnative.widgets.app_bar_layout import ProxyAppBarLayout

from .android_linear_layout import AndroidLinearLayout, LinearLayout
from .bridge import JavaMethod, JavaCallback


class AppBarLayout(LinearLayout):
    package = "com.google.android.material.appbar"

    __nativeclass__ = f"{package}.AppBarLayout"
    __signature__ = ("android.content.Context",)

    addOnOffsetChangedListener = JavaMethod(
        f"{package}.AppBarLayout$OnOffsetChangedListener"
    )
    removeOnOffsetChangedListener = JavaMethod(
        f"{package}.AppBarLayout$OnOffsetChangedListener"
    )

    setExpanded = JavaMethod("boolean")

    onOffsetChanged = JavaCallback(f"{package}.AppBarLayout", "int")


class AndroidAppBarLayout(AndroidLinearLayout, ProxyAppBarLayout):
    """An Android implementation of an Enaml ProxyAppBarLayout."""

    #: A reference to the widget created by the proxy.
    widget = Typed(AppBarLayout)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        self.widget = AppBarLayout(self.get_context())

    def init_widget(self):
        super().init_widget()
        w = self.widget
        w.addOnOffsetChangedListener(w.getId())
        w.onOffsetChanged.connect(self.on_offset_changed)

    def on_offset_changed(self, layout, offset):
        d = self.declaration
        d.vertical_offset = offset

    def set_expanded(self, expanded):
        self.widget.setExpanded(expanded)
