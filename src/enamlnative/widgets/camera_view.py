"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 10, 2018

@author: jrm
"""
from atom.api import Typed, ForwardTyped, Bool, observe
from .texture_view import TextureView, ProxyTextureView
from enaml.core.declarative import d_


class ProxyCameraView(ProxyTextureView):
    """ The abstract definition of a proxy surface object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: CameraView)
    
    def set_preview(self, show):
        raise NotImplementedError

    def take_picture(self):
        raise NotImplementedError


class CameraView(TextureView):
    """ A helper view to tie in a camera.

    """
    
    #: Display a preview
    preview = d_(Bool())
    
    #: A reference to the ProxyCameraView object.
    proxy = Typed(ProxyCameraView)
    
    @observe('preview')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(CameraView, self)._update_proxy(change)

    def take_picture(self):
        self.proxy.take_picture()

