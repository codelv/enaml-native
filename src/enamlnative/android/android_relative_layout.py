"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.relative_layout import ProxyRelativeLayout

from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaMethod


class RelativeLayout(ViewGroup):
    __nativeclass__ = set_default('android.widget.RelativeLayout')
    setGravity = JavaMethod('int')
    setHorizontalGravity = JavaMethod('int')
    setVerticalGravity = JavaMethod('int')


class AndroidRelativeLayout(AndroidViewGroup, ProxyRelativeLayout):
    """ An Android implementation of an Enaml ProxyRelativeLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(RelativeLayout)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = RelativeLayout(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidRelativeLayout, self).init_widget()
        d = self.declaration
        if d.gravity:
            self.set_gravity(d.gravity)
        if d.horizontal_gravity:
            self.set_horizontal_gravity(d.horizontal_gravity)
        if d.vertical_gravity:
            self.set_vertical_gravity(d.vertical_gravity)

    # -------------------------------------------------------------------------
    # ProxyRelativeLayout API
    # -------------------------------------------------------------------------
    def set_gravity(self, gravity):
        self.widget.setGravity(gravity)

    def set_horizontal_gravity(self, gravity):
        self.widget.setHorizontalGravity(gravity)

    def set_vertical_gravity(self, gravity):
        self.widget.setVerticalGravity(gravity)
