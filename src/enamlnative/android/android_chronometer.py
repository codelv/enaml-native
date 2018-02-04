"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.chronometer import ProxyChronometer

from .android_text_view import AndroidTextView, TextView
from .bridge import JavaCallback, JavaMethod
from datetime import datetime, timedelta


UTC_START = datetime(1970, 1, 1)


class Chronometer(TextView):
    __nativeclass__ = set_default('android.widget.Chronometer')

    setBase = JavaMethod('long')
    setCountDown = JavaMethod('boolean')
    setFormat = JavaMethod('java.lang.String')
    setOnChronometerTickListener = JavaMethod(
        'android.widget.Chronometer$OnChronometerTickListener')
    onChronometerTick = JavaCallback('android.widget.Chronometer')
    start = JavaMethod()
    stop = JavaMethod()


class AndroidChronometer(AndroidTextView, ProxyChronometer):
    """ An Android implementation of an Enaml ProxyChronometer.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Chronometer)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = Chronometer(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidChronometer, self).init_widget()
        w = self.widget
        w.setOnChronometerTickListener(w.getId())
        w.onChronometerTick.connect(self.on_chronometer_tick)

    # -------------------------------------------------------------------------
    # OnChronometerTickListener API
    # -------------------------------------------------------------------------
    def on_chronometer_tick(self, view):
        d = self.declaration
        d.ticks += 1

    # -------------------------------------------------------------------------
    # ProxyChronometer API
    # -------------------------------------------------------------------------
    def set_base(self, base, shift=0):
        #: TODO: This is wrong becuase it uses system uptime
        #: instead of the actual time
        s = long((base - UTC_START).total_seconds())-shift
        self.widget.setBase(s)

    def set_format(self, format):
        self.widget.setFormat(format)

    def set_mode(self, mode):
        pass

    def set_direction(self, direction):
        self.widget.setCountDown(direction == 'down')

    def set_running(self, running):
        if running:
            d = self.declaration
            if d.mode == 'reset':
                d.ticks = 0
                #self.set_base(datetime.now())
            elif d.mode == 'resume':
                # Shift the date by now - ticks
                #self.set_base(datetime.now(), shift=d.ticks*1000)
                pass
            self.widget.start()
        else:
            self.widget.stop()
