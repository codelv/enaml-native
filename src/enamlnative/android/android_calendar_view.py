'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.calendar_view import ProxyCalendarView

from .android_frame_layout import AndroidFrameLayout

_CalendarView = jnius.autoclass('android.widget.CalendarView')

class AndroidCalendarView(AndroidFrameLayout, ProxyCalendarView):
    """ An Android implementation of an Enaml ProxyFrameLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_CalendarView)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _CalendarView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidCalendarView, self).init_widget()
        d = self.declaration
        self.set_date(d.date)
        if d.min_date:
            self.set_min_date(d.min_date)
        if d.max_date:
            self.set_max_date(d.max_date)
        self.set_first_day_of_week(d.first_day_of_week)

    #--------------------------------------------------------------------------
    # ProxyFrameLayout API
    #--------------------------------------------------------------------------
    def set_date(self, date):
        self.widget.setDate(date)

    def set_min_date(self, date):
        self.widget.setMinDate(date)

    def set_max_date(self, date):
        self.widget.setMaxDate(date)

    def set_first_day_of_week(self, day):
        self.widget.setFirstDayOfWeek(day)
