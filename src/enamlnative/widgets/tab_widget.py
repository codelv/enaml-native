"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Int, Bool, Enum, observe
)

from enaml.core.declarative import d_

from .linear_layout import LinearLayout, ProxyLinearLayout


class ProxyTabWidget(ProxyLinearLayout):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: TabWidget)

    def set_enabled(self, enabled):
        raise NotImplementedError

    def set_current_tab(self, index):
        raise NotImplementedError

    def set_strip_enabled(self, enabled):
        raise NotImplementedError


class TabWidget(LinearLayout):
    """ A tab

    """
    #: Set the enabled state of this view.
    enabled = d_(Bool(True))

    #: Sets the currently selected tab
    current_tab = d_(Int(0))

    #: Sets the currently selected minute.
    strip_enabled = d_(Bool(True))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyTabWidget)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('enabled', 'current_tab', 'strip_enabled')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(TabWidget, self)._update_proxy(change)
