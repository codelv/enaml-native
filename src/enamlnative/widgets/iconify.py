"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 8, 2017

 
"""
from atom.api import ForwardTyped, Typed
from .button import Button, ProxyButton
from .text_view import ProxyTextView, TextView
from .toggle_button import ProxyToggleButton, ToggleButton


class ProxyIcon(ProxyTextView):
    """The abstract definition of a proxy Icon object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Icon)


class ProxyIconButton(ProxyButton):
    #: A reference to the IconButton declaration.
    declaration = ForwardTyped(lambda: IconButton)


class ProxyIconToggleButton(ProxyToggleButton):
    #: A reference to the IconToggleButton declaration.
    declaration = ForwardTyped(lambda: IconToggleButton)


class Icon(TextView):
    """A simple control for displaying a Icon."""

    #: A reference to the ProxyIcon object.
    proxy = Typed(ProxyIcon)


class IconButton(Button):
    #: A reference to the ProxyIconButton object.
    proxy = Typed(ProxyIconButton)


class IconToggleButton(ToggleButton):
    #: A reference to the ProxyIconToggleButton object.
    proxy = Typed(ProxyIconToggleButton)
