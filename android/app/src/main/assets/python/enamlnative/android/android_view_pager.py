'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed, set_default

from enamlnative.widgets.view_pager import ProxyViewPager

from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class ViewPager(ViewGroup):
    __javaclass__ = set_default('android.support.v4.view.ViewPager')
    addOnPageChangeListener = JavaMethod('android.support.v4.view.ViewPager$OnPageChangeListener')
    setCurrentItem = JavaMethod('int')
    setOffscreenPageLimit = JavaMethod('int')
    setPageMargin = JavaMethod('int')
    setAdapter = JavaMethod('android.support.v4.view.PagerAdapter')
    onPageScrollStateChanged = JavaCallback('int')
    onPageScrolled = JavaCallback('int', 'float', 'int')
    onPageSelected = JavaCallback('int')


class BridgedFragmentStatePagerAdapter(JavaBridgeObject):
    __javaclass__ = set_default('com.enaml.adapters.BridgedFragmentStatePagerAdapter')
    addFragment = JavaMethod('android.support.v4.app.Fragment')
    removeFragment = JavaMethod('android.support.v4.app.Fragment')
    # setOnItemRequestedListener = JavaMethod(
    #     'com.enaml.adapters.BridgedFragmentStatePagerAdapter$OnItemRequestedListener')
    # onItemRequested = JavaCallback('int', returns='int')


class AndroidViewPager(AndroidViewGroup, ProxyViewPager):
    """ An Android implementation of an Enaml ProxyViewPager.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ViewPager)

    #: Adapter
    adapter = Typed(BridgedFragmentStatePagerAdapter)
    
    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ViewPager(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidViewPager, self).init_widget()
        d = self.declaration
        if d.offscreen_page_limit:
            self.set_offscreen_page_limit(d.offscreen_page_limit)
        if d.page_margin >= 0:
            self.set_page_margin(d.page_margin)

        #: Create adapter
        self.adapter = BridgedFragmentStatePagerAdapter()

    def init_layout(self):
        super(AndroidViewPager, self).init_layout()
        d = self.declaration

        #: Set adapter
        self.widget.setAdapter(self.adapter)
        self.widget.addOnPageChangeListener(id(self.widget))
        self.widget.onPageSelected.connect(self.on_page_selected)

        if d.current_index:
            self.set_current_index(d.current_index)

    def destroy(self):
        """ Properly destroy adapter """
        super(AndroidViewPager, self).destroy()
        if self.adapter:
            del self.adapter

    # # --------------------------------------------------------------------------
    # # OnItemRequestedListener API
    # # --------------------------------------------------------------------------
    # def on_item_requested(self, position):
    #     print "on_item_requested"
    #     for i, c in enumerate(self.children()):
    #         if i == position:
    #             return c.widget

    # --------------------------------------------------------------------------
    # OnPageChangeListener API
    # --------------------------------------------------------------------------
    def on_page_scroll_state_changed(self, state):
        pass
    
    def on_page_scrolled(self, position, offset, offset_pixels):
        pass
    
    def on_page_selected(self, position):
        d = self.declaration
        with self.widget.setCurrentItem.suppressed():
            d.current_index = position
    
    # --------------------------------------------------------------------------
    # ProxyViewPager API
    # --------------------------------------------------------------------------
    def set_current_index(self, index):
        self.widget.setCurrentItem(index)

    def set_offscreen_page_limit(self, limit):
        self.widget.setOffscreenPageLimit(limit)

    def set_page_margin(self, margin):
        self.widget.setPageMargin(margin)
