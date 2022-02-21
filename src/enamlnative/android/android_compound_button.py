"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed
from enamlnative.widgets.compound_button import ProxyCompoundButton
from .android_button import AndroidButton, Button
from .bridge import JavaCallback, JavaMethod


class CompoundButton(Button):
    __nativeclass__ = "android.widget.CompoundButton"
    setChecked = JavaMethod(bool)
    setOnCheckedChangeListener = JavaMethod(
        "android.widget.CompoundButton$OnCheckedChangeListener"
    )
    onCheckedChanged = JavaCallback("android.widget.CompoundButton", bool)


class AndroidCompoundButton(AndroidButton, ProxyCompoundButton):
    """An Android implementation of an Enaml ProxyCompoundButton."""

    #: A reference to the widget created by the proxy.
    widget = Typed(CompoundButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        raise NotImplementedError

    def init_widget(self):
        """Initialize the underlying widget."""
        super().init_widget()
        w = self.widget
        w.setOnCheckedChangeListener(w.getId())
        w.onCheckedChanged.connect(self.on_checked)

    def on_checked(self, view, checked):
        d = self.declaration
        with self.widget.setChecked.suppressed():
            d.checked = checked

    # -------------------------------------------------------------------------
    # ProxyLabel API
    # -------------------------------------------------------------------------
    def set_checked(self, checked):
        self.widget.setChecked(checked)
