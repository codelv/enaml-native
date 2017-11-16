"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 10, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Event, observe
)

from enaml.core.declarative import d_

from .linear_layout import LinearLayout, ProxyLinearLayout


class ProxyActionMenuView(ProxyLinearLayout):
    """ The abstract definition of a proxy ActionMenuView object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ActionMenuView)

    def set_overflow_icon(self, icon):
        raise NotImplementedError

    def set_opened(self, opened):
        raise NotImplementedError


class ActionMenuView(LinearLayout):
    """ A simple control for displaying a ActionMenuView.

    """

    #: Reference to the checked radio button or None
    overflow_icon = d_(Unicode())

    #: Show menu
    show = d_(Event())

    #: Hide menu
    hide = d_(Event())

    #: TODO: Should this be more like a Picker/Combo where you pass options

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyActionMenuView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('show', 'hide', 'overflow_icon')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        if change['type'] == 'event' and self.proxy_is_active:
            self.proxy.set_opened(change['name'] == 'show')
        else:
            super(ActionMenuView, self)._update_proxy(change)
