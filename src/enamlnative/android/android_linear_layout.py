"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.linear_layout import ProxyLinearLayout

from .android_view_group import AndroidViewGroup, ViewGroup, MarginLayoutParams
from .bridge import JavaMethod, JavaField


class LinearLayout(ViewGroup):
    __nativeclass__ = set_default('android.widget.LinearLayout')
    setOrientation = JavaMethod('int')
    setGravity = JavaMethod('int')


class LinearLayoutLayoutParams(MarginLayoutParams):
    __nativeclass__ = set_default('android.widget.LinearLayout$LayoutParams')
    gravity = JavaField('int')
    weight = JavaField('int')


class AndroidLinearLayout(AndroidViewGroup, ProxyLinearLayout):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(LinearLayout)

    layout_param_type = set_default(LinearLayoutLayoutParams)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = LinearLayout(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidLinearLayout, self).init_widget()
        d = self.declaration
        self.set_orientation(d.orientation)
        if d.gravity:
            self.set_gravity(d.gravity)

    # -------------------------------------------------------------------------
    # ProxyLinearLayout API
    # -------------------------------------------------------------------------
    def set_orientation(self, orientation):
        """ Set the text in the widget.

        """
        self.widget.setOrientation(0 if orientation == 'horizontal' else 1)

    def set_gravity(self, gravity):
        self.widget.setGravity(gravity)
