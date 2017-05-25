#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.drawer_layout import ProxyDrawerLayout

from .android_view_group import AndroidViewGroup

_Gravity = jnius.autoclass('android.view.Gravity')
_DrawerLayout = jnius.autoclass('android.support.v4.widget.DrawerLayout')

class AndroidDrawerLayout(AndroidViewGroup, ProxyDrawerLayout):
    """ An Android implementation of an Enaml ProxyDrawerLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_DrawerLayout)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _DrawerLayout(self.get_context())

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

    #--------------------------------------------------------------------------
    # ProxyDrawerLayout API
    #--------------------------------------------------------------------------
    def set_opened(self, opened):
        d = self.declaration
        gravity = getattr(_Gravity,d.open_gravity.upper())
        if opened:
            self.widget.openDrawer(gravity,d.open_animated)
        else:
            self.widget.closeDrawer(gravity,d.open_animated)

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