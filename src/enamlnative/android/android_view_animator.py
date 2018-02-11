"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
import jnius
from atom.api import Typed, set_default

from enamlnative.widgets.view_animator import ProxyViewAnimator

from .android_frame_layout import AndroidFrameLayout, FrameLayout


class ViewAnimator(FrameLayout):
    __nativeclass__ = set_default('android.widget.ViewAnimator')


class AndroidViewAnimator(AndroidFrameLayout, ProxyViewAnimator):
    """ An Android implementation of an Enaml ProxyViewAnimator.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ViewAnimator)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ViewAnimator(self.get_context())

    # -------------------------------------------------------------------------
    # ProxyViewAnimator API
    # -------------------------------------------------------------------------
    def set_animate_first_view(self, enabled):
        self.widget.setAnimateFirstView(enabled)

    def set_displayed_child(self, index):
        self.widget.setDisplayedChild(index)
