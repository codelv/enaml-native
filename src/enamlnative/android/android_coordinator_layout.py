"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Sept 18, 2017

@author: jrm
"""
from atom.api import Typed
from enamlnative.widgets.coordinator_layout import ProxyCoordinatorLayout
from .android_frame_layout import AndroidFrameLayout, FrameLayout


class CoordinatorLayout(FrameLayout):
    __nativeclass__ = "androidx.coordinatorlayout.widget.CoordinatorLayout"


class AndroidCoordinatorLayout(AndroidFrameLayout, ProxyCoordinatorLayout):
    """An Android implementation of an Enaml ProxyCoordinatorLayout."""

    #: A reference to the widget created by the proxy.
    widget = Typed(CoordinatorLayout)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = CoordinatorLayout(self.get_context(), None, d.style)
