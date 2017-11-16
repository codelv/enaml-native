"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, ForwardTyped
from .view import View, ProxyView


class ProxySpacer(ProxyView):
    """ The abstract definition of a proxy Spacer object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Spacer)


class Spacer(View):
    """ A simple control for displaying an Spacer

    """

    #: A reference to the proxy object.
    proxy = Typed(ProxySpacer)
