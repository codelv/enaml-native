"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Int, Unicode, Bool, observe
)

from enaml.core.declarative import d_

from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyViewAnimator(ProxyFrameLayout):
    """ The abstract definition of a proxy ViewAnimator object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: ViewAnimator)

    def set_animate_first_view(self, enabled):
        raise NotImplementedError

    def set_displayed_child(self, index):
        raise NotImplementedError
    
    def set_in_animation(self, animation):
        raise NotImplementedError
    
    def set_out_animation(self, animation):
        raise NotImplementedError


class ViewAnimator(FrameLayout):
    """ A simple control for a ViewAnimator.

    """
    #: Indicates whether the current View should be animated the first time
    #: the ViewAnimator is displayed.
    animate_first_view = d_(Bool(True))

    #: Sets which child view will be displayed.
    displayed_child = d_(Int(0))
    
    #: Specifies the animation used to animate a View that enters the screen.
    in_animation = d_(Unicode())
    
    #: Specifies the animation used to animate a View that exit the screen.
    out_animation = d_(Unicode())

    #: A reference to the ProxyViewAnimator object.
    proxy = Typed(ProxyViewAnimator)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('animate_first_view', 'displayed_child', 'in_animation',
             'out_animation')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ViewAnimator, self)._update_proxy(change)
