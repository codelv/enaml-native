"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Instance, set_default

from enamlnative.widgets.scroll_view import ProxyScrollView

from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaMethod


class ScrollView(FrameLayout):
    __nativeclass__ = set_default('android.widget.ScrollView')
    smoothScrollBy = JavaMethod('int', 'int')
    smoothScrollTo = JavaMethod('int', 'int')
    fullScroll = JavaMethod('int')

    FOCUS_UP = 0x00000021
    FOCUS_DOWN = 0x00000082


class HorizontalScrollView(ScrollView):
    __nativeclass__ = set_default('android.widget.HorizontalScrollView')


class AndroidScrollView(AndroidFrameLayout, ProxyScrollView):
    """ An Android implementation of an Enaml ProxyFrameLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Instance(ScrollView)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        d = self.declaration
        if d.orientation == 'vertical':
            self.widget = ScrollView(self.get_context())
        else:
            self.widget = HorizontalScrollView(self.get_context())

    # -------------------------------------------------------------------------
    # ProxyScrollView API
    # -------------------------------------------------------------------------
    def set_orientation(self, orientation):
        #: Cannot be changed once set
        raise NotImplementedError(
            "ScrollView orientation cannot be changed dynamically.")

    def set_scroll_by(self, delta):
        self.widget.smoothScrollBy(*delta)

    def set_scroll_to(self, point):
        if point in ('top', 'bottom'):
            #: FOCUS_UP or FOCUS_DOWN
            #: TODO: This does not work!
            self.widget.fullScroll(
                ScrollView.FOCUS_UP
                if point == 'top' else ScrollView.FOCUS_DOWN)
        else:
            self.widget.smoothScrollTo(*point)

