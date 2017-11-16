"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.chronometer import ProxyChronometer

from .android_text_view import AndroidTextView, TextView
from .bridge import JavaCallback, JavaMethod


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
        d = self.declaration
        if d.base:
            self.set_base(d.base)
        if d.format:
            self.set_format(d.format)
        if d.direction == 'down':
            self.set_direction(d.direction)

        self.widget.setOnChronometerTickListener(self.widget.getId())
        self.widget.onChronometerTick.connect(self.on_chronometer_tick)

        if d.running:
            self.set_running(d.running)

    # -------------------------------------------------------------------------
    # OnChronometerTickListener API
    # -------------------------------------------------------------------------
    def on_chronometer_tick(self, view):
        d = self.declaration
        #d.text = self.widget.getText()
        d.ticks += 1

    # -------------------------------------------------------------------------
    # ProxyChronometer API
    # -------------------------------------------------------------------------
    def set_base(self, base):
        self.widget.setBase(base)  # or SystemClock.elapsedRealtime())

    def set_format(self, format):
        self.widget.setFormat(format)

    def set_direction(self, direction):
        self.widget.setCountDown(direction == 'down')

    def set_running(self, running):
        if running:
            d = self.declaration
            d.ticks = 0
            self.widget.start()
        else:
            self.widget.stop()
