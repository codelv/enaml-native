"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.button import ProxyButton

from .android_text_view import AndroidTextView, TextView


class Button(TextView):
    __nativeclass__ = set_default('android.widget.Button')
    __signature__ = set_default(('android.content.Context',
                                 'android.util.AttributeSet', 'int'))
    STYLES = {
        '': 0x01010048,
        'borderless': 0x0101032b,
        'inset': 0x0101004a,
        'small': 0x01010049,
    }


class AndroidButton(AndroidTextView, ProxyButton):
    """ An Android implementation of an Enaml ProxyButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Button)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        d = self.declaration
        style = Button.STYLES[d.style]
        self.widget = Button(self.get_context(), None, style)

    # -------------------------------------------------------------------------
    # ProxyButton API
    # -------------------------------------------------------------------------
    def set_style(self, style):
        pass