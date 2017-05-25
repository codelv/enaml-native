#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Typed, ForwardTyped, Unicode, Float, Int, Bool, Enum, observe
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup

class ProxyDrawerLayout(ProxyViewGroup):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: DrawerLayout)

    def set_opened(self, opened):
        raise NotImplementedError

    def set_open_animated(self, animated):
        pass

    def set_open_gravity(self, gravity):
        pass

    def set_title(self, title):
        raise NotImplementedError

    def set_title_gravity(self, gravity):
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
    """ A simple control for displaying read-only text.

    """
    #: Set the enabled state of this view.
    opened = d_(Bool())

    #: Use animation when opening
    open_animated = d_(Bool(True))

    #: Open drawer gravity
    open_gravity = d_(Enum('top', 'left', 'right',
                           'bottom','center',
                           'end','start', 'no_gravity'))

    #: Title of drawer
    title = d_(Unicode())

    #: Gravity of title
    title_gravity = d_(Int())

    #: Elevation
    drawer_elevation = d_(Float())

    #: Set lock mode
    lock_mode = d_(Int())

    #: Set a color to use for the scrim that obscures primary content while a drawer is open.
    scrim_color = d_(Int())

    #: Statusbar background color
    status_bar_background_color = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyDrawerLayout)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('opened','open_gravity', 'open_animated', 'title', 'title_gravity',
             'drawer_elevation', 'drawer_lock_mode', 'scrim_color',
             'status_bar_background_color')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(DrawerLayout, self)._update_proxy(change)
