"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Coerced, Enum, ForwardTyped, Int, List, Str, Typed, observe
from enaml.core.declarative import d_
from .view import coerce_gravity
from .view_group import ProxyViewGroup, ViewGroup


class ProxySpinner(ProxyViewGroup):
    """The abstract definition of a proxy Spinner object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Spinner)

    def set_mode(self, mode: str):
        pass

    def set_prompt(self, prompt: str):
        raise NotImplementedError

    def set_selected(self, selected: int):
        raise NotImplementedError

    def set_items(self, items: list):
        raise NotImplementedError

    def set_item_gravity(self, gravity):
        raise NotImplementedError

    def set_drop_down_horizontal_offset(self, offset):
        raise NotImplementedError

    def set_drop_down_vertical_offset(self, offset):
        raise NotImplementedError

    def set_drop_down_width(self, width):
        raise NotImplementedError


class Spinner(ViewGroup):
    """A simple control for displaying read-only text."""

    #: Set the mode
    mode = d_(Enum("dropdown", "dialog"))

    #: Sets the prompt to display when the dialog is shown.
    prompt = d_(Str())

    #: Should the layout be a column or a row.
    selected = d_(Int(0))

    #: View gravity
    items = d_(List())

    #: Gravity setting for positioning the currently selected item.
    item_gravity = d_(Coerced(int, coercer=coerce_gravity))

    #: Set a horizontal offset in pixels for the spinner's popup window
    #: of choices.
    drop_down_horizontal_offset = d_(Int())

    #: Set a vertical offset in pixels for the spinner's popup window
    #: of choices.
    drop_down_vertical_offset = d_(Int())

    #: Set the width of the spinner's popup window of choices in pixels.
    drop_down_width = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxySpinner)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe(
        "mode",
        "prompt",
        "selected",
        "items",
        "item_gravity",
        "drop_down_horizontal_offset",
        "drop_down_vertical_offset",
        "drop_down_width",
    )
    def _update_proxy(self, change):

        super()._update_proxy(change)
