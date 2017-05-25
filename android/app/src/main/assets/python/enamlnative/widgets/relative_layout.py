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

from enaml.widgets.widget import Widget, ProxyWidget

class ProxyRelativeLayout(ProxyWidget):
    """ The abstract definition of a proxy relative layout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: RelativeLayout)

    def set_gravity(self, gravity):
        raise NotImplementedError

    def set_horizontal_gravity(self, gravity):
        raise NotImplementedError

    def set_vertical_gravity(self, gravity):
        raise NotImplementedError

class RelativeLayout(Widget):
    """ RelativeLayout is a view group that displays
        child views in relative positions.

    """
    #: Describes how the child views are positioned.
    #: Defaults to Gravity.START | Gravity.TOP.
    gravity = d_(Int())

    #:
    horizontal_gravity = d_(Int())

    #:
    vertical_gravity = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyRelativeLayout)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('gravity','horizontal_gravity','vertical_gravity')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(RelativeLayout, self)._update_proxy(change)
