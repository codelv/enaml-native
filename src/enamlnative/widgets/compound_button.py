"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Bool, ForwardTyped, Typed, observe
from enaml.core.declarative import d_
from .button import Button, ProxyButton


class ProxyCompoundButton(ProxyButton):
    """The abstract definition of a proxy Label object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: CompoundButton)

    def set_checked(self, checked):
        raise NotImplementedError


class CompoundButton(Button):
    """A simple control for displaying read-only text."""

    #: Button is checked
    checked = d_(Bool())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyCompoundButton)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("checked")
    def _update_proxy(self, change):

        super()._update_proxy(change)
