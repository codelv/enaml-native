"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.radio_button import ProxyRadioButton

from .android_compound_button import AndroidCompoundButton, CompoundButton


class RadioButton(CompoundButton):
    __nativeclass__ = set_default('android.widget.RadioButton')


class AndroidRadioButton(AndroidCompoundButton, ProxyRadioButton):
    """ An Android implementation of an Enaml ProxyRadioButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(RadioButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = RadioButton(self.get_context())
