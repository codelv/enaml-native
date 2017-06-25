'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed

from enamlnative.widgets.button import ProxyButton

from .android_text_view import AndroidTextView, TextView


class Button(TextView):
    __javaclass__ = 'android.widget.Button'


class AndroidButton(AndroidTextView, ProxyButton):
    """ An Android implementation of an Enaml ProxyButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Button)

    #  --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = Button(self.get_context())

