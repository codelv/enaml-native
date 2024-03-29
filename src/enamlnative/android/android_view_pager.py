"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from typing import ClassVar
from atom.api import Int, List, Typed, set_default
from enamlnative.widgets.view import coerce_gravity, coerce_size
from enamlnative.widgets.view_pager import (
    ProxyPagerTabStrip,
    ProxyPagerTitleStrip,
    ProxyViewPager,
)
from enamlnative.core.bridge import encode
from .android_content import Context
from .android_fragment import AndroidFragment
from .android_view import LayoutParams
from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaBridgeObject, JavaCallback, JavaField, JavaMethod

package = "androidx.viewpager.widget"


class ViewPager(ViewGroup):
    __nativeclass__ = "com.codelv.enamlnative.adapters.BridgedViewPager"
    __signature__ = [Context]
    addOnPageChangeListener = JavaMethod(f"{package}.ViewPager$OnPageChangeListener")
    setCurrentItem = JavaMethod(int)
    setOffscreenPageLimit = JavaMethod(int)
    setPageMargin = JavaMethod(int)
    setAdapter = JavaMethod(f"{package}.PagerAdapter")
    onPageScrollStateChanged = JavaCallback(int)
    onPageScrolled = JavaCallback(int, float, int)
    onPageSelected = JavaCallback(int)
    setPagingEnabled = JavaMethod(bool)
    setPageTransformer = JavaMethod(bool, f"{package}.ViewPager$PageTransformer")


#: Create builtin ones
#: See https://github.com/geftimov/android-viewpager-transformers/wiki
bundle_id = "com.eftimoff.viewpagertransformers"
TRANSFORMERS = {
    k: f"{bundle_id}.{v}"
    for k, v in [
        ("accordion", "AccordionTransformer"),
        ("bg_to_fg", "BackgroundToForegroundTransformer"),
        ("cube_in", "CubeInTransformer"),
        ("cube_out", "CubeOutTransformer"),
        ("default", "DefaultTransformer"),
        ("depth_page", "DepthPageTransformer"),
        ("draw_from_back", "DrawFromBackTransformer"),
        ("flip_horizontal", "FlipHorizontalTransformer"),
        ("flip_vertical", "FlipVerticalTransformer"),
        ("fg_to_bg", "ForegroundToBackgroundTransformer"),
        ("parallax_page", "ParallaxPageTransformer"),
        ("rotate_down", "RotateDownTransformer"),
        ("rotate_up", "RotateUpTransformer"),
        ("stack", "StackTransformer"),
        ("tablet", "TabletTransformer"),
        ("zoom_in", "ZoomInTransformer"),
        ("zoom_out", "ZoomOutTransformer"),
        ("zoom_out_slide", "ZoomOutSlideTransformer"),
    ]
}


class PageTransformer(JavaBridgeObject):
    """A PageTransformer factory"""

    __cache__: ClassVar[dict[str, "PageTransformer"]] = {}

    @classmethod
    def from_name(cls, class_name):
        if class_name not in PageTransformer.__cache__:
            #: Try to get the builtin ones using a short name
            class_name = TRANSFORMERS.get(class_name, class_name)

            class Transformer(cls):
                __nativeclass__ = class_name

            PageTransformer.__cache__[class_name] = Transformer
        return PageTransformer.__cache__[class_name]()


class ViewPagerLayoutParams(LayoutParams):
    __nativeclass__ = f"{package}.ViewPager$LayoutParams"
    gravity = JavaField(int)
    isDecor = JavaField(bool)


class PagerTitleStrip(ViewGroup):
    __nativeclass__ = f"{package}.PagerTitleStrip"
    __signature__ = [Context]
    setNonPrimaryAlpha = JavaMethod(float)
    setCurrentItem = JavaMethod(int)
    setTextColor = JavaMethod("android.graphics.Color")
    setTextSize = JavaMethod(int, float)
    setTextSpacing = JavaMethod(int)
    requestLayout = JavaMethod()
    COMPLEX_UNIT_SP = 2


class PagerTabStrip(PagerTitleStrip):
    __nativeclass__ = f"{package}.PagerTabStrip"
    setTabIndicatorColor = JavaMethod("android.graphics.Color")
    setDrawFullUnderline = JavaMethod(bool)


class BridgedFragmentStatePagerAdapter(JavaBridgeObject):
    __nativeclass__ = "com.codelv.enamlnative.adapters.BridgedFragmentStatePagerAdapter"
    addFragment = JavaMethod("androidx.fragment.app.Fragment")
    addFragments = JavaMethod("[Landroidx.fragment.app.Fragment;")
    removeFragment = JavaMethod("androidx.fragment.app.Fragment")
    removeFragments = JavaMethod("[Landroidx.fragment.app.Fragment;")
    setTitles = JavaMethod(list[str])
    clearTitles = JavaMethod()
    notifyDataSetChanged = JavaMethod()


