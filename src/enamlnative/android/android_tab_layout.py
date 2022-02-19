"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import List, Typed, set_default
from enamlnative.widgets.tab_layout import ProxyTabFragment, ProxyTabLayout
from .android_fragment import AndroidPagerFragment
from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaBridgeObject, JavaCallback, JavaMethod

package = "com.google.android.material.tabs"


class TabLayout(FrameLayout):
    __nativeclass__ = f"{package}.TabLayout"
    addTab = JavaMethod(f"{package}.TabLayout$Tab")
    removeTab = JavaMethod(f"{package}.TabLayout$Tab")
    removeAllTabs = JavaMethod()
    newTab = JavaMethod(returns=f"{package}.TabLayout$Tab")

    setSelectedTabIndicatorColor = JavaMethod("android.graphics.Color")
    setSelectedTabIndicatorHeight = JavaMethod("int")
    setTabGravity = JavaMethod("int")
    setTabMode = JavaMethod("int")
    setTabTextColors = JavaMethod("android.graphics.Color", "android.graphics.Color")

    setCurrentTab = JavaMethod("int")
    setCurrentTabByTag = JavaMethod("java.lang.String")
    addOnTabSelectedListener = JavaMethod(f"{package}.TabLayout$OnTabSelectedListener")

    onTabReselected = JavaCallback(f"{package}.TabLayout$Tab")
    onTabSelected = JavaCallback(f"{package}.TabLayout$Tab")
    onTabUnselected = JavaCallback(f"{package}.TabLayout$Tab")

    MODE_FIXED = 1
    MODE_SCROLLABLE = 0
    GRAVITY_CENTER = 1
    GRAVITY_FILL = 0


class Tab(JavaBridgeObject):
    __nativeclass__ = f"{package}.TabLayout$Tab"
    setText = JavaMethod("java.lang.CharSequence")
    setIcon = JavaMethod("android.graphics.drawable.Drawable")
    # setContent = JavaMethod('int')
    # setIndicator = JavaMethod('java.lang.CharSequence')
    #


class AndroidTabLayout(AndroidFrameLayout, ProxyTabLayout):
    """An Android implementation of an Enaml ProxyTabLayout."""

    #: A reference to the widget created by the proxy.
    widget = Typed(TabLayout)

    #: Save created tab spec references
    tabs = List(Tab)

    default_layout = set_default(  # type: ignore
        {"width": "match_parent", "height": "wrap_content", "gravity": "top"}
    )

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = TabLayout(self.get_context(), None, d.style)

    def init_widget(self):
        """Initialize the underlying widget."""
        super().init_widget()
        w = self.widget
        w.addOnTabSelectedListener(w.getId())
        w.onTabSelected.connect(self.on_tab_selected)
        w.onTabUnselected.connect(self.on_tab_unselected)

    # --------------------------------------------------------------------------
    # OnTabSelectedListener API
    # --------------------------------------------------------------------------
    def on_new_tab(self, tab, page):
        tab = Tab(__id__=tab)
        d = page
        if d.title:
            tab.setText(d.title)
        self.widget.addTab(tab)
        #: TODO: Handle icon?
        #: Hold reference
        self.tabs.append(tab)

    def on_tab_selected(self, tab):
        pass
        # d = self.declaration
        # with self.widget.setCurrentTab.suppressed():
        #    d.current_tab = title

    def on_tab_unselected(self, tab):
        pass
        # d = self.declaration
        # d.current_tab = title

    def destroy(self):
        """Destroy all tabs when destroyed"""
        super().destroy()
        if self.tabs:
            del self.tabs

    # --------------------------------------------------------------------------
    # ProxyTabLayout API
    # --------------------------------------------------------------------------
    def set_current_tab(self, index):
        raise NotImplementedError

    def set_tab_mode(self, mode):
        m = TabLayout.MODE_FIXED if mode == "fixed" else TabLayout.MODE_SCROLLABLE
        self.widget.setTabMode(m)

    def set_tab_gravity(self, gravity):
        g = TabLayout.GRAVITY_CENTER if gravity == "center" else TabLayout.GRAVITY_FILL
        self.widget.setTabGravity(g)

    def set_tab_indicator_color_selected(self, color):
        self.widget.setSelectedTabIndicatorColor(color)

    def set_tab_indicator_height(self, height):
        self.widget.setSelectedTabIndicatorHeight(height)

    def set_tab_color(self, color):
        self.set_tab_colors()

    def set_tab_color_selected(self, color):
        self.set_tab_colors()

    def set_tab_colors(self, colors=None):
        d = self.declaration
        normal = d.tab_color or d.tab_color_selected or "#000000"
        selected = d.tab_color_selected or d.tab_color or "#000000"
        colors = colors or (normal, selected)
        self.widget.setTabTextColors(*colors)


class AndroidTabFragment(AndroidPagerFragment, ProxyTabFragment):
    """This is just an alias for future expansion."""
