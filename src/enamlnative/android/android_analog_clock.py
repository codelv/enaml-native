"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 7, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.analog_clock import ProxyAnalogClock

from .android_view import AndroidView, View


class AnalogClock(View):
    __nativeclass__ = set_default('android.widget.AnalogClock')


class AndroidAnalogClock(AndroidView, ProxyAnalogClock):
    """ An Android implementation of an Enaml ProxyAnalogClock.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(AnalogClock)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = AnalogClock(self.get_context())



