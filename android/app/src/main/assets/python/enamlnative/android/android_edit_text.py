#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.edit_text import ProxyEditText

from .android_text_view import AndroidTextView

_EditText = jnius.autoclass('android.widget.EditText')


class AndroidEditText(AndroidTextView, ProxyEditText):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_EditText)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _EditText(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidEditText, self).init_widget()
        d = self.declaration
        if d.selection:
            self.set_selection(d.selection)

    #--------------------------------------------------------------------------
    # ProxyEditText API
    #--------------------------------------------------------------------------
    def set_selection(self, selection):
        self.widget.setSelection(*selection)

