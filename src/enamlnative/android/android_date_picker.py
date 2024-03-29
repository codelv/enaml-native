"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from datetime import datetime
from atom.api import Typed
from enamlnative.widgets.date_picker import ProxyDatePicker
from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaCallback, JavaMethod

UTC_START = datetime(1970, 1, 1)


class DatePicker(FrameLayout):
    __nativeclass__ = "android.widget.DatePicker"
    init = JavaMethod(int, int, int, "android.widget.DatePicker$OnDateChangedListener")
    onDateChanged = JavaCallback("android.widget.DatePicker", int, int, int)
    updateDate = JavaMethod(int, int, int)
    setFirstDayOfWeek = JavaMethod(int)
    setEnabled = JavaMethod(bool)
    setMaxDate = JavaMethod("long")
    setMinDate = JavaMethod("long")


class AndroidDatePicker(AndroidFrameLayout, ProxyDatePicker):
    """An Android implementation of an Enaml ProxyDatePicker."""

    #: A reference to the widget created by the proxy.
    widget = Typed(DatePicker)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = DatePicker(
            self.get_context(), None, d.style or "@attr/datePickerStyle"
        )

    def init_widget(self):
        """Initialize the underlying widget."""
        d = self.declaration
        w = self.widget
        date = d.date
        w.init(date.year, date.month - 1, date.day, w.getId())
        super().init_widget()
        w.onDateChanged.connect(self.on_date_changed)

    # -------------------------------------------------------------------------
    # OnDateChangedListener API
    # -------------------------------------------------------------------------
    def on_date_changed(self, view, year, month, day):
        d = self.declaration
        with self.widget.updateDate.suppressed():
            d.date = datetime(year, month + 1, day)

    # -------------------------------------------------------------------------
    # ProxyDatePicker API
    # -------------------------------------------------------------------------
    def set_date(self, date):
        self.widget.updateDate(date.year, date.month - 1, date.day)

    def set_min_date(self, date):
        #: Convert to long
        s = int((date - UTC_START).total_seconds() * 1000)
        self.widget.setMinDate(s)

    def set_max_date(self, date):
        #: Convert to long
        s = int((date - UTC_START).total_seconds() * 1000)
        self.widget.setMaxDate(s)

    def set_first_day_of_week(self, day):
        self.widget.setFirstDayOfWeek(day)
