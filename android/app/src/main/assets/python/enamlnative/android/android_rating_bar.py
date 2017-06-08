'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 7, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.rating_bar import ProxyRatingBar

from .android_progress_bar import AndroidProgressBar

RatingBar = jnius.autoclass('android.widget.RatingBar')


class OnRatingBarChangeListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/widget/RatingBar$OnRatingBarChangeListener']

    def __init__(self, handler):
        self.__handler__ = handler
        super(OnRatingBarChangeListener, self).__init__()

    @jnius.java_method('(Landroid/widget/RatingBar;FZ)V')
    def onRatingChanged(self, ratingBar, rating, fromUser):
        self.__handler__.on_rating_changed(ratingBar, rating, fromUser)


class AndroidRatingBar(AndroidProgressBar, ProxyRatingBar):
    """ An Android implementation of an Enaml ProxyRatingBar.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(RatingBar)

    rating_listener = Typed(OnRatingBarChangeListener)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying Android widget.

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

        self.rating_listener = OnRatingBarChangeListener(self)
        self.widget.setOnRatingBarChangeListener(self.rating_listener)

    # --------------------------------------------------------------------------
    # OnRatingBarChangeListener API
    # --------------------------------------------------------------------------

    def on_rating_changed(self, bar, rating, user):
        d = self.declaration
        d.rating = rating

    # --------------------------------------------------------------------------
    # ProxyRatingBar API
    # --------------------------------------------------------------------------

    def set_is_indicator(self, indicator):
        self.widget.setIsIndicator(indicator)

    def set_num_stars(self, stars):
        self.widget.setNumStars(stars)

    def set_rating(self, rating):
        self.widget.setRating(rating)

    def set_step_size(self, size):
        self.widget.setStepSize(size)