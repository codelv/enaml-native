"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Int, Enum, observe, set_default
)

from enaml.core.declarative import d_
from .frame_layout import FrameLayout, ProxyFrameLayout
from .view_pager import PagerFragment, ProxyPagerFragment


class ProxyTabLayout(ProxyFrameLayout):
    """ The abstract definition of a proxy TabLayout object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: TabLayout)

    def set_current_tab(self, index):
        raise NotImplementedError

    def set_tab_mode(self, mode):
        raise NotImplementedError

    def set_tab_gravity(self, gravity):
        raise NotImplementedError

    def set_tab_indicator_color_selected(self, color):
        raise NotImplementedError

    def set_tab_indicator_height(self, height):
        raise NotImplementedError

    def set_tab_color(self, color):
        raise NotImplementedError

    def set_tab_color_selected(self, color):
        raise NotImplementedError


class ProxyTabFragment(ProxyPagerFragment):
    """ The abstract definition of a proxy TabFragment object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: TabFragment)


class TabLayout(FrameLayout):
    """ A TabLayout contains a tab for each TabFragment child of a ViewPager

    """
    #: Layout params
    layout_width = set_default('match_parent')
    layout_height = set_default('wrap_content')
    layout_gravity = set_default('top')

    #: Set the behavior mode for the Tabs in this layout.
    tab_mode = d_(Enum('fixed', 'scrollable'))

    #: Set the gravity to use when laying out the tabs.
    tab_gravity = d_(Enum('fill', 'center'))

    #: Sets the tab indicator's color for the currently selected tab.
    tab_indicator_color_selected = d_(Unicode())

    #: Sets the tab indicator's height for the currently selected tab.
    tab_indicator_height = d_(Int())

    #: Tab normal color
    tab_color = d_(Unicode())

    #: Tab color selected
    tab_color_selected = d_(Unicode())

    #: Currently selected tab title
    current_tab = d_(ForwardTyped(lambda: TabFragment))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyTabLayout)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('tabs', 'tab_mode', 'tab_gravity', 'current_tab',
             'tab_indicator_color_selected', 'tab_indicator_height',
             'tab_color', 'tab_color_selected')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(TabLayout, self)._update_proxy(change)


class TabFragment(PagerFragment):
    """ A TabFragment alias for a PagerFragment

    """
    #: A reference to the ProxyTabFragment object.
    proxy = Typed(ProxyTabFragment)


