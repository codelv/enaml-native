#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Typed, ForwardTyped, Unicode, Enum, Event, observe, set_default
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup


class ProxyLinearLayout(ProxyViewGroup):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: LinearLayout)

    def set_orientation(self, orientation):
        raise NotImplementedError

    def set_gravity(self, gravity):
        raise NotImplementedError

class LinearLayout(ViewGroup):
    """ A simple control for displaying read-only text.

    """
    #: Should the layout be a column or a row.
    orientation = d_(Enum('horizontal', 'vertical'))

    #: Layout gravity
    gravity = d_(Enum('top', 'left', 'right',
                      'bottom','center',
                      'end','start', 'no_gravity',
                      'fill_horizontal'))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyLinearLayout)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('orientation','gravity')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(LinearLayout, self)._update_proxy(change)
