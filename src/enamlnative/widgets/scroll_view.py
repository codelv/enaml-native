"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Enum, Event, observe
)

from enaml.core.declarative import d_

from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyScrollView(ProxyFrameLayout):
    """ The abstract definition of a proxy ScrollView object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ScrollView)

    def set_orientation(self, orientation):
        raise NotImplementedError

    def set_scroll_by(self, delta):
        raise NotImplementedError

    def set_scroll_to(self, point):
        raise NotImplementedError


class ScrollView(FrameLayout):
    """ A simple control for displaying a ScrollView.

    """

    #: Vertical or horizontal scrollview
    orientation = d_(Enum('vertical', 'horizontal'))

    #: Scroll to position (x, y), 'top', or 'bottom
    scroll_to = d_(Event(object))

    #: Scroll to by delta (x, y)
    scroll_by = d_(Event(tuple))

    #: A reference to the ProxyScrollView object.
    proxy = Typed(ProxyScrollView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('orientation', 'scroll_to', 'scroll_by')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        if change['type'] in ['event', 'update'] and self.proxy_is_active:
            handler = getattr(self.proxy, 'set_' + change['name'], None)
            if handler is not None:
                handler(change['value'])
