"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Sept 18, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.coordinator_layout import ProxyCoordinatorLayout

from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaMethod


class CoordinatorLayout(FrameLayout):
    __nativeclass__ = set_default(
        'android.support.design.widget.CoordinatorLayout')


class AndroidCoordinatorLayout(AndroidFrameLayout, ProxyCoordinatorLayout):
    """ An Android implementation of an Enaml ProxyCoordinatorLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(CoordinatorLayout)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = CoordinatorLayout(self.get_context())
