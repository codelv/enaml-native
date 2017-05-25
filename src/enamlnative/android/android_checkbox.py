#------------------------------------------------------------------------------
# Copyright (c) 2017, Jairus Martin.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.checkbox import ProxyCheckBox

from .android_compound_button import AndroidCompoundButton

_CheckBox = jnius.autoclass('android.widget.CheckBox')


class AndroidCheckBox(AndroidCompoundButton, ProxyCheckBox):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_CheckBox)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _CheckBox(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidCheckBox, self).init_widget()
        d = self.declaration