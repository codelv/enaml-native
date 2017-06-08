'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.chronometer import ProxyChronometer

from .android_text_view import AndroidTextView

SystemClock = jnius.autoclass('android.os.SystemClock')
Chronometer = jnius.autoclass('android.widget.Chronometer')


class OnChronometerTickListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/widget/Chronometer$OnChronometerTickListener']

    def __init__(self, handler):
        self.__handler__ = handler
        super(OnChronometerTickListener, self).__init__()

    @jnius.java_method('(Landroid/widget/Chronometer;)V')
    def onChronometerTick(self, view):
        self.__handler__.on_chronometer_tick(view)


class AndroidChronometer(AndroidTextView, ProxyChronometer):
    """ An Android implementation of an Enaml ProxyChronometer.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Chronometer)

    #: Save a reference to the tick listener
    tick_listener = Typed(OnChronometerTickListener)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = Chronometer(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidChronometer, self).init_widget()
        d = self.declaration
        self.set_base(d.base)
        if d.format:
            self.set_format(d.format)
        if d.direction == 'down':
            self.set_direction(d.direction)

        self.tick_listener = OnChronometerTickListener(self)
        self.widget.setOnChronometerTickListener(self.tick_listener)

        if d.running:
            self.set_running(d.running)

    # --------------------------------------------------------------------------
    # OnChronometerTickListener API
    # --------------------------------------------------------------------------
    def on_chronometer_tick(self, view):
        d = self.declaration
        with self.suppress_notifications():
            d.text = self.widget.getText()
            d.ticks += 1

    # --------------------------------------------------------------------------
    # ProxyChronometer API
    # --------------------------------------------------------------------------
    def set_base(self, base):
        self.widget.setBase(base or SystemClock.elapsedRealtime())

    def set_format(self, format):
        self.widget.setFormat(format)

    def set_direction(self, direction):
        self.widget.setCountDown(direction=='down')

    def set_running(self, running):
        if running:
            d = self.declaration
            d.ticks = 0
            self.widget.start()
        else:
            self.widget.stop()
