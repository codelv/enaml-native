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

from enaml.widgets.widget import Widget, ProxyWidget


class ProxyLinearLayout(ProxyWidget):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: LinearLayout)

    def set_orientation(self, orientation):
        raise NotImplementedError

class LinearLayout(Widget):
    """ A simple control for displaying read-only text.

    """
    #: Should the layout be a column or a row.
    orientation = d_(Enum('horizontal', 'vertical'))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyLinearLayout)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('orientation')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(LinearLayout, self)._update_proxy(change)
