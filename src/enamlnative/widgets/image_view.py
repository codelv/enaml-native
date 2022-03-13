"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import ForwardTyped, Int, Str, Typed
from enaml.core.declarative import d_, observe
from .view import ProxyView, View


class ProxyImageView(ProxyView):
    """The abstract definition of a proxy relative layout object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ImageView)

    def set_src(self, src: str):
        raise NotImplementedError

    def set_max_height(self, height: int):
        raise NotImplementedError

    def set_max_width(self, width: int):
        raise NotImplementedError


class ImageView(View):
    """Displays image resources"""

    #: Set the offset of the widget's text baseline from the widget's
    #: top boundary.
    # baseline = d_(Int(-1))
    #
    # baseline_align_bottom = d_(Bool())
    #
    # crop_to_padding = d_(Bool())

    #: Sets a drawable as the content of this ImageView.
    src = d_(Str())

    #: An optional argument to supply a maximum height for this view.
    max_height = d_(Int())

    #: An optional argument to supply a maximum width for this view.
    max_width = d_(Int())

    #: A reference to the ProxyImageView object.
    proxy = Typed(ProxyImageView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("src", "max_height", "max_width")
    def _update_proxy(self, change):

        super()._update_proxy(change)
