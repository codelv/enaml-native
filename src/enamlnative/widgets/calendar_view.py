"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Range, Instance, observe, set_default
)
from datetime import datetime
from enaml.core.declarative import d_

from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyCalendarView(ProxyFrameLayout):
    """ The abstract definition of a proxy relative layout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: CalendarView)

    def set_date(self, date):
        raise NotImplementedError

    def set_first_day_of_week(self, day):
        raise NotImplementedError

    def set_max_date(self, date):
        raise NotImplementedError

    def set_min_date(self, date):
        raise NotImplementedError


class CalendarView(FrameLayout):
    """ CalendarView is a view group that displays
    child views in relative positions.

    """
    #: Selected date
    date = d_(Instance(datetime))

    #: Max date
    max_date = d_(Instance(datetime))

    #: Min date
    min_date = d_(Instance(datetime))

    #: First day of week
    first_day_of_week = d_(Range(1, 7))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyCalendarView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('date', 'max_date', 'min_date', 'first_day_of_week')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(CalendarView, self)._update_proxy(change)
