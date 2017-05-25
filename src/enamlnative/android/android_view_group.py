#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.view_group import ProxyViewGroup

from .android_widget import AndroidWidget

_ViewGroup = jnius.autoclass('android.view.ViewGroup')

class AndroidViewGroup(AndroidWidget, ProxyViewGroup):
    """ An Android implementation of an Enaml ProxyViewGroup.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_ViewGroup)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _ViewGroup(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidViewGroup, self).init_widget()
        d = self.declaration

    #--------------------------------------------------------------------------
    # ProxyViewGroup API
    #--------------------------------------------------------------------------

