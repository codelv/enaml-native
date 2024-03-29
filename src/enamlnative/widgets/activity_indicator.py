"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 26, 2017
"""
from atom.api import Enum, ForwardTyped, Str, Typed, observe
from enaml.core.declarative import d_
from .view import ProxyView, View


class ProxyActivityIndicator(ProxyView):
    """The abstract definition of a proxy ActivityIndicator object."""

    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: ActivityIndicator)

    def set_size(self, size):
        raise NotImplementedError

    def set_color(self, color):
        raise NotImplementedError


class ActivityIndicator(View):
    """A simple control for displaying an ActivityIndicator."""

    #: Style for indeterminate
    size = d_(Enum("normal", "small", "large"))

    #: Sets the color of the indicator.
    color = d_(Str())

    #: A reference to the ProxyActivityIndicator object.
    proxy = Typed(ProxyActivityIndicator)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("size", "color")
    def _update_proxy(self, change):

        super()._update_proxy(change)
