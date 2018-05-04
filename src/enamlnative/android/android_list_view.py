"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, Instance, Property, Dict, set_default, observe

from enamlnative.widgets.list_view import ProxyListView, ProxyListItem

from .android_toolkit_object import AndroidToolkitObject

from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaBridgeObject, JavaCallback, JavaMethod, encode

#from .android_adapter import AndroidAdapterView, AdapterView
# class AbsListView(AdapterView):
#     __nativeclass__ = set_default('android.widget.AbsListView')
#     pointToPosition = JavaMethod('int', 'int')
#     setAdapter = JavaMethod('android.widget.ListAdapter')
#
#
# class ListView(AbsListView):
#     __nativeclass__ = set_default('android.widget.ListView')
#     setDividerHeight = JavaMethod('int')
#     setFooterDividersEnabled = JavaMethod('boolean')
#     setHeaderDividersEnabled = JavaMethod('boolean')
#     setItemsCanFocus = JavaMethod('boolean')
#     setSelection = JavaMethod('int')
#     smoothScrollByOffset = JavaMethod('int')
#     smoothScrollToPosition = JavaMethod('int')
#
#     # OnScrollListener API
#     setOnScrollListener = JavaMethod(
#         'android.widget.AbsListView$OnScrollListener')
#     onScroll = JavaCallback('android.widget.AbsListView', 'int', 'int', 'int')
#     onScrollStateChanged = JavaCallback('android.widget.AbsListView', 'int')


class RecylerView(ViewGroup):
    __nativeclass__ = set_default('android.support.v7.widget.RecyclerView')
    invalidate = JavaMethod()
    setHasFixedSize = JavaMethod('boolean')
    scrollTo = JavaMethod('int', 'int')
    scrollToPosition = JavaMethod('int')
    setItemViewCacheSize = JavaMethod('int')
    setAdapter = JavaMethod('android.support.v7.widget.RecyclerView$Adapter')
    setHasFixedSize = JavaMethod('boolean')
    setLayoutManager = JavaMethod(
        'android.support.v7.widget.RecyclerView$LayoutManager')

    setRecyclerListener = JavaMethod(
        'android.support.v7.widget.RecyclerView$RecyclerListener')

    class LayoutManager(JavaBridgeObject):
        __nativeclass__ = set_default(
            'android.support.v7.widget.RecyclerView$LayoutManager')
        scrollToPosition = JavaMethod('int')
        setItemPrefetchEnabled = JavaMethod('boolean')

        HORIZONTAL = 0
        VERTICAL = 1


class StaggeredLayoutManager(RecylerView.LayoutManager):
    __nativeclass__ = set_default(
        'android.support.v7.widget.StaggeredLayoutManager')
    __signature__ = set_default(('int', 'int'))
    setOrientation = JavaMethod('int')
    setSpanCount = JavaMethod('int')


class LinearLayoutManager(RecylerView.LayoutManager):
    __nativeclass__ = set_default(
        'android.support.v7.widget.LinearLayoutManager')
    __signature__ = set_default(('android.content.Context', 'int',
                                 'boolean'))

    scrollToPositionWithOffset = JavaMethod('int', 'int')
    setInitialPrefetchItemCount = JavaMethod('int')
    setOrientation = JavaMethod('int')
    setRecycleChildrenOnDetach = JavaMethod('boolean')
    setReverseLayout = JavaMethod('boolean')
    setSmoothScrollbarEnabled = JavaMethod('boolean')
    setStackFromEnd = JavaMethod('boolean')


class GridLayoutManager(LinearLayoutManager):
    __nativeclass__ = set_default(
        'android.support.v7.widget.GridLayoutManager')
    __signature__ = set_default(('android.content.Context', 'int', 'int',
                                 'boolean'))
    setSpanCount = JavaMethod('int')

# class BridgedListAdapter(JavaBridgeObject):
#     """ An adapter that implements a recycleview pattern.
#
#     """
#     __nativeclass__ = set_default(
#         'com.codelv.enamlnative.adapters.BridgedListAdapter')
#     setListView = JavaMethod('android.widget.ListView',
#                              'com.codelv.enamlnative.adapters.'
#                              'BridgedListAdapter$BridgedListAdapterListener')
#     setCount = JavaMethod('int')
#     setRecycleViews = JavaMethod('[Landroid.view.View;')
#     clearRecycleViews = JavaMethod()
#
#     #: BridgedListAdapterListener API
#     onRecycleView = JavaCallback('int', 'int', 'int')
#     onVisibleCountChanged = JavaCallback('int','int')
#     onScrollStateChanged = JavaCallback('android.widget.AbsListView','int')


