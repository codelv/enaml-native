"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Enum, Event, ForwardTyped, Typed, observe
from enaml.core.declarative import d_
from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyScrollView(ProxyFrameLayout):
    """The abstract definition of a proxy ScrollView object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ScrollView)

    def set_orientation(self, orientation):
        raise NotImplementedError

    def set_scroll_by(self, delta):
        raise NotImplementedError

    def set_scroll_to(self, point):
        raise NotImplementedError

    def set_scrollbars(self, scrollbars):
        raise NotImplementedError


class ScrollView(FrameLayout):
    """A simple control for displaying a ScrollView."""

    #: Vertical or horizontal scrollview
    orientation = d_(Enum("vertical", "horizontal"))

    #: Scroll to position (x, y), 'top', or 'bottom
    scroll_to = d_(Event(object))

    #: Scroll to by delta (x, y)
    scroll_by = d_(Event(tuple))

    #: Set which scrollbars are enabled
    scrollbars = d_(Enum("both", "vertical", "horizontal", "none"))

    #: A reference to the ProxyScrollView object.
    proxy = Typed(ProxyScrollView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("orientation", "scroll_to", "scroll_by", "scrollbars")
    def _update_proxy(self, change):

        if change["type"] in ["event", "update"] and self.proxy_is_active:
            handler = getattr(self.proxy, f"set_{change['name']}", None)
            if handler is not None:
                handler(change["value"])
