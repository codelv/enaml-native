"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, Int, List, set_default

from enamlnative.widgets.view_pager import (
    ProxyViewPager, ProxyPagerTitleStrip, ProxyPagerTabStrip, ProxyPagerFragment
)

from .android_view import LayoutParams
from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback, JavaField
from .app import AndroidApplication


class ViewPager(ViewGroup):
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedViewPager')
    addOnPageChangeListener = JavaMethod(
        'android.support.v4.view.ViewPager$OnPageChangeListener')
    setCurrentItem = JavaMethod('int')
    setOffscreenPageLimit = JavaMethod('int')
    setPageMargin = JavaMethod('int')
    setAdapter = JavaMethod('android.support.v4.view.PagerAdapter')
    onPageScrollStateChanged = JavaCallback('int')
    onPageScrolled = JavaCallback('int', 'float', 'int')
    onPageSelected = JavaCallback('int')
    setPagingEnabled = JavaMethod('boolean')
    setPageTransformer = JavaMethod(
        'boolean', 'android.support.v4.view.ViewPager$PageTransformer')


#: Create builtin ones
#: See https://github.com/geftimov/android-viewpager-transformers/wiki
bundle_id = 'com.eftimoff.viewpagertransformers'
TRANSFORMERS = {k: '{}.{}'.format(bundle_id, v) for k, v in [
    ('accordion', 'AccordionTransformer'),
    ('bg_to_fg', 'BackgroundToForegroundTransformer'),
    ('cube_in', 'CubeInTransformer'),
    ('cube_out', 'CubeOutTransformer'),
    ('default', 'DefaultTransformer'),
    ('depth_page', 'DepthPageTransformer'),
    ('draw_from_back', 'DrawFromBackTransformer'),
    ('flip_horizontal', 'FlipHorizontalTransformer'),
    ('flip_vertical', 'FlipVerticalTransformer'),
    ('fg_to_bg', 'ForegroundToBackgroundTransformer'),
    ('parallax_page', 'ParallaxPageTransformer'),
    ('rotate_down', 'RotateDownTransformer'),
    ('rotate_up', 'RotateUpTransformer'),
    ('stack', 'StackTransformer'),
    ('tablet', 'TabletTransformer'),
    ('zoom_in', 'ZoomInTransformer'),
    ('zoom_out', 'ZoomOutTransformer'),
    ('zoom_out_slide', 'ZoomOutSlideTransformer'),
]}


class PageTransformer(JavaBridgeObject):
    """ A PageTransformer factory """
    __cache__ = {}

    @classmethod
    def from_name(cls, class_name):
        if class_name not in PageTransformer.__cache__:
            #: Try to get the builtin ones using a short name
            class_name = TRANSFORMERS.get(class_name, class_name)

            class Transformer(cls):
                __nativeclass__ = set_default(class_name)
            PageTransformer.__cache__[class_name] = Transformer
        return PageTransformer.__cache__[class_name]()


class ViewPagerLayoutParams(LayoutParams):
    __nativeclass__ = set_default(
        'android.support.v4.view.ViewPager$LayoutParams')
    gravity = JavaField('int')
    isDecor = JavaField('boolean')


class PagerTitleStrip(ViewGroup):
    __nativeclass__ = set_default('android.support.v4.view.PagerTitleStrip')
    setNonPrimaryAlpha = JavaMethod('float')
    setCurrentItem = JavaMethod('int')
    setTextColor = JavaMethod('android.graphics.Color')
    setTextSize = JavaMethod('int', 'float')
    setTextSpacing = JavaMethod('int')
    requestLayout = JavaMethod()
    COMPLEX_UNIT_SP = 2


class PagerTabStrip(PagerTitleStrip):
    __nativeclass__ = set_default('android.support.v4.view.PagerTabStrip')
    setTabIndicatorColor = JavaMethod('android.graphics.Color')
    setDrawFullUnderline = JavaMethod('boolean')


