'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.date_picker import ProxyDatePicker

from .android_frame_layout import AndroidFrameLayout

DatePicker = jnius.autoclass('android.widget.DatePicker')


class OnDateChangedListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/widget/DatePicker$OnDateChangedListener']

    def __init__(self, handler):
        self.__handler__ = handler
        super(OnDateChangedListener, self).__init__()

    @jnius.java_method('(Landroid/widget/DatePicker;III)V')
    def onDateChanged(self, view, year, month, day):
        self.__handler__.on_date_changed(view, year, month, day)


class AndroidDatePicker(AndroidFrameLayout, ProxyDatePicker):
    """ An Android implementation of an Enaml ProxyDatePicker.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(DatePicker)

    #: Save a reference to the date changed listener
    date_listener = Typed(OnDateChangedListener)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying Android widget.

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

        self.date_listener = OnDateChangedListener(self)
        self.widget.init(d.year, d.month, d.day, self.date_listener)

    # --------------------------------------------------------------------------
    # OnDateChangedListener API
    # --------------------------------------------------------------------------
    def on_date_changed(self, view, year, month, day):
        d = self.declaration
        with self.suppress_notifications():
            d.year = year
            d.month = month
            d.day = day


    # --------------------------------------------------------------------------
    # ProxyFrameLayout API
    # --------------------------------------------------------------------------
    def set_year(self, year):
        self.update_date()

    def set_month(self, month):
        self.update_date()

    def set_day(self, day):
        self.update_date()

    def update_date(self):
        d = self.declaration
        self.widget.updateDate(d.year,d.month,d.day)

    def set_first_day_of_week(self, day):
        self.widget.setFirstDayOfWeek(day)

    def set_enabled(self, enabled):
        self.widget.setEnabled(enabled)
