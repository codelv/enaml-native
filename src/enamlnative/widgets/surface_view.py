"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 9, 2018

@author: jrm
"""
from atom.api import Typed, ForwardTyped, Bool, observe
from .view import View, ProxyView
from enaml.core.declarative import d_


class ProxySurfaceView(ProxyView):
    """ The abstract definition of a proxy surface object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: SurfaceView)

    def set_secure(self, secure):
        raise NotImplementedError


class SurfaceView(View):
    """ SurfaceView provides a dedicated drawing surface embedded inside 
    of a view hierarchy. You can control the format of this surface and, 
    if you like, its size; the SurfaceView takes care of placing the 
    surface at the correct location on the screen

    """
    
    #: Control whether the surface view's content should be treated as 
    #: secure, preventing it from appearing in screenshots or from being 
    #: viewed on non-secure displays.
    secure = d_(Bool())

    #: A reference to the ProxyViewGroup object.
    proxy = Typed(ProxySurfaceView)

    @observe('secure')
    def _update_proxy(self, change):
        super(SurfaceView, self)._update_proxy(change)

