"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Value, Bool, Int, List, observe
)

from enaml.core.declarative import d_
from enaml.widgets.toolkit_object import ToolkitObject, ProxyToolkitObject
from .view_group import ViewGroup, ProxyViewGroup


class ProxyListView(ProxyViewGroup):
    """ The abstract definition of a proxy ListView object.

    """
    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: ListView)

    def set_items(self, items):
        raise NotImplementedError

    def set_divider_height(self, height):
        raise NotImplementedError

    def set_header_dividers(self, enabled):
        raise NotImplementedError

    def set_footer_dividers(self, enabled):
        raise NotImplementedError

    def set_items_can_focus(self, enabled):
        raise NotImplementedError

    def set_selected(self, index):
        raise NotImplementedError


class ProxyListItem(ProxyToolkitObject):
    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: ListItem)


class ListView(ViewGroup):
    """ A widget for displaying a large scrollable list of items.

    """

    #: List of items to display
    items = d_(List())

    #: Number of visible items
    visible_count = d_(Int(10), writable=False)

    #: Current index within the list
    current_index = d_(Int(), writable=False)

    #: Sets the height of the divider that will be drawn between each item
    #:  in the list.
    divider_height = d_(Int(-1))

    #: Enables or disables the drawing of the divider for header views.
    header_dividers = d_(Bool())

    #: Enables or disables the drawing of the divider for footer views.
    footer_dividers = d_(Bool())

    #: Indicates that the views created by the ListAdapter can contain
    #: focusable items.
    items_can_focus = d_(Bool())

    #: Sets the currently selected item.
    selected = d_(Int(-1))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyListView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('items', 'divider_height', 'header_dividers', 'footer_dividers',
             'items_can_focus',  'selected')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ListView, self)._update_proxy(change)


class ListItem(ToolkitObject):
    """ A holder for a View within a ListItem.

    """

    #: The item this view should render
    item = d_(Value(), writable=False)

    #: The position of this item within the ListView
    index = d_(Int(), writable=False)

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyListItem)
