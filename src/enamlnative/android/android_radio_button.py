"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Typed
from enamlnative.widgets.radio_button import ProxyRadioButton
from .android_compound_button import AndroidCompoundButton, CompoundButton


class RadioButton(CompoundButton):
    __nativeclass__ = "android.widget.RadioButton"


class AndroidRadioButton(AndroidCompoundButton, ProxyRadioButton):
    """An Android implementation of an Enaml ProxyRadioButton."""

    #: A reference to the widget created by the proxy.
    widget = Typed(RadioButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = RadioButton(
            self.get_context(), None, d.style or "@attr/radioButtonStyle"
        )
