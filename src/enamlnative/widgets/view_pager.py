"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

 
"""
from atom.api import (
    Bool,
    Enum,
    Float,
    ForwardTyped,
    Int,
    Str,
    Typed,
    Property,
    set_default,
)
from enaml.core.declarative import d_, observe
from .fragment import Fragment, ProxyFragment
from .view_group import ProxyViewGroup, ViewGroup


class ProxyViewPager(ProxyViewGroup):
    """The abstract definition of a proxy ViewPager object."""

    #: A reference to the ViewPager declaration.
    declaration = ForwardTyped(lambda: ViewPager)

    def set_current_index(self, index: int):
        raise NotImplementedError

    def set_offscreen_page_limit(self, limit: int):
        raise NotImplementedError

    def set_page_margin(self, margin: int):
        raise NotImplementedError

    def set_paging_enabled(self, enabled: bool):
        raise NotImplementedError

    def set_transition(self, transition: str):
        raise NotImplementedError


class ProxyPagerTitleStrip(ProxyViewGroup):
    """The abstract definition of a proxy PagerTitleStrip object."""

    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: PagerTitleStrip)

    def set_titles(self, titles: list[str]):
        raise NotImplementedError

    def set_inactive_alpha(self, alpha: float):
        raise NotImplementedError

    def set_text_color(self, color: str):
        raise NotImplementedError

    def set_text_size(self, size: int):
        raise NotImplementedError

    def set_text_spacing(self, spacing: int):
        raise NotImplementedError


class ProxyPagerTabStrip(ProxyPagerTitleStrip):
    """The abstract definition of a proxy PagerTabStrip object."""

    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: PagerTabStrip)

    def set_tab_indicator_color(self, color: str):
        raise NotImplementedError

    def set_tab_full_underline(self, enabled: bool):
        raise NotImplementedError


class ProxyPagerFragment(ProxyFragment):
    """The abstract definition of a proxy ProxyPagerFragment object."""

    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: PagerFragment)

    def set_title(self, title: str):
        raise NotImplementedError

    def set_icon(self, icon: str):
        raise NotImplementedError


class ViewPager(ViewGroup):
    """Layout manager that allows the user to flip left and right through
    pages of data.

    """

    #: Set the currently selected page.
    current_index = d_(Int())

    #: Set the number of pages that should be retained to either side
    #: of the current page in the view hierarchy in an idle state.
    offscreen_page_limit = d_(Int())

    #: Enable or disable paging by swiping
    paging_enabled = d_(Bool(True))

    #: Set the margin between pages.
    page_margin = d_(Int(-1))

    #: Read only list of pages
    pages = Property()

    def _get_pages(self):
        return [c for c in self._children if isinstance(c, Fragment)]

    #: Transition
    transition = d_(
        Enum(
            "default",
            "accordion",
            "bg_to_fg",
            "fg_to_bg",
            "cube_in",
            "cube_out",
            "draw_from_back",
            "flip_horizontal",
            "flip_vertical",
            "depth_page",
            "parallax_page",
            "rotate_down",
            "rotate_up",
            "stack",
            "tablet",
            "zoom_in",
            "zoom_out",
            "zoom_out_slide",
        )
    )

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyViewPager)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe(
        "current_index",
        "offscreen_page_limit",
        "page_margin",
        "paging_enabled",
        "transition",
    )
    def _update_proxy(self, change):

        super()._update_proxy(change)


class PagerTitleStrip(ViewGroup):
    #: Top by default
    gravity = set_default("top")

    #: Set the alpha value used for non-primary page titles.
    inactive_alpha = d_(Float())

    # Set the color value used as the base color for all displayed page titles.
    text_color = d_(Str())

    #: Set the default text size to a given unit and value. Forced to DP
    text_size = d_(Int())

    #: Spacing pixels
    text_spacing = d_(Int())

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("text_color", "text_size", "text_spacing")
    def _update_proxy(self, change):

        super()._update_proxy(change)


class PagerTabStrip(PagerTitleStrip):

    #: Set the color of the tab indicator bar.
    tab_indicator_color = d_(Str())

    #: Set whether this tab strip should draw a full-width underline
    #: in the current tab indicator color.
    tab_full_underline = d_(Bool())

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("tab_indicator_color", "tab_full_underline")
    def _update_proxy(self, change):

        super()._update_proxy(change)


class PagerFragment(Fragment):
    """A Fragment that sets page content and provides a title for tabs
    and title sliders.

    """

    #: Set the title for the title or tab pager
    title = d_(Str())

    #: Set the icon or drawable resource for the title or tab pager
    icon = d_(Str())

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("title", "icon")
    def _update_proxy(self, change):

        super()._update_proxy(change)
