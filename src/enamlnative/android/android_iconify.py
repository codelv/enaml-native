"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed
from enamlnative.widgets.iconify import (
    ProxyIcon,
    ProxyIconButton,
    ProxyIconToggleButton,
)
from .android_button import AndroidButton, Button
from .android_text_view import AndroidTextView, TextView
from .android_toggle_button import AndroidToggleButton, ToggleButton
from .bridge import JavaBridgeObject


class IconDrawable(JavaBridgeObject):
    __nativeclass__ = "com.joanzapata.iconify.IconDrawable"
    __signature__ = ["android.content.Context", "java.lang.String"]


class Icon(TextView):
    __nativeclass__ = "com.joanzapata.iconify.widget.IconTextView"


class IconButton(Button):
    __nativeclass__ = "com.joanzapata.iconify.widget.IconButton"


class IconToggleButton(ToggleButton):
    __nativeclass__ = "com.joanzapata.iconify.widget.IconToggleButton"


class AndroidIcon(AndroidTextView, ProxyIcon):
    """An Android implementation of an Enaml ProxyIcon."""

    #: A reference to the widget created by the proxy.
    widget = Typed(Icon)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = Icon(self.get_context(), None, d.style)


class AndroidIconButton(AndroidButton, ProxyIconButton):
    """An Android implementation of an Enaml ProxyIconButton."""

    #: A reference to the widget created by the proxy.
    widget = Typed(IconButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        style = (
            d.style
            if d.style
            else ("@attr/borderlessButtonStyle" if d.flat else "@attr/buttonStyle")
        )
        self.widget = IconButton(self.get_context(), None, style)


class AndroidIconToggleButton(AndroidToggleButton, ProxyIconToggleButton):
    """An Android implementation of an Enaml ProxyIconToggleButton."""

    #: A reference to the widget created by the proxy.
    widget = Typed(IconToggleButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        self.widget = IconToggleButton(self.get_context())
