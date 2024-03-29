"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Enum, ForwardTyped, Typed
from enaml.core.declarative import d_, observe
from .view_group import ProxyViewGroup, ViewGroup


class ProxyLinearLayout(ProxyViewGroup):
    """The abstract definition of a proxy Label object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: LinearLayout)

    def set_orientation(self, orientation):
        raise NotImplementedError


class LinearLayout(ViewGroup):
    """A simple control for displaying read-only text."""

    #: Should the layout be a column or a row.
    orientation = d_(Enum("horizontal", "vertical"))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyLinearLayout)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("orientation")
    def _update_proxy(self, change):

        super()._update_proxy(change)
