"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Enum, ForwardTyped, Str, Tuple, Typed, observe, set_default
from enaml.core.declarative import d_
from .text_view import ProxyTextView, TextView


class ProxyEditText(ProxyTextView):
    """The abstract definition of a proxy EditText object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: EditText)

    def set_selection(self, selection):
        raise NotImplementedError

    def set_style(self, style):
        raise NotImplementedError

    def set_placeholder(self, placeholder):
        raise NotImplementedError


class EditText(TextView):
    """A simple control for displaying read-only text."""

    #: Text selection
    selection = d_(Tuple(int))

    #: Make editable by default
    input_type = set_default("text")

    #: Placeholder text
    placeholder = d_(Str())

    #: Style (iOS)
    style = d_(Enum("", "line", "bezel", "rounded_rect"))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyEditText)

    @observe("selection", "placeholder", "style")
    def _update_proxy(self, change):

        super()._update_proxy(change)
