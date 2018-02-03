"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Enum, Float, Unicode, Bool, observe, set_default
)

from enaml.core.declarative import d_

from .text_view import TextView, ProxyTextView
from .image_view import ImageView, ProxyImageView


class ProxyButton(ProxyTextView):
    """ The abstract definition of a proxy Button object.

    """
    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: Button)

    def set_flat(self, flat):
        raise NotImplementedError


class ProxyImageButton(ProxyImageView):
    """ The abstract definition of a proxy ImageButton object.

    """
    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: ImageButton)


class ProxyFloatingActionButton(ProxyImageButton):
    """ The abstract definition of a proxy FloatingActionButton object.

    """
    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: FloatingActionButton)

    def set_size(self, size):
        raise NotImplementedError

    def set_elevation(self, elevation):
        raise NotImplementedError

    def set_ripple_color(self, color):
        raise NotImplementedError

    def set_show(self, show):
        raise NotImplementedError


class Button(TextView):
    """ A simple control for displaying a button.

    """
    #: Button is clickable by default
    clickable = set_default(True)

    #: Use a flat style
    flat = d_(Bool())
    
    #: A reference to the proxy object.
    proxy = Typed(ProxyButton)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('flat')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(Button, self)._update_proxy(change)


class ImageButton(ImageView):
    """ A simple control for displaying a button with an Image.

    """
    #: ImageButton is clickable by default
    clickable = set_default(True)

    #: A reference to the proxy object.
    proxy = Typed(ProxyImageButton)


class FloatingActionButton(ImageButton):
    """ A simple control for displaying a floating button with an Image.

    """
    #: A reference to the proxy object.
    proxy = Typed(ProxyFloatingActionButton)

    #: Size of the button. Auto will resize to mini for small screens
    size = d_(Enum('normal', 'auto', 'mini'))

    #: Elevation to use
    elevation = d_(Float())

    #: Color of the ripple touch effect
    ripple_color = d_(Unicode())

    #: Show or hide the button
    show = d_(Bool(True))
