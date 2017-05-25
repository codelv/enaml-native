#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.scroll_view import ProxyScrollView

from .android_frame_layout import AndroidFrameLayout

_ScrollView = jnius.autoclass('android.widget.ScrollView')

class AndroidScrollView(AndroidFrameLayout, ProxyScrollView):
    """ An Android implementation of an Enaml ProxyFrameLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_ScrollView)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _ScrollView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidScrollView, self).init_widget()
        d = self.declaration

    #--------------------------------------------------------------------------
    # ProxyFrameLayout API
    #--------------------------------------------------------------------------
