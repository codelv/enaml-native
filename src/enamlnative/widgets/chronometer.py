"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from datetime import datetime
from atom.api import Bool, Enum, ForwardTyped, Int, Str, Typed, observe
from enaml.core.declarative import d_
from .text_view import ProxyTextView, TextView


class ProxyChronometer(ProxyTextView):
    """The abstract definition of a proxy Chronometer object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Chronometer)

    def set_base(self, base):
        raise NotImplementedError

    def set_format(self, format):
        raise NotImplementedError

    def set_direction(self, direction):
        raise NotImplementedError

    def set_running(self, running):
        raise NotImplementedError

    def set_mode(self, mode):
        raise NotImplementedError


class Chronometer(TextView):
    """A simple control for displaying read-only text."""

    #: Set the time that the count-up timer is in reference to.
    base = d_(Typed(datetime, factory=datetime.now))

    #: Tick counter
    ticks = d_(Int(), writable=False)

    #: Sets the format string used for display.
    format = d_(Str())

    #: Counting direction
    direction = d_(Enum("up", "down"))

    #: Defines the behavior when restarting
    #: If mode is resume it will continue otherwise
    #: it will reset the count.
    mode = d_(Enum("resume", "reset", "manual"))

    #: Start / stop the counter
    running = d_(Bool())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyChronometer)

    @observe("base", "direction", "format", "running", "mode")
    def _update_proxy(self, change):

        super()._update_proxy(change)
