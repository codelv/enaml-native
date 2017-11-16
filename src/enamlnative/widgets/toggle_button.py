"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 7, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, observe
)

from enaml.core.declarative import d_

from .compound_button import CompoundButton, ProxyCompoundButton


class ProxyToggleButton(ProxyCompoundButton):
    """ The abstract definition of a proxy ToggleButton object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ToggleButton)

    def set_text_off(self, text):
        raise NotImplementedError

    def set_text_on(self, text):
        raise NotImplementedError


class ToggleButton(CompoundButton):
    """ A simple control for displaying a ToggleButton.

    """

    #: Sets the text for when the button is not in the checked state.
    text_off = d_(Unicode())

    #: Sets the text for when the button is in the checked state.
    text_on = d_(Unicode())

    #: A reference to the ProxyToggleButton object.
    proxy = Typed(ProxyToggleButton)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('text_off', 'text_on')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ToggleButton, self)._update_proxy(change)


