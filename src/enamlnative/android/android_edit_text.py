"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.edit_text import ProxyEditText

from .android_text_view import AndroidTextView, TextView
from .bridge import JavaMethod


class EditText(TextView):
    __nativeclass__ = set_default('android.widget.EditText')
    setSelection = JavaMethod('int', 'int')
    selectAll = JavaMethod()
    extendSelection = JavaMethod('int')
    setHint = JavaMethod('java.lang.CharSequence')


class AndroidEditText(AndroidTextView, ProxyEditText):
    """ An Android implementation of an Enaml ProxyEditText.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(EditText)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = EditText(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidEditText, self).init_widget()
        d = self.declaration
        if d.selection:
            self.set_selection(d.selection)
        if d.placeholder:
            self.set_placeholder(d.placeholder)

    # -------------------------------------------------------------------------
    # ProxyEditText API
    # -------------------------------------------------------------------------
    def set_selection(self, selection):
        self.widget.setSelection(*selection)

    def set_placeholder(self, placeholder):
        self.widget.setHint(placeholder)


