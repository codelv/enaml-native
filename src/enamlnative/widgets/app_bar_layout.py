"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Mar 13, 2018

@author: jrm
"""
from atom.api import Typed, ForwardTyped, Bool, Int, observe
from enaml.core.declarative import d_
from .linear_layout import LinearLayout, ProxyLinearLayout


class ProxyAppBarLayout(ProxyLinearLayout):
    """ The abstract definition of a proxy AppBarLayout object.

    """
    #: A reference to the AppBarLayout declaration.
    declaration = ForwardTyped(lambda: AppBarLayout)

    def set_expanded(self, expanded):
        raise NotImplementedError


class AppBarLayout(LinearLayout):
    """ AppBarLayout is a vertical LinearLayout which implements many of the 
    features of material designs app bar concept, namely scrolling gestures. 

    """

    #: A reference to the ProxyAppBarLayout object.
    proxy = Typed(ProxyAppBarLayout)   

    #: Sets whether this AppBarLayout is expanded or not, animating if it has
    #: already been laid out.
    expanded = d_(Bool(True))

    #: The vertical offset for the parent AppBarLayout, in px
    vertical_offset = d_(Int(), writable=False)

    @observe('expanded')
    def _update_proxy(self, change):
        super(AppBarLayout, self)._update_proxy(change)
