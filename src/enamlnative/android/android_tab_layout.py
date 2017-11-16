"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import List, Typed, set_default

from enamlnative.widgets.tab_layout import ProxyTabLayout, ProxyTabFragment

from .android_view_pager import ViewPagerLayoutParams, LayoutParams
from .android_fragment import AndroidPagerFragment
from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class TabLayout(FrameLayout):
    __nativeclass__ = set_default('android.support.design.widget.TabLayout')
    addTab = JavaMethod('android.support.design.widget.TabLayout$Tab')
    removeTab = JavaMethod('android.support.design.widget.TabLayout$Tab')
    removeAllTabs = JavaMethod()
    newTab = JavaMethod(returns='android.support.design.widget.TabLayout$Tab')

    setSelectedTabIndicatorColor = JavaMethod('android.graphics.Color')
    setSelectedTabIndicatorHeight = JavaMethod('int')
    setTabGravity = JavaMethod('int')
    setTabMode = JavaMethod('int')
    setTabTextColors = JavaMethod('android.graphics.Color',
                                  'android.graphics.Color')

    setCurrentTab = JavaMethod('int')
    setCurrentTabByTag = JavaMethod('java.lang.String')
    addOnTabSelectedListener = JavaMethod(
            'android.support.design.widget.TabLayout$OnTabSelectedListener')

    onTabReselected = JavaCallback(
        'android.support.design.widget.TabLayout$Tab')
    onTabSelected = JavaCallback(
        'android.support.design.widget.TabLayout$Tab')
    onTabUnselected = JavaCallback(
        'android.support.design.widget.TabLayout$Tab')

    MODE_FIXED = 1
    MODE_SCROLLABLE = 0
    GRAVITY_CENTER = 1
    GRAVITY_FILL = 0


class Tab(JavaBridgeObject):
    __nativeclass__ = set_default(
        'android.support.design.widget.TabLayout$Tab')
    setText = JavaMethod('java.lang.CharSequence')
    setIcon = JavaMethod('android.graphics.drawable.Drawable')
    # setContent = JavaMethod('int')
    # setIndicator = JavaMethod('java.lang.CharSequence')
    #


class AndroidTabLayout(AndroidFrameLayout, ProxyTabLayout):
    """ An Android implementation of an Enaml ProxyTabLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TabLayout)

    #: Save created tab spec references
    tabs = List(Tab)

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
        self.widget = TabLayout(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidTabLayout, self).init_widget()
        d = self.declaration
        if d.tab_mode != 'fixed':  #: Default
            self.set_tab_mode(d.tab_mode)
        if d.tab_gravity != 'fill':  #: Default
            self.set_tab_gravity(d.tab_gravity)
        if d.tab_indicator_color_selected:
            self.set_tab_indicator_color_selected(
                d.tab_indicator_color_selected)
        if d.tab_indicator_height:
            self.set_tab_indicator_height(d.tab_indicator_height)
        if d.tab_color or d.tab_color_selected:
            self.set_tab_color(d.tab_color)

        self.widget.addOnTabSelectedListener(self.widget.getId())
        self.widget.onTabSelected.connect(self.on_tab_selected)
        self.widget.onTabUnselected.connect(self.on_tab_unselected)

    def init_layout(self):
        """ Initialize the tabs.

        """
        super(AndroidTabLayout, self).init_layout()
        app = self.get_context()
        d = self.declaration
        parent = self.parent()
        #for page in parent.declaration.pages:
        #    self.widget.newTab().then(lambda tab,page=page:
        # self.on_new_tab(tab,page))

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
        d = self.declaration

        #with self.widget.setCurrentTab.suppressed():
        #    d.current_tab = title

    def on_tab_unselected(self, tab):
        d = self.declaration
        #d.current_tab = title

    def destroy(self):
        """ Destroy all tabs when destroyed 
        
        """
        super(AndroidTabLayout, self).destroy()
        if self.tabs:
            del self.tabs

    # --------------------------------------------------------------------------
    # ProxyTabLayout API
    # --------------------------------------------------------------------------
    def set_current_tab(self, index):
        raise NotImplementedError

    def set_tab_mode(self, mode):
        m = (TabLayout.MODE_FIXED
             if mode == 'fixed' else TabLayout.MODE_SCROLLABLE)
        self.widget.setTabMode(m)

    def set_tab_gravity(self, gravity):
        g = (TabLayout.GRAVITY_CENTER
             if gravity == 'center' else TabLayout.GRAVITY_FILL)
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
        normal = d.tab_color or d.tab_color_selected or '#000000'
        selected = d.tab_color_selected or d.tab_color or '#000000'
        colors = colors or (normal, selected)
        self.widget.setTabTextColors(*colors)


class AndroidTabFragment(AndroidPagerFragment, ProxyTabFragment):
    """ This is just an alias for future expansion. 
    
    """
