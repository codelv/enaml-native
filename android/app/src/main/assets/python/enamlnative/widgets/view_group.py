'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Int, Unicode, Enum, Event, observe, set_default
)

from enaml.core.declarative import d_

from .view import View, ProxyView


class ProxyViewGroup(ProxyView):
    """ The abstract definition of a proxy relative layout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ViewGroup)

    def set_layout_mode(self, mode):
        raise NotImplementedError

    def set_layout_gravity(self, gravity):
        raise NotImplementedError

    def set_layout_width(self, width):
        raise NotImplementedError

    def set_layout_height(self, height):
        raise NotImplementedError

class ViewGroup(View):
    """ ViewGroup is a view group that displays
        child views in relative positions.

    """
    #: Describes how the child views are positioned.
    #: Defaults to Gravity.START | Gravity.TOP.
    layout_mode = d_(Int())

    layout_width = d_(Unicode(''))

    layout_height = d_(Unicode(''))

    #: Layout gravity
    layout_gravity = d_(Enum(
        'top', 'left', 'right',
        'bottom','center',
        'end','start', 'no_gravity',
        'fill_horizontal'))

    #: A reference to the ProxyViewGroup object.
    proxy = Typed(ProxyViewGroup)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('layout_mode', 'layout_gravity',
             'layout_width', 'layout_height')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ViewGroup, self)._update_proxy(change)
