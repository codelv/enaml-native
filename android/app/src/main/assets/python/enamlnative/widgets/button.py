'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, set_default
)

from enaml.core.declarative import d_

from .text_view import TextView, ProxyTextView


class ProxyButton(ProxyTextView):
    """ The abstract definition of a proxy Button object.

    """
    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: Button)


class Button(TextView):
    """ A simple control for displaying read-only text.

    """
    #: Button is clickable by default
    clickable = set_default(True)
    
    #: A reference to the proxy object.
    proxy = Typed(ProxyButton)

