"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Float, ForwardTyped, Tuple, Typed
from enaml.core.declarative import d_, observe
from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyCardView(ProxyFrameLayout):
    """The abstract definition of a proxy CardVew object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: CardView)

    def set_elevation(self, elevation: float):
        raise NotImplementedError

    def set_radius(self, radius: float):
        raise NotImplementedError

    def set_content_padding(self, padding: tuple[int, ...]):
        raise NotImplementedError


class CardView(FrameLayout):
    """A simple control for displaying read-only text."""

    #: Updates the corner radius of the CardView.
    elevation = d_(Float(-1))

    #: Updates the corner radius of the CardView.
    radius = d_(Float(-1))

    #: Content padding of the CardView.
    content_padding = d_(Tuple(int))

    #: A reference to the ProxyCardView object.
    proxy = Typed(ProxyCardView)

    @observe("elevation", "radius", "content_padding")
    def _update_proxy(self, change):

        super()._update_proxy(change)
