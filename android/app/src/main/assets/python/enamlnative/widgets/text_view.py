'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Unicode, Enum, Float, Int, Bool, observe, set_default
)

from enaml.core.declarative import d_

from .view import View, ProxyView


class ProxyTextView(View):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: TextView)

    def set_all_caps(self, enabled):
        raise NotImplementedError

    def set_auto_link_mask(self, mask):
        raise NotImplementedError

    def set_font_family(self, family):
        raise NotImplementedError

    def set_font_style(self, style):
        raise NotImplementedError

    def set_text(self, text):
        raise NotImplementedError

    def set_text_color(self, color):
        raise NotImplementedError

    def set_highlight_color(self, color):
        raise NotImplementedError

    def set_link_color(self, color):
        raise NotImplementedError

    def set_text_size(self, size):
        raise NotImplementedError

    def set_lines(self, lines):
        raise NotImplementedError

    def set_max_lines(self, lines):
        raise NotImplementedError


class TextView(View):
    """ A simple control for displaying read-only text.

    """

    #: Sets the properties of this field to transform input to ALL CAPS display.
    all_caps = d_(Bool())

    #: Sets the autolink mask of the text.
    auto_link_mask = d_(Int(0))

    #: Font family
    font_family = d_(Unicode())

    #: Font style
    font_style = d_(Enum('normal','bold','italic','bold_italic'))

    #: Sets the color used to display the selection highlight.
    highlight_color = d_(Unicode())

    #: Sets the color of links in the text.
    link_color = d_(Unicode())

    #: The unicode text for the label.
    text = d_(Unicode())

    #: Sets the text color for all the states (normal, selected, focused) to be this color.
    text_color = d_(Unicode())

    #: Set the default text size to the given value, interpreted as "scaled pixel" units.
    text_size = d_(Float(strict=False))

    #: Sets the height of the TextView to be exactly lines tall.
    lines = d_(Int())

    #: Sets the height of the TextView to be at most maxLines tall.
    max_lines = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyTextView)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
    @observe('all_caps', 'auto_link_mask',
             'font_family', 'font_style',
             'text', 'text_color', 'text_size',
             'link_color', 'highlight_color',
             'lines', 'max_lines')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(TextView, self)._update_proxy(change)
