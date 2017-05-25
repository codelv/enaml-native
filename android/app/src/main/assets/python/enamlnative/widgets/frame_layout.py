#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Typed, ForwardTyped, Int, Bool, observe
)

from enaml.core.declarative import d_

from enaml.widgets.widget import Widget, ProxyWidget

class ProxyFrameLayout(ProxyWidget):
    """ The abstract definition of a proxy relative layout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: FrameLayout)

    def set_foreground_gravity(self, gravity):
        raise NotImplementedError

    def set_measure_all_children(self, enabled):
        raise NotImplementedError

class FrameLayout(Widget):
    """ FrameLayout is a view group that displays
        child views in relative positions.

    """
    #: Describes how the child views are positioned.
    #: Defaults to Gravity.START | Gravity.TOP.
    foreground_gravity = d_(Int())

    measure_all_children = d_(Bool())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyFrameLayout)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('foreground_gravity','measure_all_children')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(FrameLayout, self)._update_proxy(change)
