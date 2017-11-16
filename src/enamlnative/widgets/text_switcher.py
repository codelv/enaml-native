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

from .view_switcher import ViewSwitcher, ProxyViewSwitcher


class ProxyTextSwitcher(ProxyViewSwitcher):
    """ The abstract definition of a proxy TextSwitcher object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: TextSwitcher)


class TextSwitcher(ViewSwitcher):
    """ A simple control for a TextSwitcher.

    """
    
    #: Sets the text of the text view that is currently showing.
    current_text = d_(Unicode())
    
    #: Sets the text of the next view and switches to the next view.
    text = d_(Unicode())

    #: A reference to the ProxyTextSwitcher object.
    proxy = Typed(ProxyTextSwitcher)

