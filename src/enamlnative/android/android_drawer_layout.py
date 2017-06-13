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

from .android_view_group import AndroidViewGroup

LayoutParams = jnius.autoclass('android.view.ViewGroup$LayoutParams')
Gravity = jnius.autoclass('android.view.Gravity')
GravityCompat = jnius.autoclass('android.support.v4.view.GravityCompat')
ViewCompat = jnius.autoclass('android.support.v4.view.ViewCompat')
DrawerLayout = jnius.autoclass('android.support.v4.widget.DrawerLayout')
DrawerLayoutLayoutParams = jnius.autoclass('android.support.v4.widget.DrawerLayout$LayoutParams')

class DrawerListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/support/v4/widget/DrawerLayout$DrawerListener']
    __javacontext__ = 'app'

    def __init__(self, handler):
        self.__handler__ = handler
        super(DrawerListener, self).__init__()

    @jnius.java_method('(Landroid/view/View;)V')
    def onDrawerClosed(self, view):
        self.__handler__.on_drawer_closed(view)
    
    @jnius.java_method('(Landroid/view/View;)V')
    def onDrawerOpened(self, view):
        self.__handler__.on_drawer_opened(view)
        
    @jnius.java_method('(Landroid/view/View;F)V')
    def onDrawerSlide(self, view, slideOffset):
        self.__handler__.on_drawer_slide(view, slideOffset)
    
    @jnius.java_method('(I)V')
    def onDrawerStateChanged(self, newState):
        self.__handler__.on_drawer_state_changed(newState)

class AndroidDrawerLayout(AndroidViewGroup, ProxyDrawerLayout):
    """ An Android implementation of an Enaml ProxyDrawerLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(DrawerLayout)
    
    #: Save a reference to the drawer listener
    drawer_listener = Typed(DrawerListener)

    #: Save reference to the drawer state set by events
    _opened = Bool(False)
    
    def _default_layout_params(self):
        return DrawerLayoutLayoutParams

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

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
        self.set_opened(d.opened, init=True)

        #: Add drawer listener
        self.drawer_listener = DrawerListener(self)
        self.widget.addDrawerListener(self.drawer_listener)

    # --------------------------------------------------------------------------
    # DrawerListener API
    # --------------------------------------------------------------------------
    def on_drawer_closed(self, view):
        self._opened = False

    def on_drawer_opened(self, view):
        self._opened = True

    def on_drawer_slide(self, view, offset):
        pass
    
    def on_drawer_state_changed(self, state):
        pass

    def _observe__opened(self, change):
        d = self.declaration
        d.opened = self._opened

    # --------------------------------------------------------------------------
    # ProxyDrawerLayout API
    # --------------------------------------------------------------------------
    def set_opened(self, opened, init=False):
        if not init and (opened == self._opened):
            # Triggered by user event, ignore
            return
        self._opened = opened

        #: Else, triggered from declaration
        d = self.declaration
        view = None
        for c in self.children():
            if hasattr(c.declaration,'layout_gravity') and \
                        c.declaration.layout_gravity==d.side:
                view = c.widget
                break
        if not view:
            raise ValueError("DrawerLayout must have a child with layout_gravity==side")

        #: Force the view to have the correct layout params
        if init:
            _params = view.getLayoutParams()
            gravity = getattr(Gravity, d.side.upper())
            params = DrawerLayoutLayoutParams(
                _params.width,
                _params.height,
                gravity
            )
            view.setLayoutParams(params)
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
        self.widget.setTitle(title,d.title_gravity)

    def set_title_gravity(self, gravity):
        d = self.declaration
        self.widget.setTitle(d.title,gravity)

    def set_drawer_elevation(self, elevation):
        self.widget.setDrawerElevation(elevation)

    def set_lock_mode(self, mode):
        self.widget.setDrawerLockMode(mode)

    def set_scrim_color(self, color):
        self.widget.setScrimColor(color)

    def set_status_bar_background_color(self, color):
        self.widget.setStatusBarBackgroundColor(color)