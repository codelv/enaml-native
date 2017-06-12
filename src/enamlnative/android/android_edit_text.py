'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.edit_text import ProxyEditText

from .android_text_view import AndroidTextView, TextWatcher

String = jnius.autoclass('java.lang.String')
EditText = jnius.autoclass('android.widget.EditText')
BufferType = jnius.autoclass('android.widget.TextView$BufferType')

class AndroidEditText(AndroidTextView, ProxyEditText):
    """ An Android implementation of an Enaml ProxyEditText.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(EditText)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = EditText(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidEditText, self).init_widget()
        d = self.declaration
        if d.selection:
            self.set_selection(d.selection)

        self.watcher = TextWatcher(self)
        self.widget.addTextChangedListener(self.watcher)

    # --------------------------------------------------------------------------
    # TextWatcher API
    # --------------------------------------------------------------------------
    def after_text_changed(self, e):
        pass

    def before_text_changed(self, text, start, before, count):
        pass

    def on_text_changed(self, text, start, before, count):
        d = self.declaration
        with self.suppress_notifications():
            d.text = text

    # --------------------------------------------------------------------------
    # ProxyEditText API
    # --------------------------------------------------------------------------
    def set_selection(self, selection):
        self.widget.setSelection(*selection)

    def set_text(self, text):
        """ Set text and keep the state of the cursor

        """
        self.widget.setTextKeepState(String(text), BufferType.NORMAL)

