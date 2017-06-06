'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 25, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.time_picker import ProxyTimePicker

from .android_frame_layout import AndroidFrameLayout

Boolean = jnius.autoclass('java.lang.Boolean')
TimePicker = jnius.autoclass('android.widget.TimePicker')


class AndroidTimePicker(AndroidFrameLayout, ProxyTimePicker):
    """ An Android implementation of an Enaml ProxyFrameLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TimePicker)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

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

    #--------------------------------------------------------------------------
    # ProxyFrameLayout API
    #--------------------------------------------------------------------------
    def set_hour(self, hour):
        self.widget.setHour(hour)

    def set_minute(self, minute):
        self.widget.setMinute(minute)

    def set_hour_mode(self, mode):
        self.widget.setIs24HourView(Boolean(mode == '24'))

    def set_enabled(self, enabled):
        self.widget.setEnabled(enabled)
