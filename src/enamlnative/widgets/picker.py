"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 6, 2017


"""
from atom.api import Bool, ForwardTyped, Int, List, Float, Str, Typed, observe
from enaml.core.declarative import d_
from .linear_layout import LinearLayout, ProxyLinearLayout


class ProxyPicker(ProxyLinearLayout):
    """The abstract definition of a proxy Picker object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Picker)

    def set_max_value(self, value: int):
        raise NotImplementedError

    def set_min_value(self, value: int):
        raise NotImplementedError

    def set_value(self, value: int):
        raise NotImplementedError

    def set_long_press_update_interval(self, interval: int):
        raise NotImplementedError

    def set_wraps(self, wraps: bool):
        raise NotImplementedError

    def set_items(self, items: list[str]):
        raise NotImplementedError

    def set_text_color(self, color: str):
        raise NotImplementedError

    def set_text_size(self, size: float):
        raise NotImplementedError

    def set_divider_height(self, height: int):
        raise NotImplementedError


class Picker(LinearLayout):
    """A simple control for displaying a Picker."""

    #: Formatter, hmm?

    #: Sets the max value of the picker
    max_value = d_(Int())

    #: Sets the min value of the picker.
    min_value = d_(Int())

    #: Set the current value or selected index for the picker.
    value = d_(Int())

    #: Items to display
    items = d_(List(str))

    #: Text color
    text_color = d_(Str())

    #: Text size
    text_size = d_(Float(strict=False))

    #: Divider height
    divider_height = d_(Int(1))

    #: Sets the speed at which the numbers be incremented and decremented
    #: when the up and down buttons are long pressed respectively.
    long_press_update_interval = d_(Int())

    #: Sets whether the selector wheel shown during flinging/scrolling
    #: should wrap around
    wraps = d_(Bool(True))

    #: A reference to the proxy object.
    proxy = Typed(ProxyPicker)

    # --------------------------------------------------------------------------
    # Observers
    # --------------------------------------------------------------------------
    @observe(
        "max_value",
        "min_value",
        "value",
        "items",
        "long_press_update_interval",
        "wraps",
        "text_color",
        "text_size",
        "divider_height",
    )
    def _update_proxy(self, change):

        super()._update_proxy(change)
