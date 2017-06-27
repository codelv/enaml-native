'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed

from enamlnative.widgets.scroll_view import ProxyScrollView

from .android_frame_layout import AndroidFrameLayout, FrameLayout


class ScrollView(FrameLayout):
    __javaclass__ = 'android.widget.ScrollView'


class AndroidScrollView(AndroidFrameLayout, ProxyScrollView):
    """ An Android implementation of an Enaml ProxyFrameLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ScrollView)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ScrollView(self.get_context())


