"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on June 7, 2017
"""
from atom.api import Bool, ForwardTyped, Str, Typed, observe
from enaml.core.declarative import d_
from .compound_button import CompoundButton, ProxyCompoundButton


class ProxySwitch(ProxyCompoundButton):
    """The abstract definition of a proxy Switch object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Switch)

    def set_show_text(self, show):
        raise NotImplementedError

    def set_split_track(self, split):
        raise NotImplementedError

    def set_text_off(self, text):
        raise NotImplementedError

    def set_text_on(self, text):
        raise NotImplementedError


class Switch(CompoundButton):
    """A simple control for displaying a Switch."""

    #: Sets whether the on/off text should be displayed.
    show_text = d_(Bool())

    #: Specifies whether the track should be split by the thumb.
    split_track = d_(Bool())

    #: Sets the text for when the button is not in the checked state.
    text_off = d_(Str())

    #: Sets the text for when the button is in the checked state.
    text_on = d_(Str())

    #: A reference to the ProxySwitch object.
    proxy = Typed(ProxySwitch)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("show_text", "split_track", "text_off", "text_on")
    def _update_proxy(self, change):

        super()._update_proxy(change)
