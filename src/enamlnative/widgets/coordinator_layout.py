"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Sept 18, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Int, Bool, Float, Tuple, observe
)

from enaml.core.declarative import d_

from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyCoordinatorLayout(ProxyFrameLayout):
    """ The abstract definition of a proxy CardVew object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: CoordinatorLayout)


class CoordinatorLayout(FrameLayout):
    """ By specifying Behaviors for child views of a CoordinatorLayout you can 
    provide many different interactions within a single parent and those views 
    can also interact with one another

    """

    #: A reference to the ProxyCoordinatorLayout object.
    proxy = Typed(ProxyCoordinatorLayout)

