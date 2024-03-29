"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Enum, ForwardTyped, Typed
from enaml.core.declarative import d_, observe
from .view import ProxyView, View


class ProxyViewGroup(ProxyView):
    """The abstract definition of a proxy relative layout object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ViewGroup)

    def set_transition(self, transition):
        raise NotImplementedError


class ViewGroup(View):
    """ViewGroup is a view group that displays
    child views in relative positions.

    """

    # A layout transition for when children are added or removed
    transition = d_(Enum("", "default"))

    #: A reference to the ProxyViewGroup object.
    proxy = Typed(ProxyViewGroup)

    @observe("transition")
    def _update_proxy(self, change):
        super()._update_proxy(change)
