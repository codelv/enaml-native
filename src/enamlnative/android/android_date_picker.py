#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.date_picker import ProxyDatePicker

from .android_frame_layout import AndroidFrameLayout

_DatePicker = jnius.autoclass('android.widget.DatePicker')

class AndroidDatePicker(AndroidFrameLayout, ProxyDatePicker):
    """ An Android implementation of an Enaml ProxyFrameLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_DatePicker)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _DatePicker(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidDatePicker, self).init_widget()
        d = self.declaration
        self.update_date()
        self.set_enabled(d.enabled)
        self.set_first_day_of_week(d.first_day_of_week)
        if d.min_date:
            self.set_min_date(d.min_date)
        if d.max_date:
            self.set_max_date(d.max_date)

    #--------------------------------------------------------------------------
    # ProxyFrameLayout API
    #--------------------------------------------------------------------------
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
