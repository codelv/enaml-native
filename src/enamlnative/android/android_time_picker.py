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


class OnTimeChangedListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/widget/TimePicker$OnTimeChangedListener']

    def __init__(self, handler):
        self.__handler__ = handler
        super(OnTimeChangedListener, self).__init__()

    @jnius.java_method('(Landroid/widget/TimePicker;II)V')
    def onTimeChanged(self, view, hour, minute):
        self.__handler__.on_time_changed(view, hour, minute)



class AndroidTimePicker(AndroidFrameLayout, ProxyTimePicker):
    """ An Android implementation of an Enaml ProxyTimePicker.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TimePicker)

    #: Save a reference to the time changed listener
    time_listener = Typed(OnTimeChangedListener)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
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

        self.time_listener = OnTimeChangedListener(self)
        self.widget.setOnTimeChangedListener(self.time_listener)

    # --------------------------------------------------------------------------
    # OnTimeChangedListener API
    # --------------------------------------------------------------------------
    def on_time_changed(self, view, hour, minute):
        d = self.declaration
        with self.suppress_notifications():
            d.hour = hour
            d.minute = minute

    # --------------------------------------------------------------------------
    # ProxyFrameLayout API
    # --------------------------------------------------------------------------
    def set_hour(self, hour):
        self.widget.setHour(hour)

    def set_minute(self, minute):
        self.widget.setMinute(minute)

    def set_hour_mode(self, mode):
        self.widget.setIs24HourView(Boolean(mode == '24'))

    def set_enabled(self, enabled):
        self.widget.setEnabled(enabled)
