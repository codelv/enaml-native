"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 22, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Bool, Int, Event, observe
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup


class ProxySwipeRefreshLayout(ProxyViewGroup):
    """ The abstract definition of a proxy SwipeRefreshLayout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: SwipeRefreshLayout)

    def set_indicator_background_color(self, color):
        raise NotImplementedError

    def set_indicator_color(self, color):
        raise NotImplementedError

    def set_trigger_distance(self, distance):
        raise NotImplementedError

    def set_refreshed(self, refresh):
        raise NotImplementedError


class SwipeRefreshLayout(ViewGroup):
    """ SwipeRefreshLayout is a view group that displays
        child views in relative positions.

    """
    #: Enabled
    enabled = d_(Bool(True))

    #: Must be a
    indicator_color = d_(Unicode())

    #: Must be a
    indicator_background_color = d_(Unicode())

    #: Set the distance to trigger a sync in dips
    trigger_distance = d_(Int())

    #: Triggered when the user swipes
    refreshed = d_(Event())

    #: A reference to the proxy object.
    proxy = Typed(ProxySwipeRefreshLayout)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('enabled', 'indicator_color', 'indicator_background_color',
             'trigger_distance', 'refeshed')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        if change['type'] == 'event':
            self.proxy.set_refreshed(True)
        else:
            super(SwipeRefreshLayout, self)._update_proxy(change)
