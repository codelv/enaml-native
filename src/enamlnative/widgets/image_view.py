"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Int, Unicode, Bool, Event, observe, set_default
)

from enaml.core.declarative import d_

from .view import View, ProxyView


class ProxyImageView(ProxyView):
    """ The abstract definition of a proxy relative layout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ImageView)

    def set_src(self, src):
        raise NotImplementedError

    def set_max_height(self, height):
        raise NotImplementedError

    def set_max_width(self, width):
        raise NotImplementedError


class ImageView(View):
    """ Displays image resources

    """

    #: Set the offset of the widget's text baseline from the widget's
    #: top boundary.
    # baseline = d_(Int(-1))
    #
    # baseline_align_bottom = d_(Bool())
    #
    # crop_to_padding = d_(Bool())

    #: Sets a drawable as the content of this ImageView.
    src = d_(Unicode())

    #: An optional argument to supply a maximum height for this view.
    max_height = d_(Int())

    #: An optional argument to supply a maximum width for this view.
    max_width = d_(Int())

    #: A reference to the ProxyImageView object.
    proxy = Typed(ProxyImageView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('src', 'max_height', 'max_width')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ImageView, self)._update_proxy(change)
