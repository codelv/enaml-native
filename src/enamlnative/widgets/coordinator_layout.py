"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Sept 18, 2017
"""
from atom.api import ForwardTyped, Typed
from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyCoordinatorLayout(ProxyFrameLayout):
    """The abstract definition of a proxy CardVew object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: CoordinatorLayout)


class CoordinatorLayout(FrameLayout):
    """By specifying Behaviors for child views of a CoordinatorLayout you can
    provide many different interactions within a single parent and those views
    can also interact with one another

    """

    #: A reference to the ProxyCoordinatorLayout object.
    proxy = Typed(ProxyCoordinatorLayout)
