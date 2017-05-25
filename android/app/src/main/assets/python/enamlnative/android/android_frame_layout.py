'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.frame_layout import ProxyFrameLayout

from .android_widget import AndroidWidget

_FrameLayout = jnius.autoclass('android.widget.FrameLayout')

class AndroidFrameLayout(AndroidWidget, ProxyFrameLayout):
    """ An Android implementation of an Enaml ProxyFrameLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_FrameLayout)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _FrameLayout(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidFrameLayout, self).init_widget()
        d = self.declaration
        if d.foreground_gravity:
            self.set_foreground_gravity(d.foreground_gravity)
        self.set_measure_all_children(d.measure_all_children)

    #--------------------------------------------------------------------------
    # ProxyFrameLayout API
    #--------------------------------------------------------------------------
    def set_foreground_gravity(self, gravity):
        self.widget.setForegroundGravity(gravity)

    def set_measure_all_children(self, enabled):
        self.widget.setMeasureAllChildren(enabled)
