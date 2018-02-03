"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.toolbar import ProxyToolbar

from .android_view_group import AndroidViewGroup, ViewGroup, MarginLayoutParams
from .bridge import JavaMethod, JavaCallback, JavaField


class Toolbar(ViewGroup):
    __nativeclass__ = set_default('android.support.v7.widget.Toolbar')
    setTitle = JavaMethod('java.lang.CharSequence')
    setSubtitle = JavaMethod('java.lang.CharSequence')
    setSubtitleTextColor = JavaMethod('android.graphics.Color')
    setTitleMargin = JavaMethod('int', 'int', 'int', 'int')
    setTitleTextColor = JavaMethod('android.graphics.Color')
    setNavigationOnClickListener = JavaMethod(
        'android.view.View$OnClickListener')
    setOnMenuItemClickListener = JavaMethod(
        'android.widget.Toolbar$OnMenuItemClickListener')
    setContentInsetsAbsolute = JavaMethod('int', 'int')
    setContentInsetsRelative = JavaMethod('int', 'int')
    onNavigationClick = JavaCallback('android.view.View')
    onMenuItemClick = JavaCallback('android.view.MenuItem')


class ToolbarLayoutParams(MarginLayoutParams):
    __nativeclass__ = set_default(
        'android.support.v7.widget.Toolbar$LayoutParams')
    gravity = JavaField('int')


class AndroidToolbar(AndroidViewGroup, ProxyToolbar):
    """ An Android implementation of an Enaml ProxyToolbar.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Toolbar)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = Toolbar(self.get_context())

    # -------------------------------------------------------------------------
    # ProxyToolbar API
    # -------------------------------------------------------------------------
    def set_content_padding(self, padding):
        # Left right
        self.widget.setContentInsetsAbsolute(padding[0], padding[2])
        # Start, end
        self.widget.setContentInsetsRelative(padding[1], padding[3])

    def set_title(self, text):
        self.widget.setTitle(text)

    def set_subtitle(self, text):
        self.widget.setSubtitle(text)

    def set_title_margins(self, margins):
        self.widget.setTitleMargin(*margins)

    def set_title_color(self, color):
        self.widget.setTitleTextColor(color)

    def set_subtitle_color(self, color):
        self.widget.setSubtitleTextColor(color)
