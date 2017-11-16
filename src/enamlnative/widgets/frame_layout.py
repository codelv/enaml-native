"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Int, Bool, observe
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup


class ProxyFrameLayout(ProxyViewGroup):
    """ The abstract definition of a proxy FrameLayout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: FrameLayout)

    def set_foreground_gravity(self, gravity):
        raise NotImplementedError

    def set_measure_all_children(self, enabled):
        raise NotImplementedError


class FrameLayout(ViewGroup):
    """ FrameLayout is a view group that displays
        child views in relative positions.

    """
    #: Describes how the child views are positioned.
    #: Defaults to Gravity.START | Gravity.TOP.
    foreground_gravity = d_(Int())

    measure_all_children = d_(Bool())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyFrameLayout)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('foreground_gravity', 'measure_all_children')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(FrameLayout, self)._update_proxy(change)
