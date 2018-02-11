"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Int, Enum, Event, observe, set_default
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup


class ProxyLinearLayout(ProxyViewGroup):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: LinearLayout)

    def set_orientation(self, orientation):
        raise NotImplementedError


class LinearLayout(ViewGroup):
    """ A simple control for displaying read-only text.

    """
    #: Should the layout be a column or a row.
    orientation = d_(Enum('horizontal', 'vertical'))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyLinearLayout)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('orientation')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(LinearLayout, self)._update_proxy(change)
