'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 7, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.card_view import ProxyCardView

from .android_frame_layout import AndroidFrameLayout

#: You must add "compile 'com.android.support:cardview-v7:21.0.+'" to build.gradle
CardView = jnius.autoclass('android.support.v7.widget.CardView')


class AndroidCardView(AndroidFrameLayout, ProxyCardView):
    """ An Android implementation of an Enaml ProxyCardView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(CardView)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying Android widget.

        """
        self.widget = CardView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidCardView, self).init_widget()
        d = self.declaration

        if d.card_background_color:
            self.set_card_background_color(d.card_background_color)
        if d.card_elevation >= 0:
            self.set_card_elevation(d.card_elevation)
        if d.content_padding:
            self.set_content_padding(d.content_padding)
        if d.prevent_corner_overlap:
            self.widget.setPreventCornerOverlap(d.prevent_corner_overlap)
        if d.radius >= 0:
            self.widget.setRadius(d.radius)
        if d.use_compat_padding:
            self.set_use_compat_padding(d.use_compat_padding)


    #--------------------------------------------------------------------------
    # ProxyCardView API
    #--------------------------------------------------------------------------
    def set_card_background_color(self, color):
        self.widget.setCardBackgroundColor(color)

    def set_card_elevation(self, elevation):
        self.widget.setCardElevation(elevation)

    def set_content_padding(self, padding):
        dp = self.dp
        l, t, r, b = padding
        self.widget.setContentPadding(l*dp,t*dp,r*dp,b*dp)

    def set_prevent_corner_overlap(self, enabled):
        self.widget.setPreventCornerOverlap(enabled)

    def set_radius(self, radius):
        self.widget.setRadius(radius)

    def set_use_compat_padding(self, enabled):
        self.widget.setUseCompatPadding(enabled)