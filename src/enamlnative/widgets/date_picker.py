#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Typed, ForwardTyped, Int, Long, Range, Bool, observe
)

from enaml.core.declarative import d_

from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyDatePicker(ProxyFrameLayout):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: DatePicker)

    def set_enabled(self, enabled):
        raise NotImplementedError

    def set_first_day_of_week(self, day):
        raise NotImplementedError

    def set_year(self, year):
        raise NotImplementedError

    def set_month(self, month):
        raise NotImplementedError

    def set_day(self, day):
        raise NotImplementedError

    def set_min_date(self, date):
        raise NotImplementedError

    def set_max_date(self, date):
        raise NotImplementedError


class DatePicker(FrameLayout):
    """ A simple control for displaying read-only text.

    """
    #: Set the enabled state of this view.
    enabled = d_(Bool(True))

    #: Update the current year.
    year = d_(Int(0))

    #: Update the current month.
    month = d_(Int(0))

    #: Update the current day.
    day = d_(Int(0))

    #: Sets the minimal date supported by this DatePicker
    #: in milliseconds since January 1, 1970 00:00:00 in getDefault() time zone.
    min_date = d_(Long(0))

    #: Sets the maximal date supported by this DatePicker
    #: in milliseconds since January 1, 1970 00:00:00 in getDefault() time zone.
    max_date = d_(Long(0))

    #: Sets the first day of week.
    first_day_of_week = d_(Range(1,7))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyDatePicker)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('enabled','year','month','day','min_date','max_date','first_day_of_week')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(DatePicker, self)._update_proxy(change)
