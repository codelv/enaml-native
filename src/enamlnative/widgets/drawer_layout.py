"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Enum, Float, ForwardTyped, Int, List, Str, Typed
from enaml.core.declarative import d_, observe
from .view import View
from .view_group import ProxyViewGroup, ViewGroup


class ProxyDrawerLayout(ProxyViewGroup):
    """The abstract definition of a proxy DrawerLayout object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: DrawerLayout)

    def set_opened(self, opened):
        raise NotImplementedError

    def set_side(self, side):
        pass

    def set_title(self, title):
        raise NotImplementedError

    def set_title_gravity(self, gravity):
        raise NotImplementedError

    def set_drawer_width(self, width):
        raise NotImplementedError

    def set_drawer_elevation(self, elevation):
        raise NotImplementedError

    def set_lock_mode(self, mode):
        raise NotImplementedError

    def set_scrim_color(self, color):
        raise NotImplementedError

    def set_status_bar_background_color(self, color):
        raise NotImplementedError


class DrawerLayout(ViewGroup):
    """A simple control for displaying a drawer"""

    #: List of opened drawers
    opened = d_(List(View))

    #: Drawer width
    drawer_width = d_(Int(200))

    #: Title of drawer
    title = d_(Str())

    #: Gravity of title
    title_gravity = d_(Int())

    #: Elevation
    drawer_elevation = d_(Float())

    #: Set lock mode
    lock_mode = d_(Enum("unlocked", "locked_closed", "locked_open"))

    #: Set a color to use for the scrim that obscures primary content
    #: while a drawer is open.
    scrim_color = d_(Str())

    #: Statusbar background color
    status_bar_background_color = d_(Str())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyDrawerLayout)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe(
        "opened",
        "drawer_width",
        "title",
        "title_gravity",
        "drawer_elevation",
        "lock_mode",
        "scrim_color",
        "status_bar_background_color",
    )
    def _update_proxy(self, change):

        super()._update_proxy(change)
