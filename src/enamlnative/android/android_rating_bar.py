"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 7, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.rating_bar import ProxyRatingBar

from .android_progress_bar import AndroidProgressBar, ProgressBar
from .bridge import JavaMethod, JavaCallback


class RatingBar(ProgressBar):
    __nativeclass__ = set_default('android.widget.RatingBar')
    setIsIndicator = JavaMethod('boolean')
    setMax = JavaMethod('int')
    setNumStars = JavaMethod('int')
    setOnRatingBarChangeListener = JavaMethod(
        'android.widget.RatingBar$OnRatingBarChangeListener')
    setRating = JavaMethod('float')
    setStepSize = JavaMethod('float')
    onRatingChanged = JavaCallback('android.widget.RatingBar', 'float',
                                   'boolean')


class AndroidRatingBar(AndroidProgressBar, ProxyRatingBar):
    """ An Android implementation of an Enaml ProxyRatingBar.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(RatingBar)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = RatingBar(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidRatingBar, self).init_widget()
        d = self.declaration
        if d.is_indicator:
            self.set_is_indicator(d.is_indicator)
        if d.num_stars:
            self.set_num_stars(d.num_stars)
        if d.step_size:
            self.set_step_size(d.step_size)

        self.set_rating(d.rating)

        #: Setup listener
        self.widget.setOnRatingBarChangeListener(self.widget.getId())
        self.widget.onRatingChanged.connect(self.on_rating_changed)

    # -------------------------------------------------------------------------
    # OnRatingBarChangeListener API
    # -------------------------------------------------------------------------
    def on_rating_changed(self, bar, rating, user):
        d = self.declaration
        with self.widget.setRating.suppressed():
            d.rating = rating

    # -------------------------------------------------------------------------
    # ProxyRatingBar API
    # -------------------------------------------------------------------------
    def set_is_indicator(self, indicator):
        self.widget.setIsIndicator(indicator)

    def set_num_stars(self, stars):
        self.widget.setNumStars(stars)

    def set_rating(self, rating):
        self.widget.setRating(rating)

    def set_step_size(self, size):
        self.widget.setStepSize(size)