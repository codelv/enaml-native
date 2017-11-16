"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Int, Instance, Range, Bool, observe
)

from datetime import datetime
from enaml.core.declarative import d_

from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyDatePicker(ProxyFrameLayout):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: DatePicker)

    def set_first_day_of_week(self, day):
        raise NotImplementedError

    def set_date(self, date):
        raise NotImplementedError

    def set_min_date(self, date):
        raise NotImplementedError

    def set_max_date(self, date):
        raise NotImplementedError


class DatePicker(FrameLayout):
    """ A simple control for displaying read-only text.

    """
    #: Update the current year.
    date = d_(Instance(datetime, factory=datetime.now))

    #: Sets the minimal date supported by this DatePicker in milliseconds
    #: since January 1, 1970 00:00:00 in getDefault() time zone.
    min_date = d_(Instance(datetime))

    #: Sets the maximal date supported by this DatePicker in milliseconds
    #: since January 1, 1970 00:00:00 in getDefault() time zone.
    max_date = d_(Instance(datetime))

    #: Sets the first day of week.
    first_day_of_week = d_(Range(1, 7))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyDatePicker)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('date', 'min_date', 'max_date', 'first_day_of_week')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(DatePicker, self)._update_proxy(change)
