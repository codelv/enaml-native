"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import ForwardTyped, Int, Typed
from enaml.core.declarative import d_, observe
from .view_group import ProxyViewGroup, ViewGroup


class ProxyRelativeLayout(ProxyViewGroup):
    """The abstract definition of a proxy relative layout object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: RelativeLayout)

    def set_gravity(self, gravity: int):
        raise NotImplementedError

    def set_horizontal_gravity(self, gravity: int):
        raise NotImplementedError

    def set_vertical_gravity(self, gravity: int):
        raise NotImplementedError


class RelativeLayout(ViewGroup):
    """RelativeLayout is a view group that displays
    child views in relative positions.

    """

    #: Describes how the child views are positioned.
    #: Defaults to Gravity.START | Gravity.TOP.
    gravity = d_(Int())

    #:
    horizontal_gravity = d_(Int())

    #:
    vertical_gravity = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyRelativeLayout)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("gravity", "horizontal_gravity", "vertical_gravity")
    def _update_proxy(self, change):

        super()._update_proxy(change)
