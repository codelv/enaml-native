"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, observe
)

from enaml.core.declarative import d_

from .text_view import TextView, ProxyTextView


class ProxyTextClock(ProxyTextView):
    """ The abstract definition of a proxy TextClock object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: TextClock)

    def set_format_12_hour(self, clock_format):
        raise NotImplementedError

    def set_format_24_hour(self, clock_format):
        raise NotImplementedError

    def set_time_zone(self, time_zone):
        raise NotImplementedError


class TextClock(TextView):
    """ A simple control for displaying read-only text.

    """

    #: Specifies the formatting pattern used to display the date and/or time
    #: in 12-hour mode.
    format_12_hour = d_(Unicode())

    #: Specifies the formatting pattern used to display the date and/or time
    #: in 24-hour mode.
    format_24_hour = d_(Unicode())

    #: Sets the specified time zone to use in this clock.
    time_zone = d_(Unicode())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyTextClock)

    @observe('format_12_hour', 'format_24_hour', 'time_zone')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(TextClock, self)._update_proxy(change)
