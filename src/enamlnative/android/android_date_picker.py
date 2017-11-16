"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from datetime import datetime
from enamlnative.widgets.date_picker import ProxyDatePicker

from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaMethod, JavaCallback

UTC_START = datetime(1970, 1, 1)


class DatePicker(FrameLayout):
    __nativeclass__ = set_default('android.widget.DatePicker')
    init = JavaMethod('int', 'int', 'int',
                      'android.widget.DatePicker$OnDateChangedListener')
    onDateChanged = JavaCallback('android.widget.DatePicker', 'int', 'int',
                                 'int')
    updateDate = JavaMethod('int', 'int', 'int')
    setFirstDayOfWeek = JavaMethod('int')
    setEnabled = JavaMethod('boolean')
    setMaxDate = JavaMethod('long')
    setMinDate = JavaMethod('long')


class AndroidDatePicker(AndroidFrameLayout, ProxyDatePicker):
    """ An Android implementation of an Enaml ProxyDatePicker.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(DatePicker)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = DatePicker(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidDatePicker, self).init_widget()
        d = self.declaration

        if d.min_date:
            self.set_min_date(d.min_date)
        if d.max_date:
            self.set_max_date(d.max_date)
        if d.first_day_of_week != 1:
            self.set_first_day_of_week(d.first_day_of_week)

        self.widget.init(d.date.year, d.date.month-1, d.date.day,
                         self.widget.getId())
        self.widget.onDateChanged.connect(self.on_date_changed)

    # -------------------------------------------------------------------------
    # OnDateChangedListener API
    # -------------------------------------------------------------------------
    def on_date_changed(self, view, year, month, day):
        d = self.declaration
        with self.widget.updateDate.suppressed():
            d.date = datetime(year, month+1, day)

    # -------------------------------------------------------------------------
    # ProxyDatePicker API
    # -------------------------------------------------------------------------
    def set_date(self, date):
        self.widget.updateDate(date.year, date.month-1, date.day)

    def set_min_date(self, date):
        #: Convert to long
        s = long((date - UTC_START).total_seconds()*1000)
        self.widget.setMinDate(s)

    def set_max_date(self, date):
        #: Convert to long
        s = long((date - UTC_START).total_seconds()*1000)
        self.widget.setMaxDate(s)

    def set_first_day_of_week(self, day):
        self.widget.setFirstDayOfWeek(day)

