"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import ForwardTyped, Str, Typed
from enaml.core.declarative import d_
from .view_switcher import ProxyViewSwitcher, ViewSwitcher


class ProxyTextSwitcher(ProxyViewSwitcher):
    """The abstract definition of a proxy TextSwitcher object."""

    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: TextSwitcher)


class TextSwitcher(ViewSwitcher):
    """A simple control for a TextSwitcher."""

    #: Sets the text of the text view that is currently showing.
    current_text = d_(Str())

    #: Sets the text of the next view and switches to the next view.
    text = d_(Str())

    #: A reference to the ProxyTextSwitcher object.
    proxy = Typed(ProxyTextSwitcher)
