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

from .android_view import OnClickListener
from .android_text_view import AndroidTextView

Button = jnius.autoclass('android.widget.Button')


class AndroidButton(AndroidTextView, ProxyButton):
    """ An Android implementation of an Enaml ProxyButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Button)

    #: Save reference to the on click listener
    click_listener = Typed(OnClickListener)

    #  --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = Button(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidButton, self).init_widget()
        self.click_listener = OnClickListener(self)
        self.widget.setOnClickListener(self.click_listener)

    def on_click(self, view):
        """ Trigger the click

        """
        d = self.declaration
        d.clicked()

    # --------------------------------------------------------------------------
    # ProxyButton API
    # --------------------------------------------------------------------------
