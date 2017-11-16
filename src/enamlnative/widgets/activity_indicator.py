"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 26, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Enum, Unicode, observe
)

from enaml.core.declarative import d_
from .view import View, ProxyView


class ProxyActivityIndicator(ProxyView):
    """ The abstract definition of a proxy ActivityIndicator object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: ActivityIndicator)

    def set_style(self, style):
        raise NotImplementedError

    def set_color(self, color):
        raise NotImplementedError


class ActivityIndicator(View):
    """ A simple control for displaying an ActivityIndicator.

    """

    #: Style for indeterminate
    style = d_(Enum('normal', 'small', 'large'))

    #: Sets the color of the indicator.
    color = d_(Unicode())

    #: A reference to the ProxyActivityIndicator object.
    proxy = Typed(ProxyActivityIndicator)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('style', 'color')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ActivityIndicator, self)._update_proxy(change)
