"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Enum, observe, set_default
)

from enaml.core.declarative import d_

from .text_view import TextView, ProxyTextView


class ProxyButton(ProxyTextView):
    """ The abstract definition of a proxy Button object.

    """
    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: Button)

    def set_style(self, style):
        raise NotImplementedError


class Button(TextView):
    """ A simple control for displaying a button.

    """
    #: Button is clickable by default
    clickable = set_default(True)

    #: Styles
    style = d_(Enum('', 'borderless', 'inset', 'small'))
    
    #: A reference to the proxy object.
    proxy = Typed(ProxyButton)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('style')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(Button, self)._update_proxy(change)