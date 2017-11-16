"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Int, Bool, Float, Tuple, observe
)

from enaml.core.declarative import d_

from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyCardView(ProxyFrameLayout):
    """ The abstract definition of a proxy CardVew object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: CardView)

    def set_card_background_color(self, color):
        raise NotImplementedError
    
    def set_card_elevation(self, elevation):
        raise NotImplementedError

    def set_content_padding(self, padding):
        raise NotImplementedError

    def set_prevent_corner_overlap(self, enabled):
        raise NotImplementedError

    def set_radius(self, radius):
        raise NotImplementedError

    def set_use_compat_padding(self, enabled):
        raise NotImplementedError
    

class CardView(FrameLayout):
    """ A simple control for displaying read-only text.

    """

    #: Updates the corner radius of the CardView.
    card_background_color = d_(Unicode())

    #: Updates the corner radius of the CardView.
    card_elevation = d_(Float(-1))

    #: Sets the padding between the Card's edges and the children of CardView.
    content_padding = d_(Tuple(int))

    #: On pre-Lollipop platforms, CardView does not clip the bounds
    #: of the Card for the rounded corners.
    prevent_corner_overlap = d_(Bool())

    #: Updates the corner radius of the CardView.
    radius = d_(Float(-1))

    #: CardView adds additional padding to draw shadows on platforms
    #: before Lollipop.
    use_compat_padding = d_(Bool())

    #: A reference to the ProxyCardView object.
    proxy = Typed(ProxyCardView)

    @observe('card_background_color', 'card_elevation', 'content_padding'
             'prevent_corner_overlap', 'radius', 'use_compat_padding')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(CardView, self)._update_proxy(change)

