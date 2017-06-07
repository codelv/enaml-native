'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed, set_default

from enamlnative.widgets.linear_layout import ProxyLinearLayout

from .android_view_group import AndroidViewGroup

Gravity = jnius.autoclass('android.view.Gravity')
LayoutParams = jnius.autoclass('android.view.ViewGroup$LayoutParams')
LinearLayout = jnius.autoclass('android.widget.LinearLayout')
LinearLayoutLayoutParams = jnius.autoclass('android.widget.LinearLayout$LayoutParams')


class AndroidLinearLayout(AndroidViewGroup, ProxyLinearLayout):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(LinearLayout)

    #: Layout params constructor for this layout
    layout_params = set_default(LinearLayoutLayoutParams)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

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

    #--------------------------------------------------------------------------
    # ProxyLinearLayout API
    #--------------------------------------------------------------------------
    def set_orientation(self, orientation):
        """ Set the text in the widget.

        """
        self.widget.setOrientation(0 if orientation=='horizontal' else 1)

    def set_gravity(self, gravity):
        g = getattr(Gravity,gravity.upper())
        self.widget.setGravity(g)
