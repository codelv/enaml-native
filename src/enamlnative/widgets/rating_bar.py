"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 7, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Float, Int, Bool, observe, set_default
)

from enaml.core.declarative import d_

from .progress_bar import ProgressBar, ProxyProgressBar


class ProxyRatingBar(ProxyProgressBar):
    """ The abstract definition of a proxy RatingBar object.

    """
    #: A reference to the RatingBar declaration.
    declaration = ForwardTyped(lambda: RatingBar)

    def set_is_indicator(self, indicator):
        raise NotImplementedError

    def set_num_stars(self, stars):
        raise NotImplementedError

    def set_rating(self, rating):
        raise NotImplementedError

    def set_step_size(self, size):
        raise NotImplementedError


class RatingBar(ProgressBar):
    """ A simple control for displaying read-only text.

    """

    #: Whether this rating bar should only be an indicator
    #: (thus non-changeable by the user).
    is_indicator = d_(Bool())

    #: The number of stars set (via setNumStars(int) or in an XML layout)
    #: will be shown when the layout width is set to wrap content
    #: (if another layout width is set, the results may be unpredictable).
    layout_width = set_default('wrap_content')

    #: Sets the number of stars to show.
    num_stars = d_(Int())

    #: Sets the rating (the number of stars filled).
    rating = d_(Float(strict=False))

    #: Sets the step size (granularity) of this rating bar.
    step_size = d_(Float(strict=False))

    #: A reference to the RatingBar object.
    proxy = Typed(ProxyRatingBar)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('is_indicator', 'num_stars', 'rating', 'step_size')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(RatingBar, self)._update_proxy(change)
