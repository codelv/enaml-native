"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from datetime import datetime
from atom.api import ForwardTyped, Instance, Range, Typed, observe
from enaml.core.declarative import d_
from .frame_layout import FrameLayout, ProxyFrameLayout


class ProxyCalendarView(ProxyFrameLayout):
    """The abstract definition of a proxy relative layout object."""

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
    """CalendarView is a view group that displays
    child views in relative positions.

    """

    #: Selected date
    date = d_(Instance(datetime, factory=datetime.now))

    #: Max date
    max_date = d_(Instance(datetime, factory=datetime.now))

    #: Min date
    min_date = d_(Instance(datetime, factory=datetime.now))

    #: First day of week
    first_day_of_week = d_(Range(1, 7))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyCalendarView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("date", "max_date", "min_date", "first_day_of_week")
    def _update_proxy(self, change):

        super()._update_proxy(change)
