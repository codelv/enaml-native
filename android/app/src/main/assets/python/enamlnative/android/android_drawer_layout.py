'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed, Bool

from enamlnative.widgets.drawer_layout import ProxyDrawerLayout

from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaMethod, JavaCallback

# LayoutParams = jnius.autoclass('android.view.ViewGroup$LayoutParams')
# Gravity = jnius.autoclass('android.view.Gravity')
# GravityCompat = jnius.autoclass('android.support.v4.view.GravityCompat')
# ViewCompat = jnius.autoclass('android.support.v4.view.ViewCompat')
# #DrawerLayout = jnius.autoclass('android.support.v4.widget.DrawerLayout')
# DrawerLayoutLayoutParams = jnius.autoclass('android.support.v4.widget.DrawerLayout$LayoutParams')

class DrawerLayout(ViewGroup):
    __javaclass__ = 'android.support.v4.widget.DrawerLayout'
    openDrawer = JavaMethod('android.view.View', 'boolean')
    closeDrawer = JavaMethod('android.view.View', 'boolean')
    addDrawerListener = JavaMethod('android.support.v4.widget.DrawerLayout$DrawerListener')
    onDrawerClosed = JavaCallback('android.view.View')
    onDrawerOpened = JavaCallback('android.view.View')
    onDrawerSlide = JavaCallback('android.view.View', 'float')
    onDrawerStateChanged = JavaCallback('int')

    setDrawerElevation = JavaMethod('float')
    setDrawerTitle = JavaMethod('int', 'java.lang.CharSequence')
    setDrawerLockMode = JavaMethod('int')
    setScrimColor = JavaMethod('android.graphics.Color')
    setStatusBarBackgroundColor = JavaMethod('android.graphics.Color')

    LOCK_MODES = {
        'unlocked': 0,
        'locked_closed': 1,
        'locked_open': 2,
        'undefined': 3,
    }


class AndroidDrawerLayout(AndroidViewGroup, ProxyDrawerLayout):
    """ An Android implementation of an Enaml ProxyDrawerLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(DrawerLayout)
    
    def _default_layout_params(self):
        return DrawerLayoutLayoutParams

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = DrawerLayout(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidDrawerLayout, self).init_widget()
        d = self.declaration
        if d.title:
            self.set_title(d.title)
        if d.drawer_elevation:
            self.set_drawer_elevation(d.drawer_elevation)
        if d.lock_mode:
            self.set_lock_mode(d.lock_mode)
        if d.scrim_color:
            self.set_scrim_color(d.scrim_color)
        if d.status_bar_background_color:
            self.set_status_bar_background_color(d.status_bar_background_color)
        
    def init_layout(self):
        super(AndroidDrawerLayout, self).init_layout()
        d = self.declaration
        if d.opened:
            self.set_opened(d.opened)
        if d.title:
            self.set_title(d.title)
        if d.lock_mode:
            self.set_lock_mode(d.lock_mode)
        if d.drawer_elevation:
            self.set_drawer_elevation(d.drawer_elevation)
        if d.scrim_color:
            self.set_scrim_color(d.scrim_color)
        if d.status_bar_background_color:
            self.set_status_bar_background_color(d.status_bar_background_color)

        #: Add drawer listener
        self.widget.addDrawerListener(id(self.widget))
        self.widget.onDrawerClosed.connect(self.on_drawer_closed)
        self.widget.onDrawerOpened.connect(self.on_drawer_opened)

    # --------------------------------------------------------------------------
    # DrawerListener API
    # --------------------------------------------------------------------------
    def on_drawer_closed(self, view):
        d = self.declaration
        with self.widget.closeDrawer.suppressed():
            d.opened = False

    def on_drawer_opened(self, view):
        d = self.declaration
        with self.widget.openDrawer.suppressed():
            d.opened = True

    def on_drawer_slide(self, view, offset):
        pass
    
    def on_drawer_state_changed(self, state):
        pass

    # --------------------------------------------------------------------------
    # ProxyDrawerLayout API
    # --------------------------------------------------------------------------
    def set_opened(self, opened):
        #: Else, triggered from declaration
        d = self.declaration
        view = None
        # for c in self.children():
        #     if hasattr(c.declaration,'layout_gravity') and \
        #                 c.declaration.layout_gravity==d.side:
        #         view = c.widget
        #         break
        # if not view:
        #     raise ValueError("DrawerLayout must have a child with layout_gravity==side")
        #
        # #: Force the view to have the correct layout params
        # if init:
        #     _params = view.getLayoutParams()
        #     gravity = getattr(Gravity, d.side.upper())
        #     params = DrawerLayoutLayoutParams(
        #         _params.width,
        #         _params.height,
        #         gravity
        #     )
        #     view.setLayoutParams(params)
        if opened:
            self.widget.openDrawer(view, d.open_animated)
        else:
            self.widget.closeDrawer(view, d.open_animated)

    def set_drawer_width(self, width):
        d = self.declaration
        self.set_side(d.side)

    # def set_drawer_gravity(self,gravity):
    #     d = self.declaration
    #     params = DrawerLayoutLayoutParams(
    #         d.drawer_width,
    #         LayoutParams.MATCH_PARENT
    #     )
    #     params.gravity = getattr(Gravity,gravity.upper())
    #     self.widget.setLayoutParams(params)

    def set_title(self, title):
        d = self.declaration
        self.widget.setDrawerTitle(d.title_gravity, title)

    def set_title_gravity(self, gravity):
        d = self.declaration
        self.widget.setDrawerTitle(gravity, d.title)

    def set_drawer_elevation(self, elevation):
        self.widget.setDrawerElevation(elevation)

    def set_lock_mode(self, lock_mode):
        mode = DrawerLayout.LOCK_MODES[lock_mode]
        self.widget.setDrawerLockMode(mode)

    def set_scrim_color(self, color):
        self.widget.setScrimColor(color)

    def set_status_bar_background_color(self, color):
        self.widget.setStatusBarBackgroundColor(color)