class AndroidViewPager(AndroidViewGroup, ProxyViewPager):
    """An Android implementation of an Enaml ProxyViewPager."""

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
        """Get pages"""
        #: Defer the import
        for p in self.declaration.pages:
            yield p.proxy

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        self.widget = ViewPager(self.get_context())
        self.adapter = BridgedFragmentStatePagerAdapter()

    def init_layout(self):
        super().init_layout()
        d = self.declaration
        w = self.widget

        # Add pages
        adapter = self.adapter
        adapter.addFragments([encode(c.fragment) for c in self.pages])

        # Set adapter
        w.setAdapter(adapter)
        w.addOnPageChangeListener(w.getId())
        w.onPageSelected.connect(self.on_page_selected)

        if d.current_index:
            self.set_current_index(d.current_index)

    def child_added(self, child):
        """When a child is added, add it to the adapter."""
        if isinstance(child, AndroidFragment):
            self.adapter.addFragment(child.fragment)

    def child_removed(self, child):
        """When a child is removed, remove it from the adapter"""
        if isinstance(child, AndroidFragment):
            self.adapter.removeFragment(child.fragment)

    def _queue_pending_calls(self):
        #: Now wait for current page to load, then invoke any pending calls
        for i, page in enumerate(self.pages):
            #: Wait for first page!
            #: Trigger when the current page is loaded
            page.ready.add_done_callback(self._run_pending_calls)
            #: If the page is already complete it will be called right away
            break

    def _run_pending_calls(self, f):
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
        """We can only set the index once the page has been created.
        otherwise we get `FragmentManager is already executing transactions`
        errors in Java. To avoid this, we only call this once has been loaded.

        """
        # d = self.declaration
        # #: We have to wait for the current_index to be ready before we can
        # #: change pages
        if self._notify_count > 0:
            self._pending_calls.append(
                lambda index=index: self.widget.setCurrentItem(index)
            )
        else:
            self.widget.setCurrentItem(index)

    def set_offscreen_page_limit(self, limit):
        self.widget.setOffscreenPageLimit(limit)

    def set_page_margin(self, margin):
        self.widget.setPageMargin(margin)

    def set_paging_enabled(self, enabled):
        self.widget.setPagingEnabled(enabled)

    def set_transition(self, transition):
        self.widget.setPageTransformer(True, PageTransformer.from_name(transition))

    def create_layout_params(self, child, layout):
        """Override as there is no (width, height) constructor."""
        if isinstance(child, AndroidFragment):
            return super().create_layout_params(child, layout)
        # Only apply to decor views
        dp = self.dp
        w, h = (
            coerce_size(layout.get("width", "match_parent")),
            coerce_size(layout.get("height", "wrap_content")),
        )
        w = w if w < 0 else int(w * dp)
        h = h if h < 0 else int(h * dp)
        # No (w,h) constructor
        params = ViewPagerLayoutParams()
        params.width = w
        params.height = h
        params.isDecor = True
        return params

    def apply_layout(self, child, layout):
        super().apply_layout(child, layout)
        if "gravity" in layout:
            child.layout_params.gravity = coerce_gravity(layout["gravity"])


class AndroidPagerTitleStrip(AndroidViewGroup, ProxyPagerTitleStrip):
    """An Android implementation of an Enaml ProxyPagerTitleStrip."""

    #: A reference to the widget created by the proxy.
    widget = Typed(PagerTitleStrip)

    default_layout = set_default(  # type: ignore
        {"width": "match_parent", "height": "wrap_content", "gravity": "top"}
    )

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        self.widget = PagerTitleStrip(self.get_context())

    def init_layout(self):
        # Make sure the layout always exists
        if not self.layout_params:
            self.set_layout({})
        super().init_layout()

    # -------------------------------------------------------------------------
    # ProxyPagerTitleStrip API
    # -------------------------------------------------------------------------
    def set_inactive_alpha(self, alpha):
        self.widget.setNonPrimaryAlpha(alpha)

    def set_text_color(self, color):
        self.widget.setTextColor(color)

    def set_text_size(self, size):
        self.widget.setTextSize(PagerTitleStrip.COMPLEX_UNIT_SP, size)

    def set_text_spacing(self, spacing):
        self.widget.setTextSpacing(spacing)


class AndroidPagerTabStrip(AndroidPagerTitleStrip, ProxyPagerTabStrip):
    """An Android implementation of an Enaml ProxyViewPager."""

    #: A reference to the widget created by the proxy.
    widget = Typed(PagerTabStrip)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        self.widget = PagerTabStrip(self.get_context())

    # -------------------------------------------------------------------------
    # ProxyPagerTabStrip API
    # -------------------------------------------------------------------------
    def set_tab_indicator_color(self, alpha):
        self.widget.setTabIndicatorColor(alpha)

    def set_tab_full_underline(self, enabled):
        self.widget.setDrawFullUnderline(enabled)
