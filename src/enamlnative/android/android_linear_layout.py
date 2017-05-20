#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.linear_layout import ProxyLinearLayout

from .android_widget import AndroidWidget

_LinearLayout = jnius.autoclass('android.widget.LinearLayout')

class AndroidLinearLayout(AndroidWidget, ProxyLinearLayout):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_LinearLayout)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _LinearLayout(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidLinearLayout, self).init_widget()
        d = self.declaration
        self.set_orientation(d.orientation)

    #--------------------------------------------------------------------------
    # ProxyLinearLayout API
    #--------------------------------------------------------------------------
    def set_orientation(self, orientation):
        """ Set the text in the widget.

        """
        self.widget.setOrientation(0 if orientation=='horizontal' else 1)
