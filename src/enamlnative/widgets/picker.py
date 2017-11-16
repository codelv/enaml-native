"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 6, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, List, Int, Bool, observe
)

from enaml.core.declarative import d_

from .linear_layout import LinearLayout, ProxyLinearLayout


class ProxyPicker(ProxyLinearLayout):
    """ The abstract definition of a proxy Picker object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Picker)

    def set_max_value(self, value):
        raise NotImplementedError

    def set_min_value(self, value):
        raise NotImplementedError

    def set_value(self, value):
        raise NotImplementedError

    def set_long_press_update_interval(self, interval):
        raise NotImplementedError

    def set_wraps(self, wraps):
        raise NotImplementedError

    def set_items(self, items):
        raise NotImplementedError


class Picker(LinearLayout):
    """ A simple control for displaying a Picker.

    """

    #: Formatter, hmm?

    #: Sets the max value of the picker
    max_value = d_(Int())

    #: Sets the min value of the picker.
    min_value = d_(Int())

    #: Set the current value or selected index for the picker.
    value = d_(Int())

    #: Items to display
    items = d_(List(basestring))

    #: Sets the speed at which the numbers be incremented and decremented
    #: when the up and down buttons are long pressed respectively.
    long_press_update_interval = d_(Int())

    #: Sets whether the selector wheel shown during flinging/scrolling
    #: should wrap around
    wraps = d_(Bool(True))

    #: A reference to the proxy object.
    proxy = Typed(ProxyPicker)

    # --------------------------------------------------------------------------
    # Observers
    # --------------------------------------------------------------------------
    @observe('max_value', 'min_value', 'value', 'items',
             'long_press_update_interval', 'wraps')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(Picker, self)._update_proxy(change)


