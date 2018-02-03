"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, ForwardTyped
from .view import View, ProxyView


class ProxyViewGroup(ProxyView):
    """ The abstract definition of a proxy relative layout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ViewGroup)


class ViewGroup(View):
    """ ViewGroup is a view group that displays
    child views in relative positions.

    """
    #: A reference to the ProxyViewGroup object.
    proxy = Typed(ProxyViewGroup)
