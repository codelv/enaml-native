"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

 
"""
from atom.api import ForwardTyped, Instance, Typed, observe
from enaml.core.declarative import d_
from .linear_layout import LinearLayout, ProxyLinearLayout
from .radio_button import RadioButton


class ProxyRadioGroup(ProxyLinearLayout):
    """The abstract definition of a proxy RadioGroup object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: RadioGroup)

    def set_checked(self, checked):
        raise NotImplementedError


class RadioGroup(LinearLayout):
    """A simple control for displaying a RadioGroup."""

    #: Reference to the checked radio button or None
    checked = d_(Instance(RadioButton))

    #: TODO: Should this be more like a Picker/Combo where you pass options

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyRadioGroup)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("checked")
    def _update_proxy(self, change):

        super()._update_proxy(change)
