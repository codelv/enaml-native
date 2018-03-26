"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, Property, Dict, set_default, observe

from enamlnative.widgets.list_view import ProxyListView, ProxyListItem

from .android_toolkit_object import AndroidToolkitObject
from .android_adapter import AndroidAdapterView, AdapterView
from .bridge import JavaBridgeObject, JavaCallback, JavaMethod, encode


class AbsListView(AdapterView):
    __nativeclass__ = set_default('android.widget.AbsListView')
    pointToPosition = JavaMethod('int', 'int')
    setAdapter = JavaMethod('android.widget.ListAdapter')


class ListView(AbsListView):
    __nativeclass__ = set_default('android.widget.ListView')
    setDividerHeight = JavaMethod('int')
    setFooterDividersEnabled = JavaMethod('boolean')
    setHeaderDividersEnabled = JavaMethod('boolean')
    setItemsCanFocus = JavaMethod('boolean')
    setSelection = JavaMethod('int')
    smoothScrollByOffset = JavaMethod('int')
    smoothScrollToPosition = JavaMethod('int')

    # OnScrollListener API
    setOnScrollListener = JavaMethod(
        'android.widget.AbsListView$OnScrollListener')
    onScroll = JavaCallback('android.widget.AbsListView', 'int', 'int', 'int')
    onScrollStateChanged = JavaCallback('android.widget.AbsListView', 'int')


class BridgedListAdapter(JavaBridgeObject):
    """ An adapter that implements a recycleview pattern.

    """
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedListAdapter')
    setListView = JavaMethod('android.widget.ListView',
                             'com.codelv.enamlnative.adapters.'
                             'BridgedListAdapter$BridgedListAdapterListener')
    setCount = JavaMethod('int')
    setRecycleViews = JavaMethod('[Landroid.view.View;')
    clearRecycleViews = JavaMethod()

    #: BridgedListAdapterListener API
    onRecycleView = JavaCallback('int', 'int', 'int')
    onVisibleCountChanged = JavaCallback('int','int')
    onScrollStateChanged = JavaCallback('android.widget.AbsListView','int')


class AndroidListView(AndroidAdapterView, ProxyListView):
    """ An Android implementation of an Enaml ProxyListView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ListView)

    #: Reference to adapter
    adapter = Typed(BridgedListAdapter)

    def _get_list_items(self):
        return [c for c in self.children() if isinstance(c, AndroidListItem)]

    #: List items
    list_items = Property(lambda self: self._get_list_items(), cached=True)

    #: List mapping from index to view
    item_mapping = Dict()

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ListView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidListView, self).init_widget()
        d = self.declaration

        if d.divider_height >= 0:
            self.set_divider_height(d.divider_height)
        if d.header_dividers:
            self.set_header_dividers(d.header_dividers)
        if d.footer_dividers:
            self.set_footer_dividers(d.footer_dividers)
        if d.items_can_focus:
            self.set_items_can_focus(d.items_can_focus)

        w = self.widget
        w.setOnItemClickListener(w.getId())
        w.setOnItemLongClickListener(w.getId())
        w.onItemClick.connect(self.on_item_click)
        w.onItemLongClick.connect(self.on_item_long_click)
        #self.widget.setOnScrollListener(self.widget.getId())
        #self.widget.onScroll.connect(self.on_scroll)

        #: Selection listener
        #self.widget.setOnItemSelectedListener(self.widget.getId())
        #self.widget.onItemSelected.connect(self.on_item_selected)
        #self.widget.onNothingSelected.connect(self.on_nothing_selected)

    def get_declared_items(self):
        """ Override to do it manually
        
        """
        for k, v in super(AndroidListView, self).get_declared_items():
            if k == 'layout':
                yield k, v
                break

    def init_layout(self):
        """ Initialize the underlying widget.

        """
        super(AndroidListView, self).init_layout()
        d = self.declaration
        w = self.widget

        # Prepare adapter
        adapter = self.adapter = BridgedListAdapter()

        # I'm sure this will make someone upset haha
        adapter.setListView(w, adapter.getId())
        adapter.onRecycleView.connect(self.on_recycle_view)
        adapter.onVisibleCountChanged.connect(self.on_visible_count_changed)
        adapter.onScrollStateChanged.connect(self.on_scroll_state_changed)

        if d.items:
            self.set_items(d.items)

        w.setAdapter(adapter)
        if d.selected >= 0:
            self.set_selected(d.selected)

    # -------------------------------------------------------------------------
    # BridgedListAdapterListener API
    # -------------------------------------------------------------------------
    def on_recycle_view(self, index, position):
        """ Update the item the view at the given index should display
        """
        item = self.list_items[index]
        self.item_mapping[position] = item
        item.recycle_view(position)

    def on_visible_count_changed(self, count, total):
        d = self.declaration
        d.visible_count = count

    def on_scroll_state_changed(self, view, state):
        pass

    # -------------------------------------------------------------------------
    # ListAdapter API
    # -------------------------------------------------------------------------
    def on_item_click(self, adapter, view, index, row_id):
        # Get the ListItem at this index
        item = self.item_mapping.get(index)
        if item:
            item.on_click()

    def on_item_long_click(self, adapter, view, index, row_id):
        # Get the ListItem at this index
        item = self.item_mapping.get(index)
        if item:
            item.on_long_click()

    # -------------------------------------------------------------------------
    # ProxyListView API
    # -------------------------------------------------------------------------
    #@observe('declaration.visible_count')
    def refresh_views(self, change=None):
        """ Set the views that the adapter will cycle through. """
        adapter = self.adapter

        # Set initial ListItem state
        item_mapping = self.item_mapping
        for i, item in enumerate(self.list_items):
            item_mapping[i] = item
            item.recycle_view(i)

        if adapter:
           adapter.clearRecycleViews()
           adapter.setRecycleViews(
                [encode(li.get_view()) for li in self.list_items])

    def set_items(self, items):
        self.adapter.setCount(len(items))
        self.refresh_views()

    def set_divider_height(self, height):
        self.widget.setDividerHeight(height)

    def set_header_dividers(self, enabled):
        self.widget.setHeaderDividersEnabled(enabled)

    def set_footer_dividers(self, enabled):
        self.widget.setFooterDividersEnabled(enabled)

    def set_items_can_focus(self, enabled):
        self.widget.setItemsCanFocus(enabled)

    def set_selected(self, index):
        self.widget.setSelection(index)


class AndroidListItem(AndroidToolkitObject, ProxyListItem):

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ The list item has no widget, it's a placeholder. """
        pass

    def init_widget(self):
        """ The list item has no widget, it's a placeholder. """

    def init_layout(self):
        """ The list item has no widget, it's a placeholder. """
        pass

    # -------------------------------------------------------------------------
    # ListAdapter API
    # -------------------------------------------------------------------------
    def recycle_view(self, position):
        """ Tell the view to render the item at the given position """
        d = self.declaration

        if position < len(d.parent.items):
            d.index = position
            d.item = d.parent.items[position]
        else:
            d.index = -1
            d.item = None

    def get_view(self):
        """ Return the view for this item (first child widget) """
        for w in self.child_widgets():
            return w

    def on_click(self):
        d = self.declaration
        d.clicked()

    def on_long_click(self):
        d = self.declaration
        d.long_clicked()
