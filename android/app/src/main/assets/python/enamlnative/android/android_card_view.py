'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.card_view import ProxyCardView

from .android_frame_layout import AndroidFrameLayout

CardView = jnius.autoclass('android.support.v7.widget.CardView')


class AndroidCardView(AndroidFrameLayout, ProxyCardView):
    """ An Android implementation of an Enaml ProxyCardView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(CardView)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying Android widget.

        """
        self.widget = CardView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidCardView, self).init_widget()
        d = self.declaration

    # --------------------------------------------------------------------------
    # ProxyCardView API
    # --------------------------------------------------------------------------
