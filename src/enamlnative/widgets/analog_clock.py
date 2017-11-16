"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, observe
)

from enaml.core.declarative import d_

from .view import View, ProxyView


class ProxyAnalogClock(ProxyView):
    """ The abstract definition of a proxy AnalogClock object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: AnalogClock)


class AnalogClock(View):
    """ A simple control for displaying an AnalogClock

    """

    #: A reference to the proxy object.
    proxy = Typed(ProxyAnalogClock)
