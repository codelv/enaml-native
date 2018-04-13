"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Mar 13, 2018

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.app_bar_layout import ProxyAppBarLayout

from .android_linear_layout import AndroidLinearLayout, LinearLayout
from .bridge import JavaMethod, JavaCallback


class AppBarLayout(LinearLayout):
    __nativeclass__ = set_default(
        'android.support.design.widget.AppBarLayout')
    __signature__ = set_default(('android.content.Context',))

    addOnOffsetChangedListener = JavaMethod(
        'android.support.design.widget.AppBarLayout$OnOffsetChangedListener')
    removeOnOffsetChangedListener = JavaMethod(
        'android.support.design.widget.AppBarLayout$OnOffsetChangedListener')

    setExpanded = JavaMethod('boolean')

    onOffsetChanged = JavaCallback(
        'android.support.design.widget.AppBarLayout', 'int')


class AndroidAppBarLayout(AndroidLinearLayout, ProxyAppBarLayout):
    """ An Android implementation of an Enaml ProxyAppBarLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(AppBarLayout)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = AppBarLayout(self.get_context())

    def init_widget(self):
        super(AndroidAppBarLayout, self).init_widget()
        w = self.widget
        w.addOnOffsetChangedListener(w.getId())
        w.onOffsetChanged.connect(self.on_offset_changed)

    def on_offset_changed(self, layout, offset):
        d = self.declaration
        d.vertical_offset = offset

    def set_expanded(self, expanded):
        self.widget.setExpanded(expanded)
