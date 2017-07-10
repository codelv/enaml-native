'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed, Int, set_default

from enamlnative.widgets.view_pager import (
    ProxyViewPager, ProxyPagerTitleStrip, ProxyPagerTabStrip, ProxyPagerFragment
)

from .android_view import LayoutParams
from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback, JavaField
from .app import AndroidApplication


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


class ViewPagerLayoutParams(LayoutParams):
    __javaclass__ = set_default('android.support.v4.view.ViewPager$LayoutParams')
    gravity = JavaField('int')
    isDecor = JavaField('boolean')


class PagerTitleStrip(ViewGroup):
    __javaclass__ = set_default('android.support.v4.view.PagerTitleStrip')
    setNonPrimaryAlpha = JavaMethod('float')
    setCurrentItem = JavaMethod('int')
    setTextColor = JavaMethod('android.graphics.Color')
    setTextSize = JavaMethod('int', 'float')
    setTextSpacing = JavaMethod('int')
    requestLayout = JavaMethod()
    COMPLEX_UNIT_SP = 2


class PagerTabStrip(PagerTitleStrip):
    __javaclass__ = set_default('android.support.v4.view.PagerTabStrip')
    setTabIndicatorColor = JavaMethod('android.graphics.Color')
    setDrawFullUnderline = JavaMethod('boolean')


class BridgedFragmentStatePagerAdapter(JavaBridgeObject):
    __javaclass__ = set_default('com.enaml.adapters.BridgedFragmentStatePagerAdapter')
    addFragment = JavaMethod('android.support.v4.app.Fragment')
    removeFragment = JavaMethod('android.support.v4.app.Fragment')
    setTitles = JavaMethod('[Ljava.lang.String;')
    clearTitles = JavaMethod()
    notifyDataSetChanged = JavaMethod()
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

    #: Pending changes
    _notify_count = Int()
    _notify_delay = Int(2)

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
        self.widget.addOnPageChangeListener(self.widget.getId())
        self.widget.onPageSelected.connect(self.on_page_selected)

        if d.current_index:
            self.set_current_index(d.current_index)

    def child_added(self, child):
        """ When a child is added, schedule a data changed notification """
        super(AndroidViewPager, self).child_added(child)
        self._notify_count += 1
        AndroidApplication.instance().timed_call(self._notify_delay, self._notify_change)

    def child_removed(self, child):
        """ When a child is removed, schedule a data changed notification """
        super(AndroidViewPager, self).child_removed(child)
        self._notify_count += 1
        AndroidApplication.instance().timed_call(self._notify_delay, self._notify_change)

    def destroy(self):
        """ Properly destroy adapter """
        super(AndroidViewPager, self).destroy()
        if self.adapter:
            del self.adapter

    def _notify_change(self):
        """ After all changes have settled, tell Java it changed """
        self._notify_count -= 1
        if self._notify_count == 0:
            self.adapter.notifyDataSetChanged()

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


class AndroidPagerTitleStrip(AndroidViewGroup, ProxyPagerTitleStrip):
    """ An Android implementation of an Enaml ProxyPagerTitleStrip.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(PagerTitleStrip)

    #: ViewPager views should have the given layout params
    layout_param_type = set_default(ViewPagerLayoutParams)

    def _default_layout_params(self):
        d = self.declaration
        try:
            w = int(int(d.layout_width)*self.dp)
        except ValueError:
            w = LayoutParams.LAYOUTS[d.layout_width or 'match_parent']
        try:
            h = int(int(d.layout_height)*self.dp)
        except ValueError:
            h = LayoutParams.LAYOUTS[d.layout_height or 'match_parent']
        #: Takes no arguments
        layout_params = self.layout_param_type()
        layout_params.width = w
        layout_params.height = h
        layout_params.isDecor = True
        return layout_params

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = PagerTitleStrip(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidPagerTitleStrip, self).init_widget()
        d = self.declaration
        #if d.titles:
        #    self.set_titles(d.titles)
        if d.text_color:
            self.set_text_color(d.text_color)
        if d.text_size:
            self.set_text_size(d.text_size)
        if d.text_spacing:
            self.set_text_spacing(d.text_spacing)
        if d.inactive_alpha:
            self.set_inactive_alpha(d.inactive_alpha)

    # --------------------------------------------------------------------------
    # ProxyPagerTitleStrip API
    # --------------------------------------------------------------------------
    # def set_titles(self, titles):
    #     parent = self.parent()
    #     adapter = parent.adapter
    #     adapter.clearTitles()
    #     adapter.setTitles(titles)
    #     self.widget.requestLayout()

    def set_inactive_alpha(self, alpha):
        self.widget.setNonPrimaryAlpha(alpha)

    def set_text_color(self, color):
        self.widget.setTextColor(color)

    def set_text_size(self, size):
        self.widget.setTextSize(PagerTitleStrip.COMPLEX_UNIT_SP, size)

    def set_text_spacing(self, spacing):
        self.widget.setTextSpacing(spacing)


class AndroidPagerTabStrip(AndroidPagerTitleStrip, ProxyPagerTabStrip):
    """ An Android implementation of an Enaml ProxyViewPager.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(PagerTabStrip)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = PagerTabStrip(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidPagerTabStrip, self).init_widget()
        d = self.declaration
        if d.tab_full_underline:
            self.set_tab_full_underline(d.tab_full_underline)
        if d.tab_indicator_color:
            self.set_tab_indicator_color(d.tab_indicator_color)

    # --------------------------------------------------------------------------
    # ProxyPagerTabStrip API
    # --------------------------------------------------------------------------
    def set_tab_indicator_color(self, alpha):
        self.widget.setTabIndicatorColor(alpha)

    def set_tab_full_underline(self, enabled):
        self.widget.setDrawFullUnderline(enabled)


