#------------------------------------------------------------------------------
# Copyright (c) 2017, Jairus Martin.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.chronometer import ProxyChronometer

from .android_text_view import AndroidTextView

SystemClock = jnius.autoclass('android.os.SystemClock')
_Chronometer = jnius.autoclass('android.widget.Chronometer')


class AndroidChronometer(AndroidTextView, ProxyChronometer):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_Chronometer)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _Chronometer(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidChronometer, self).init_widget()
        d = self.declaration
        self.set_base(d.base)
        if d.format:
            self.set_format(d.format)
        if d.direction=='down':
            self.set_direction(d.direction)

    #--------------------------------------------------------------------------
    # ProxyLabel API
    #--------------------------------------------------------------------------
    def set_base(self, base):
        self.widget.setBase(base or SystemClock.elapsedRealtime())

    def set_format(self, format):
        self.widget.setFormat(format)

    def set_direction(self, direction):
        self.widget.setCountDown(direction=='down')
