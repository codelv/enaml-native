#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.radio_group import ProxyRadioGroup

from .android_linear_layout import AndroidLinearLayout

_RadioGroup = jnius.autoclass('android.widget.RadioGroup')


class AndroidRadioGroup(AndroidLinearLayout, ProxyRadioGroup):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_RadioGroup)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _RadioGroup(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidRadioGroup, self).init_widget()
        d = self.declaration