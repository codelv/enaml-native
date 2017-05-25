#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Typed, ForwardTyped, Int, Enum, Event, observe, set_default
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

class ViewGroup(View):
    """ ViewGroup is a view group that displays
        child views in relative positions.

    """
    #: Describes how the child views are positioned.
    #: Defaults to Gravity.START | Gravity.TOP.
    layout_mode = d_(Int())

    #: A reference to the ProxyViewGroup object.
    proxy = Typed(ProxyViewGroup)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('layout_mode')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ViewGroup, self)._update_proxy(change)
