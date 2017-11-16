"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Tuple, Int, Enum, Event, observe, set_default
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup


class ProxyToolbar(ProxyViewGroup):
    """ The abstract definition of a proxy Toolbar object.

    """
    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: Toolbar)

    def set_content_padding(self, padding):
        raise NotImplementedError

    def set_title(self, text):
        raise NotImplementedError

    def set_subtitle(self, text):
        raise NotImplementedError

    def set_title_margins(self, margins):
        raise NotImplementedError

    def set_title_color(self, color):
        raise NotImplementedError

    def set_subtitle_color(self, color):
        raise NotImplementedError


class Toolbar(ViewGroup):
    """ A standard toolbar for use within application content.

    """

    #: Sets the content padding
    content_padding = d_(Tuple(int))

    #: Set the title of this toolbar.
    title = d_(Unicode())

    #: Set the subtitle of this toolbar
    subtitle = d_(Unicode())

    #: Sets the title margin.
    title_margins = d_(Tuple(int))

    #: Sets the text color of the title, if present.
    title_color = d_(Unicode())

    #: Sets the text color of the subtitle, if present.
    subtitle_color = d_(Unicode())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyToolbar)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('content_padding','title', 'title_color', 'title_margins',
             'subtitle', 'subtitle_color')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(Toolbar, self)._update_proxy(change)
