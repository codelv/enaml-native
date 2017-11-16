"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
import jnius
from atom.api import Typed

from enamlnative.widgets.view_animator import ProxyViewAnimator

from .android_frame_layout import AndroidFrameLayout



class AndroidViewAnimator(AndroidFrameLayout, ProxyViewAnimator):
    """ An Android implementation of an Enaml ProxyViewAnimator.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ViewAnimator)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying Android widget.

        """
        self.widget = ViewAnimator(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidViewAnimator, self).init_widget()
        d = self.declaration
        if d.animate_first_view:
            self.set_animate_first_view(d.animate_first_view)
        if d.displayed_child:
            self.set_displayed_child(d.displayed_child)

    # --------------------------------------------------------------------------
    # ProxyViewAnimator API
    # --------------------------------------------------------------------------
    def set_animate_first_view(self, enabled):
        self.widget.setAnimateFirstView(enabled)

    def set_displayed_child(self, index):
        self.widget.setDisplayedChild(index)