class BridgedFragmentStatePagerAdapter(JavaBridgeObject):
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedFragmentStatePagerAdapter')
    addFragment = JavaMethod('android.support.v4.app.Fragment')
    removeFragment = JavaMethod('android.support.v4.app.Fragment')
    setTitles = JavaMethod('[Ljava.lang.String;')
    clearTitles = JavaMethod()
    notifyDataSetChanged = JavaMethod()


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
    _pending_calls = List()

    @property
    def pages(self):
        """ Get pages """
        #: Defer the import
        for p in self.declaration.pages:
            yield p.proxy

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
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
        if not d.paging_enabled:
            self.set_paging_enabled(d.paging_enabled)
        if d.transition != 'default':
            self.set_transition(d.transition)

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
        AndroidApplication.instance().timed_call(
            self._notify_delay, self._notify_change)

    def child_removed(self, child):
        """ When a child is removed, schedule a data changed notification """
        super(AndroidViewPager, self).child_removed(child)
        self._notify_count += 1
        AndroidApplication.instance().timed_call(
            self._notify_delay, self._notify_change)

    def destroy(self):
        """ Properly destroy adapter """
        super(AndroidViewPager, self).destroy()
        if self.adapter:
            del self.adapter

    def _notify_change(self):
        """ After all changes have settled, tell Java it changed """
        d = self.declaration
        self._notify_count -= 1
        if self._notify_count == 0:
            #: Tell the UI we made changes
            self.adapter.notifyDataSetChanged(now=True)
            AndroidApplication.instance().timed_call(
                500, self._queue_pending_calls)

    def _queue_pending_calls(self):
        #: Now wait for current page to load, then invoke any pending calls
        for i, page in enumerate(self.pages):
            #: Wait for first page!
            #: Trigger when the current page is loaded
            page.ready.then(self._run_pending_calls)
            #: If the page is already complete it will be called right away
            break

    def _run_pending_calls(self, *args):
        if self._pending_calls:
            for call in self._pending_calls:
                call()
            self._pending_calls = []

    # -------------------------------------------------------------------------
    # OnItemRequestedListener API
    # -------------------------------------------------------------------------
    # def on_item_requested(self, position):
    #     print "on_item_requested"
    #     for i, c in enumerate(self.children()):
    #         if i == position:
    #             return c.widget

    # -------------------------------------------------------------------------
    # OnPageChangeListener API
    # -------------------------------------------------------------------------
    def on_page_scroll_state_changed(self, state):
        pass
    
    def on_page_scrolled(self, position, offset, offset_pixels):
        pass
    
    def on_page_selected(self, position):
        d = self.declaration
        with self.widget.setCurrentItem.suppressed():
            d.current_index = position
    
    # -------------------------------------------------------------------------
    # ProxyViewPager API
    # -------------------------------------------------------------------------
    def set_current_index(self, index):
        """ We can only set the index once the page has been created.
        otherwise we get `FragmentManager is already executing transactions`
        errors in Java. To avoid this, we only call this once has been loaded.
        
        """
        # d = self.declaration
        # #: We have to wait for the current_index to be ready before we can
        # #: change pages
        if self._notify_count > 0:
            self._pending_calls.append(
                lambda index=index: self.widget.setCurrentItem(index))
        else:
            self.widget.setCurrentItem(index)

    def set_offscreen_page_limit(self, limit):
        self.widget.setOffscreenPageLimit(limit)

    def set_page_margin(self, margin):
        self.widget.setPageMargin(margin)

    def set_paging_enabled(self, enabled):
        self.widget.setPagingEnabled(enabled)

    def set_transition(self, transition):
        self.widget.setPageTransformer(True,
                                       PageTransformer.from_name(transition))


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

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # ProxyPagerTitleStrip API
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
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

    # -------------------------------------------------------------------------
    # ProxyPagerTabStrip API
    # -------------------------------------------------------------------------
    def set_tab_indicator_color(self, alpha):
        self.widget.setTabIndicatorColor(alpha)

    def set_tab_full_underline(self, enabled):
        self.widget.setDrawFullUnderline(enabled)


