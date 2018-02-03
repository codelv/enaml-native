"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on June 7, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.toggle_button import ProxyToggleButton

from .android_compound_button import AndroidCompoundButton, CompoundButton
from .bridge import JavaMethod


class ToggleButton(CompoundButton):
    __nativeclass__ = set_default('android.widget.ToggleButton')
    setTextOff = JavaMethod('java.lang.CharSequence')
    setTextOn = JavaMethod('java.lang.CharSequence')


class AndroidToggleButton(AndroidCompoundButton, ProxyToggleButton):
    """ An Android implementation of an Enaml ProxyToggleButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ToggleButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ToggleButton(self.get_context())

    # -------------------------------------------------------------------------
    # ProxyToggleButton API
    # -------------------------------------------------------------------------
    def set_text_off(self, text):
        self.widget.setTextOff(text)

    def set_text_on(self, text):
        self.widget.setTextOn(text)
