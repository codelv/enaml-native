"""
Copyright (c) 2017-2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Bool, ContainerList, Enum, ForwardTyped, Int, Typed, Value
from enaml.core.declarative import d_, observe
from enaml.widgets.toolkit_object import ProxyToolkitObject, ToolkitObject
from .view_group import ProxyViewGroup, ViewGroup


class ProxyListView(ProxyViewGroup):
    """The abstract definition of a proxy ListView object."""

    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: ListView)

    def set_items(self, items: list):
        raise NotImplementedError

    def set_span_count(self, count: int):
        raise NotImplementedError

    def set_orientation(self, orientation: str):
        raise NotImplementedError

    def set_arrangement(self, arrangement: str):
        raise NotImplementedError

    def set_selected(self, index: int):
        raise NotImplementedError

    def set_fixed_size(self, fixed_size: bool):
        raise NotImplementedError

    def scroll_to(self, x: int, y: int):
        raise NotImplementedError

    def scroll_to_position(self, position: int):
        raise NotImplementedError


class ProxyListItem(ProxyToolkitObject):
    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: ListItem)


class ListView(ViewGroup):
    """A widget for displaying a large scrollable list of items."""

    #: List of items to display
    items = d_(ContainerList())

    #: use this setting to improve performance if you know that changes
    #: in content do not change the layout size of the RecyclerView
    fixed_size = d_(Bool())

    #: Layout manager to use
    arrangement = d_(Enum("linear", "grid", "staggered"))

    #: Orientation
    orientation = d_(Enum("vertical", "horizontal"))

    #: Span count (only for grid and staggered)
    span_count = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyListView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("items", "arrangement", "orientation", "span_count", "fixed_size")
    def _update_proxy(self, change):

        super()._update_proxy(change)

    def scroll_to(self, x: int, y: int):
        """Scroll to the given x,y coordinates within the list"""
        if proxy := self.proxy:
            proxy.scroll_to(x, y)

    def scroll_to_position(self, position: int):
        """Scroll to the given position in the list"""
        if proxy := self.proxy:
            proxy.scroll_to_position(position)


class ListItem(ToolkitObject):
    """A holder for a View within a ListItem."""

    #: The item this view should render
    item = d_(Value(), writable=False)

    #: The position of this item within the ListView
    index = d_(Int(), writable=False)

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyListItem)
