'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Int,  observe
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup


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

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyViewPager)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('current_index','offscreen_page_limit','page_margin')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ViewPager, self)._update_proxy(change)
