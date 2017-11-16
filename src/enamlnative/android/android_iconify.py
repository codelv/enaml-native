"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.iconify import ProxyIcon, ProxyIconButton, ProxyIconToggleButton

from .android_text_view import AndroidTextView, TextView
from .android_button import AndroidButton, Button
from .android_toggle_button import AndroidToggleButton, ToggleButton


class Icon(TextView):
    __nativeclass__ = set_default('com.joanzapata.iconify.widget.IconTextView')


class IconButton(Button):
    __nativeclass__ = set_default('com.joanzapata.iconify.widget.IconButton')


class IconToggleButton(ToggleButton):
    __nativeclass__ = set_default('com.joanzapata.iconify.widget.IconToggleButton')


class AndroidIcon(AndroidTextView, ProxyIcon):
    """ An Android implementation of an Enaml ProxyIcon.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Icon)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = Icon(self.get_context())


class AndroidIconButton(AndroidButton, ProxyIconButton):
    """ An Android implementation of an Enaml ProxyIconButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(IconButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        d = self.declaration
        style = Button.STYLES[d.style]
        self.widget = IconButton(self.get_context(), None, style)


class AndroidIconToggleButton(AndroidToggleButton, ProxyIconToggleButton):
    """ An Android implementation of an Enaml ProxyIconToggleButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(IconToggleButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = IconToggleButton(self.get_context())
