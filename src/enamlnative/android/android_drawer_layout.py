"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, List, set_default

from enamlnative.widgets.drawer_layout import ProxyDrawerLayout

from .android_view_group import AndroidViewGroup, ViewGroup, MarginLayoutParams
from .bridge import JavaMethod, JavaCallback, JavaField


class DrawerLayout(ViewGroup):
    __nativeclass__ = set_default('android.support.v4.widget.DrawerLayout')
    openDrawer = JavaMethod('android.view.View')
    closeDrawer = JavaMethod('android.view.View')
    addDrawerListener = JavaMethod(
        'android.support.v4.widget.DrawerLayout$DrawerListener')
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


class DrawerLayoutParams(MarginLayoutParams):
    """ Update the child widget with the given params """
    __nativeclass__ = set_default(
        'android.support.v4.widget.DrawerLayout$LayoutParams')
    gravity = JavaField('int')


class AndroidDrawerLayout(AndroidViewGroup, ProxyDrawerLayout):
    """ An Android implementation of an Enaml ProxyDrawerLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(DrawerLayout)

    #: Drawer state
    drawer_state = List()

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
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

        #: Set the layout params to a drawer layout
        for c in self.drawers():
            c.layout_param_type = DrawerLayoutParams

    def init_layout(self):
        super(AndroidDrawerLayout, self).init_layout()
        d = self.declaration

        #: Set the proper layout for each child
        # for c in self.drawers():
        #     #: Set the gravity
        #     gravity = 3 if c.declaration.layout_gravity == 'left' else 5
        #     c.layout_params.gravity = gravity

        if d.opened:
            self.set_opened(d.opened)

        #: Add drawer listener
        self.widget.addDrawerListener(self.widget.getId())
        self.widget.onDrawerClosed.connect(self.on_drawer_closed)
        self.widget.onDrawerOpened.connect(self.on_drawer_opened)

    def drawers(self):
        for i, c in enumerate(self.children()):
            if i != 0:
                yield c

    # -------------------------------------------------------------------------
    # DrawerListener API
    # -------------------------------------------------------------------------
    def on_drawer_closed(self, view):
        d = self.declaration
        with self.widget.openDrawer.suppressed():
            with self.widget.closeDrawer.suppressed():
                #: Remove view from state
                d.opened = [v for v in d.opened
                                if v.proxy.widget.getId() != view]

    def on_drawer_opened(self, view):
        d = self.declaration
        with self.widget.openDrawer.suppressed():
            with self.widget.closeDrawer.suppressed():
                #: Add view to state
                for c in self.drawers():
                    if c.widget.getId() == view:
                        d.opened = list(set(d.opened + [c.declaration]))
                        break

    def on_drawer_slide(self, view, offset):
        pass

    def on_drawer_state_changed(self, state):
        pass

    # -------------------------------------------------------------------------
    # ProxyDrawerLayout API
    # -------------------------------------------------------------------------
    def set_opened(self, opened):
        """ Opened is a tuple of the drawer sides that are open

        """
        self.drawer_state = opened

    def _observe_drawer_state(self, change):
        #: Diff old and new to find changes
        old = set(change.get('oldvalue', []))
        new = set(change.get('value', []))

        #: Closed
        for c in old.difference(new):
            view = c.proxy.widget
            self.widget.closeDrawer(view)

        #: Opened
        for c in new.difference(old):
            view = c.proxy.widget
            self.widget.openDrawer(view)

        #: Rest unchanged

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
