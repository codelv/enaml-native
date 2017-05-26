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

from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyTabHost(ProxyFrameLayout):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: TabHost)

    def set_current_tab(self, index):
        raise NotImplementedError

class TabHost(FrameLayout):
    """ A tab

    """
    #: Sets the currently selected tab
    current_tab = d_(Int(0))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyTabHost)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('current_tab')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(TabHost, self)._update_proxy(change)
