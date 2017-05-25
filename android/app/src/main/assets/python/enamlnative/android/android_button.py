'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.button import ProxyButton

from .android_text_view import AndroidTextView

_Button = jnius.autoclass('android.widget.Button')


class AndroidButton(AndroidTextView, ProxyButton):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_Button)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _Button(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidButton, self).init_widget()
        d = self.declaration

    #--------------------------------------------------------------------------
    # ProxyLabel API
    #--------------------------------------------------------------------------
