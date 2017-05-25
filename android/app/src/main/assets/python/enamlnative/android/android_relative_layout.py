#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.relative_layout import ProxyRelativeLayout

from .android_widget import AndroidWidget

_RelativeLayout = jnius.autoclass('android.widget.RelativeLayout')

class AndroidRelativeLayout(AndroidWidget, ProxyRelativeLayout):
    """ An Android implementation of an Enaml ProxyRelativeLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_RelativeLayout)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _RelativeLayout(self.get_context())

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

    #--------------------------------------------------------------------------
    # ProxyRelativeLayout API
    #--------------------------------------------------------------------------
    def set_gravity(self, gravity):
        self.widget.setGravity(gravity)

    def set_horizontal_gravity(self, gravity):
        self.widget.setHorizontalGravity(gravity)

    def set_vertical_gravity(self, gravity):
        self.widget.setVerticalGravity(gravity)
