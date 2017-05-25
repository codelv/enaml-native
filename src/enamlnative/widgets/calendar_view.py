#------------------------------------------------------------------------------
# Copyright (c) 2017, Jairus Martin.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Typed, ForwardTyped, Int, Long, Enum, Event, observe, set_default
)

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
    #: Describes how the child views are positioned.
    #: Defaults to Gravity.START | Gravity.TOP.
    date = d_(Long())

    max_date = d_(Long())

    min_date = d_(Long())

    #:
    first_day_of_week = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyCalendarView)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('date','max_date','min_date','first_day_of_week')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(CalendarView, self)._update_proxy(change)
