"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 25, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.time_picker import ProxyTimePicker

from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaMethod, JavaCallback


class TimePicker(FrameLayout):
    __nativeclass__ = set_default('android.widget.TimePicker')
    onTimeChanged = JavaCallback('android.widget.TimePicker', 'int', 'int')
    setHour = JavaMethod('int')
    setMinute = JavaMethod('int')
    setCurrentHour = JavaMethod('java.lang.Integer')
    setCurrentMinute = JavaMethod('java.lang.Integer')
    setEnabled = JavaMethod('boolean')
    setIs24HourView = JavaMethod('java.lang.Boolean')
    setOnTimeChangedListener = JavaMethod(
        'android.widget.TimePicker$OnTimeChangedListener')


class AndroidTimePicker(AndroidFrameLayout, ProxyTimePicker):
    """ An Android implementation of an Enaml ProxyTimePicker.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TimePicker)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = TimePicker(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidTimePicker, self).init_widget()
        d = self.declaration
        self.set_hour(d.hour)
        self.set_minute(d.minute)
        self.set_hour_mode(d.hour_mode)
        self.set_enabled(d.enabled)

        self.widget.setOnTimeChangedListener(self.widget.getId())
        self.widget.onTimeChanged.connect(self.on_time_changed)

    # -------------------------------------------------------------------------
    # OnTimeChangedListener API
    # -------------------------------------------------------------------------
    def on_time_changed(self, view, hour, minute):
        d = self.declaration
        with self.widget.setHour.suppressed():
            d.hour = hour
        with self.widget.setMinute.suppressed():
            d.minute = minute

    # -------------------------------------------------------------------------
    # ProxyFrameLayout API
    # -------------------------------------------------------------------------
    def set_hour(self, hour):
        if self.get_context().api_level < 23:
            self.widget.setCurrentHour(hour)
        else:
            self.widget.setHour(hour)

    def set_minute(self, minute):

        if self.get_context().api_level < 23:
            self.widget.setCurrentMinute(minute)
        else:
            self.widget.setMinute(minute)

    def set_hour_mode(self, mode):
        self.widget.setIs24HourView(mode == '24')

    def set_enabled(self, enabled):
        self.widget.setEnabled(enabled)
