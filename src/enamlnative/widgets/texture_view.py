"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 10, 2018

@author: jrm
"""
from atom.api import Typed, ForwardTyped, Bool, observe
from .view import View, ProxyView
from enaml.core.declarative import d_


class ProxyTextureView(ProxyView):
    """ The abstract definition of a proxy surface object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: TextureView)


class TextureView(View):
    """ A TextureView can be used to display a content stream. Such a content 
    stream can for instance be a video or an OpenGL scene. The content stream 
    can come from the application's process as well as a remote process.

    """
    
    #: A reference to the ProxyViewGroup object.
    proxy = Typed(ProxyTextureView)
