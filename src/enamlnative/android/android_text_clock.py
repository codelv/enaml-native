"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.text_clock import ProxyTextClock

from .android_text_view import AndroidTextView, TextView
from .bridge import JavaMethod


class TextClock(TextView):
    __nativeclass__ = set_default('android.widget.TextClock')
    setFormat24Hour = JavaMethod('java.lang.CharSequence')
    setFormat24Hour = JavaMethod('java.lang.CharSequence')
    setTimeZone = JavaMethod('java.lang.String')


class AndroidTextClock(AndroidTextView, ProxyTextClock):
    """ An Android implementation of an Enaml ProxyTextClock.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TextClock)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = TextClock(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidTextClock, self).init_widget()
        d = self.declaration
        if d.format_12_hour:
            self.set_format_12_hour(d.format_12_hour)
        if d.format_24_hour:
            self.set_format_24_hour(d.format_24_hour)
        if d.time_zone:
            self.set_time_zone(d.time_zone)

    # -------------------------------------------------------------------------
    # ProxyTextClock API
    # -------------------------------------------------------------------------
    def set_format_12_hour(self, clock_format):
        self.widget.setFormat12Hour(clock_format)

    def set_format_24_hour(self, clock_format):
        self.widget.setFormat24Hour(clock_format)

    def set_time_zone(self, time_zone):
        self.widget.setTimeZone(time_zone)


