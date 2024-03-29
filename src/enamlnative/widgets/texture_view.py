"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 10, 2018
"""
from atom.api import ForwardTyped, Typed
from .view import ProxyView, View


class ProxyTextureView(ProxyView):
    """The abstract definition of a proxy surface object."""

    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: TextureView)


class TextureView(View):
    """A TextureView can be used to display a content stream. Such a content
    stream can for instance be a video or an OpenGL scene. The content stream
    can come from the application's process as well as a remote process.

    """

    #: A reference to the ProxyViewGroup object.
    proxy = Typed(ProxyTextureView)
