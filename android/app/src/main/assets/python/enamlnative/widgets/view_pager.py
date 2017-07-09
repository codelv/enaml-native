'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Unicode, List, Float, Int,  observe, set_default
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup
from .fragment import  Fragment


class ProxyViewPager(ProxyViewGroup):
    """ The abstract definition of a proxy ViewPager object.

    """
    #: A reference to the ViewPager declaration.
    declaration = ForwardTyped(lambda: ViewPager)

    def set_current_index(self, index):
        raise NotImplementedError

    def set_offscreen_page_limit(self, limit):
        raise NotImplementedError

    def set_page_margin(self, margin):
        raise NotImplementedError


class ProxyPagerTitleStrip(ProxyViewGroup):
    """ The abstract definition of a proxy PagerTitleStrip object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: PagerTitleStrip)

    def set_titles(self, titles):
        raise NotImplementedError

    def set_inactive_alpha(self, alpha):
        raise NotImplementedError

    def set_text_color(self, color):
        raise NotImplementedError

    def set_text_size(self, size):
        raise NotImplementedError

    def set_text_spacing(self, spacing):
        raise NotImplementedError


class ProxyPagerTabStrip(ProxyPagerTitleStrip):
    """ The abstract definition of a proxy PagerTabStrip object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: PagerTabStrip)

    def set_tab_indicator_color(self, color):
        raise NotImplementedError


class ViewPager(ViewGroup):
    """ Layout manager that allows the user to flip left and right through pages of data.

    """
    #: Set the currently selected page.
    current_index = d_(Int())

    #: Set the number of pages that should be retained to either side 
    #: of the current page in the view hierarchy in an idle state.
    offscreen_page_limit = d_(Int())

    #: Set the margin between pages.
    page_margin = d_(Int(-1))

    #: Read only list of pages
    pages = property(lambda self: [c for c in self._children if isinstance(c, Fragment)])

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyViewPager)

    # --------------------------------------------------------------------------
    # Observers
    # --------------------------------------------------------------------------
    @observe('current_index', 'offscreen_page_limit','page_margin')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ViewPager, self)._update_proxy(change)


class PagerTitleStrip(ViewGroup):

    #: Titles to use
    titles = d_(List(basestring))

    #: Update defaults
    layout_width = set_default("match_parent")
    layout_height = set_default("wrap_content")
    layout_gravity = set_default("top")

    #: Set the alpha value used for non-primary page titles.
    inactive_alpha = d_(Float())

    # Set the color value used as the base color for all displayed page titles.
    text_color = d_(Unicode())

    #: Set the default text size to a given unit and value. Forced to DP
    text_size = d_(Int())

    #: Spacing pixels
    text_spacing = d_(Int())

    # --------------------------------------------------------------------------
    # Observers
    # --------------------------------------------------------------------------
    @observe('titles', 'text_color', 'text_size', 'text_spacing')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(PagerTitleStrip, self)._update_proxy(change)


class PagerTabStrip(PagerTitleStrip):

    #: Set the color of the tab indicator bar.
    tab_indicator_color = d_(Unicode())

    # --------------------------------------------------------------------------
    # Observers
    # --------------------------------------------------------------------------
    @observe('tab_indicator_color')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(PagerTabStrip, self)._update_proxy(change)

