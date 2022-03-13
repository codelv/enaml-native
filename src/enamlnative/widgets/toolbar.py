"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import ForwardTyped, Str, Tuple, Typed
from enaml.core.declarative import d_, observe
from .view_group import ProxyViewGroup, ViewGroup


class ProxyToolbar(ProxyViewGroup):
    """The abstract definition of a proxy Toolbar object."""

    #: A reference to the widget declaration.
    declaration = ForwardTyped(lambda: Toolbar)

    def set_content_padding(self, padding: tuple[int, ...]):
        raise NotImplementedError

    def set_title(self, text: str):
        raise NotImplementedError

    def set_subtitle(self, text: str):
        raise NotImplementedError

    def set_title_margins(self, margins: tuple[int, ...]):
        raise NotImplementedError

    def set_title_color(self, color: str):
        raise NotImplementedError

    def set_subtitle_color(self, color: str):
        raise NotImplementedError


class Toolbar(ViewGroup):
    """A standard toolbar for use within application content."""

    #: Sets the content padding
    content_padding = d_(Tuple(int))

    #: Set the title of this toolbar.
    title = d_(Str())

    #: Set the subtitle of this toolbar
    subtitle = d_(Str())

    #: Sets the title margin.
    title_margins = d_(Tuple(int))

    #: Sets the text color of the title, if present.
    title_color = d_(Str())

    #: Sets the text color of the subtitle, if present.
    subtitle_color = d_(Str())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyToolbar)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe(
        "content_padding",
        "title",
        "title_color",
        "title_margins",
        "subtitle",
        "subtitle_color",
    )
    def _update_proxy(self, change):

        super()._update_proxy(change)
