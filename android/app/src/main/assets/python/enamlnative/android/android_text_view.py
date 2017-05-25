'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.text_view import ProxyTextView

from .android_widget import AndroidWidget

_TextView = jnius.autoclass('android.widget.TextView')


class AndroidTextView(AndroidWidget, ProxyTextView):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_TextView)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _TextView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidTextView, self).init_widget()
        d = self.declaration
        self.set_text(d.text)

    #--------------------------------------------------------------------------
    # ProxyLabel API
    #--------------------------------------------------------------------------
    def set_text(self, text):
        """ Set the text in thae widget.

        """
        self.widget.setText(text,0,len(text))