class BridgedRecyclerAdapter(JavaBridgeObject):
    """ An adapter that implements a recycleview pattern.

    """
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedRecyclerAdapter')
    __signature__ = set_default(
        ('android.support.v7.widget.RecyclerView',))
    setRecyleListener = JavaMethod(
        'com.codelv.enamlnative.adapters.BridgedRecyclerAdapter'
        '$BridgedListAdapterListener'
    )
    setItemCount = JavaMethod('int')
    setRecycleViews = JavaMethod('[Landroid.view.View;')
    clearRecycleViews = JavaMethod()

    #: BridgedListAdapterListener API
    onRecycleView = JavaCallback('int', 'int')
    onVisibleCountChanged = JavaCallback('int', 'int')
    onScrollStateChanged = JavaCallback('android.widget.AbsListView','int')

    notifyDataSetChanged = JavaMethod()
    notifyItemChanged = JavaMethod('int')
    notifyItemInserted = JavaMethod('int')
    notifyItemRemoved = JavaMethod('int')
    notifyItemRangeChanged = JavaMethod('int', 'int')
    notifyItemRangeInserted = JavaMethod('int', 'int')
    notifyItemRangeRemoved = JavaMethod('int', 'int')


class AndroidListView(AndroidViewGroup, ProxyListView):
    """ An Android implementation of an Enaml ProxyListView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(RecylerView)

    #: Reference to adapter
    adapter = Typed(BridgedRecyclerAdapter)

    #: Layout manager
    layout_manager = Instance(RecylerView.LayoutManager)

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
        self.widget = RecylerView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidListView, self).init_widget()
        d = self.declaration
        self.set_arrangement(d.arrangement)

        # w = self.widget
        # w.setOnItemClickListener(w.getId())
        # w.setOnItemLongClickListener(w.getId())
        # w.onItemClick.connect(self.on_item_click)
        # w.onItemLongClick.connect(self.on_item_long_click)
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
        adapter = self.adapter = BridgedRecyclerAdapter(w)

        # I'm sure this will make someone upset haha
        adapter.setRecyleListener(adapter.getId())
        adapter.onRecycleView.connect(self.on_recycle_view)
        #adapter.onVisibleCountChanged.connect(self.on_visible_count_changed)
        #adapter.onScrollStateChanged.connect(self.on_scroll_state_changed)
        self.set_items(d.items)
        w.setAdapter(adapter)
        #self.set_selected(d.selected)
        self.refresh_views()

    # -------------------------------------------------------------------------
    # BridgedListAdapterListener API
    # -------------------------------------------------------------------------
    def on_recycle_view(self, index, position):
        """ Update the item the view at the given index should display
        """
        item = self.list_items[index]
        self.item_mapping[position] = item
        item.recycle_view(position)

    def on_scroll_state_changed(self, view, state):
        pass

    # -------------------------------------------------------------------------
    # ProxyListView API
    # -------------------------------------------------------------------------
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
        adapter = self.adapter
        adapter.setItemCount(len(items))
        adapter.notifyDataSetChanged()

    @observe('declaration.items')
    def _on_items_changed(self, change):
        """ Observe container events on the items list and update the
        adapter appropriately. 
        """
        if change['type'] != 'container':
            return
        op = change['operation']
        if op == 'append':
            i = len(change['value'])-1
            self.adapter.notifyItemInserted(i)
        elif op == 'insert':
            self.adapter.notifyItemInserted(change['index'])
        elif op in ('pop', '__delitem__'):
            self.adapter.notifyItemRemoved(change['index'])
        elif op == '__setitem__':
            self.adapter.notifyItemChanged(change['index'])
        elif op == 'extend':
            n = len(change['items'])
            i = len(change['value'])-n
            self.adapter.notifyItemRangeInserted(i, n)
        elif op in ('remove', 'reverse', 'sort'):
            # Reset everything for these
            self.adapter.notifyDataSetChanged()

    def set_arrangement(self, arrangement):
        ctx = self.get_context()
        d = self.declaration
        reverse = False
        orientation = (
            LinearLayoutManager.VERTICAL if d.orientation == 'vertical'
            else LinearLayoutManager.HORIZONTAL)
        if arrangement == 'linear':
            manager = LinearLayoutManager(ctx, orientation, reverse)
        elif arrangement == 'grid':
            manager = GridLayoutManager(ctx, d.span_count, orientation,
                                        reverse)
        elif arrangement == 'staggered':
            manager = StaggeredLayoutManager(d.span_count, orientation)
        self.layout_manager = manager
        self.widget.setLayoutManager(manager)

    def set_span_count(self, count):
        if not self.layout_manager:
            return
        self.layout_manager.setSpanCount(count)

    def set_orientation(self, orientation):
        if not self.layout_manager:
            return
        orientation = (
            LinearLayoutManager.VERTICAL if orientation == 'vertical'
            else LinearLayoutManager.HORIZONTAL)
        self.layout_manager.setOrientation(orientation)

    def set_selected(self, index):
        self.widget.setSelection(index)

    def scroll_to(self, x, y):
        self.widget.scrollTo(x, y)

    def scroll_to_position(self, position):
        self.widget.scrollToPosition(position)


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
