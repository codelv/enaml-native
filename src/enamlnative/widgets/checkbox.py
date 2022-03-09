"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

 
"""
from atom.api import ForwardTyped, Typed
from .compound_button import CompoundButton, ProxyCompoundButton


class ProxyCheckBox(ProxyCompoundButton):
    """The abstract definition of a proxy CheckBox object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: CheckBox)


class CheckBox(CompoundButton):
    """A simple control for displaying a CheckBox."""

    #: A reference to the ProxyCheckBox object.
    proxy = Typed(ProxyCheckBox)
