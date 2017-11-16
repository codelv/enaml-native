"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 22, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.swipe_refresh_layout import ProxySwipeRefreshLayout

from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaMethod, JavaCallback


class SwipeRefreshLayout(ViewGroup):
    __nativeclass__ = set_default(
        'android.support.v4.widget.SwipeRefreshLayout')
    setDistanceToTriggerSync = JavaMethod('int')
    setRefreshing = JavaMethod('boolean')
    setEnabled = JavaMethod('boolean')
    setProgressBackgroundColorSchemeColor = JavaMethod(
        'android.graphics.Color')
    setColorSchemeColors = JavaMethod('[Landroid.graphics.Color;')

    setOnRefreshListener = JavaMethod(
        'android.support.v4.widget.SwipeRefreshLayout$OnRefreshListener')
    onRefresh = JavaCallback()


class AndroidSwipeRefreshLayout(AndroidViewGroup, ProxySwipeRefreshLayout):
    """ An Android implementation of an Enaml ProxySwipeRefreshLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(SwipeRefreshLayout)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = SwipeRefreshLayout(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidSwipeRefreshLayout, self).init_widget()
        d = self.declaration
        if not d.enabled:
            self.set_enabled(d.enabled)
        if d.indicator_background_color:
            self.set_indicator_background_color(d.indicator_background_color)
        if d.indicator_color:
            self.set_indicator_color(d.indicator_color)
        if d.trigger_distance:
            self.set_trigger_distance(d.trigger_distance)
        self.widget.onRefresh.connect(self.on_refresh)
        self.widget.setOnRefreshListener(self.widget.getId())

    # -------------------------------------------------------------------------
    # OnRefreshListener API
    # -------------------------------------------------------------------------
    def on_refresh(self):
        d = self.declaration
        d.refreshed()
        #: Stop the refresh indicator
        self.widget.setRefreshing(False)

    # -------------------------------------------------------------------------
    # ProxySwipeRefreshLayout API
    # -------------------------------------------------------------------------
    def set_indicator_background_color(self, color):
        self.widget.setProgressBackgroundColorSchemeColor(color)

    def set_indicator_color(self, color):
        self.widget.setColorSchemeColors((color,))

    def set_trigger_distance(self, distance):
        self.widget.setDistanceToTriggerSync(distance)

    def set_refreshed(self, refreshed):
        #: Show the refreshed indicator
        self.widget.setRefresh(refreshed)
