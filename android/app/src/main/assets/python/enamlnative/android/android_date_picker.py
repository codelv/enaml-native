'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed, set_default

from enamlnative.widgets.date_picker import ProxyDatePicker

from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaMethod, JavaCallback


class DatePicker(FrameLayout):
    __javaclass__ = set_default('android.widget.DatePicker')
    init = JavaMethod('int', 'int', 'int', 'android.widget.DatePicker$OnDateChangedListener')
    onDateChanged = JavaCallback('android.widget.DatePicker', 'int', 'int', 'int')
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

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = DatePicker(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidDatePicker, self).init_widget()
        d = self.declaration
        self.set_enabled(d.enabled)
        self.set_first_day_of_week(d.first_day_of_week)
        if d.min_date:
            self.set_min_date(d.min_date)
        if d.max_date:
            self.set_max_date(d.max_date)

        self.widget.init(d.year, d.month, d.day, id(self.widget))
        self.widget.onDateChanged.connect(self.on_date_changed)

    # --------------------------------------------------------------------------
    # OnDateChangedListener API
    # --------------------------------------------------------------------------
    def on_date_changed(self, view, year, month, day):
        d = self.declaration
        with self.widget.updateDate.suppressed():
            d.year = year
            d.month = month
            d.day = day

    # --------------------------------------------------------------------------
    # ProxyDatePicker API
    # --------------------------------------------------------------------------
    def set_year(self, year):
        self.update_date()

    def set_month(self, month):
        self.update_date()

    def set_day(self, day):
        self.update_date()

    def update_date(self):
        d = self.declaration
        self.widget.updateDate(d.year, d.month, d.day)

    def set_min_date(self, date):
        self.widget.setMinDate(date)

    def set_max_date(self, date):
        self.widget.setMaxDate(date)

    def set_first_day_of_week(self, day):
        self.widget.setFirstDayOfWeek(day)

    def set_enabled(self, enabled):
        self.widget.setEnabled(enabled)
