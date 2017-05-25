'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Int, Bool, Enum, observe
)

from enaml.core.declarative import d_

from .linear_layout import LinearLayout, ProxyLinearLayout


class ProxyTabWidget(ProxyLinearLayout):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: TabWidget)

    def set_enabled(self, enabled):
        raise NotImplementedError

    def set_hour(self, hour):
        raise NotImplementedError

    def set_minute(self, minute):
        raise NotImplementedError

    def set_hour_mode(self,mode):
        raise NotImplementedError

class TabWidget(LinearLayout):
    """ A simple control for displaying read-only text.

    """
    #: Set the enabled state of this view.
    enabled = d_(Bool(True))

    #: Sets the currently selected hour using 24-hour time.
    hour = d_(Int(0))

    #: Sets the currently selected minute.
    minute = d_(Int(0))

    #: Sets whether this widget displays time in 24-hour mode or 12-hour mode with an AM/PM picker.
    hour_mode = d_(Enum('24','12'))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyTabWidget)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('enabled','hour','minute','hour_mode')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(TabWidget, self)._update_proxy(change)
