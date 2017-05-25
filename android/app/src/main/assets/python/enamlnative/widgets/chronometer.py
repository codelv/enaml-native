'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Long, Unicode, Enum, Event, observe, set_default
)

from enaml.core.declarative import d_

from .text_view import TextView, ProxyTextView


class ProxyChronometer(ProxyTextView):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Chronometer)

    def set_base(self, base):
        raise NotImplementedError

    def set_format(self, format):
        raise NotImplementedError

    def set_direction(self, direction):
        raise NotImplementedError

    def on_start(self):
        pass

    def on_stop(self):
        pass

class Chronometer(TextView):
    """ A simple control for displaying read-only text.

    """

    #: Set the time that the count-up timer is in reference to.
    base = d_(Long())

    #: Sets the format string used for display.
    format = d_(Unicode())

    direction = d_(Enum('up','down'))

    #: Start counting up.
    start = d_(Event(), writable=False)

    #: Stop counting up.
    stop = d_(Event(), writable=False)

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyChronometer)

    @observe('base', 'direction', 'format')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(Chronometer, self)._update_proxy(change)
