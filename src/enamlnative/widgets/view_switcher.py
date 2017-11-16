"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, observe
)

from enaml.core.declarative import d_

from .view_animator import ViewAnimator, ProxyViewAnimator


class ProxyViewSwitcher(ProxyViewAnimator):
    """ The abstract definition of a proxy ViewSwitcher object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: ViewSwitcher)


class ViewSwitcher(ViewAnimator):
    """ A simple control for a ViewSwitcher.

    """
    
    #: A reference to the ProxyViewSwitcher object.
    proxy = Typed(ProxyViewSwitcher)

