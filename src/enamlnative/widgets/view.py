"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Int, Dict, Float, Bool, Tuple, Unicode, Event, observe, set_default
)

from enaml.core.declarative import d_

from enaml.widgets.widget import Widget, ProxyWidget


class ProxyView(ProxyWidget):
    """ The abstract definition of a proxy relative layout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: View)

    def set_alpha(self, alpha):
        raise NotImplementedError
    
    def set_clickable(self, clickable):
        raise NotImplementedError

    def set_background_color(self, color):
        raise NotImplementedError

    def set_layout_width(self, width):
        raise NotImplementedError

    def set_layout_height(self, height):
        raise NotImplementedError

    def set_layout_direction(self, direction):
        raise NotImplementedError

    def set_padding(self, padding):
        raise NotImplementedError

    def set_margins(self, margins):
        raise NotImplementedError

    def set_alpha(self, alpha):
        raise NotImplementedError

    def set_top(self, top):
        raise NotImplementedError

    def set_left(self, left):
        raise NotImplementedError

    def set_right(self, right):
        raise NotImplementedError

    def set_bottom(self, bottom):
        raise NotImplementedError

    def set_rotation(self,rotation):
        raise NotImplementedError

    def set_rotation_x(self, rotation):
        raise NotImplementedError

    def set_rotation_y(self, rotation):
        raise NotImplementedError

    def set_scale_x(self, scale):
        raise NotImplementedError

    def set_scale_y(self, scale):
        raise NotImplementedError

    def set_translation_x(self, translation):
        raise NotImplementedError

    def set_translation_y(self, translation):
        raise NotImplementedError

    def set_translation_z(self, translation):
        raise NotImplementedError

    def set_x(self, x):
        raise NotImplementedError

    def set_y(self, y):
        raise NotImplementedError

    def set_z(self, z):
        raise NotImplementedError

    def set_width(self, width):
        raise NotImplementedError

    def set_height(self, height):
        raise NotImplementedError

    def set_layout(self, layout):
        raise NotImplementedError


class View(Widget):
    """ View is a view group that displays
        child views in relative positions.

    """
    #: Describes how the child views are positioned.
    #: Defaults to Gravity.START | Gravity.TOP.

    alpha = d_(Float(1.0,strict=False))

    background_color = d_(Unicode())

    #
    # camera_distance = d_(Float())

    clickable = d_(Bool())
    
    #: Called when view is clicked
    clicked = d_(Event(), writable=False)

    # clip_bounds = d_(Tuple(int, default=(0, 0, 0, 0)))
    #
    # clip_to_outline = d_(Bool())

    content_description = d_(Unicode())

    # content_clickable = d_(Bool())
    #
    # drawing_cache_background_color = d_(Int())
    #
    # drawing_cache_enabled = d_(Bool())
    #
    # drawing_cache_quality = d_(Bool())
    #
    # duplicate_parent_state_enabled = d_(Bool())
    #
    # elevation = d_(Float())
    #
    # fading_edge_length = d_(Int())
    #
    # filter_touches_when_obscured = d_(Bool())
    #
    # fits_system_windows = d_(Bool())

    focusable = d_(Bool())

    # focusable_in_touch_mode = d_(Bool())
    #
    # hovered = d_(Bool())
    #
    # important_for_accessibility = d_(Int())

    keeps_screen_on = d_(Bool())

    #: Observe key events
    key_events = d_(Bool())

    #: Called when a key event occurs
    key_event = d_(Event(dict), writable=False)

    label_for = d_(Int())

    #layout_direction = d_(Enum('ltr', 'rtl', 'inherit', 'locale'))

    long_clickable = d_(Bool())

    nested_scrolling_enabled = d_(Bool())

    over_scroll_mode = d_(Int())


    #padding_relative = d_(Tuple(int))

    # pivot_x = d_(Float())
    #
    # pivot_y = d_(Float())

    pressed = d_(Bool())


    # rotation = d_(Float())
    #
    # rotation_x = d_(Float())
    #
    # rotation_y = d_(Float())
    #
    # save_enabled = d_(Bool())
    #
    # save_from_parent_enabled = d_(Bool())
    #
    # scale_x = d_(Float())
    #
    # scale_y = d_(Float())
    #
    # scroll_bar_default_delay_before_fade = d_(Int())
    #
    # scroll_bar_fade_duration = d_(Int())
    #
    # scroll_bar_size = d_(Int())
    #
    # scroll_bar_style = d_(Int())
    #
    # scroll_container = d_(Bool())
    #
    # scroll_indicators = d_(Tuple(int))
    #
    # scroll_x = d_(Int())
    #
    # scroll_y = d_(Int())
    #
    # scrollbar_fading_enabled = d_(Int())

    selected = d_(Bool())

    # sound_effects_enabled = d_(Bool())
    #
    # system_ui_visibility = d_(Int())

    text_alignment = d_(Int())

    text_direction = d_(Int())

    #: Observe touch events
    touch_events = d_(Bool())

    #: Called when a touch event occurs
    touch_event = d_(Event(dict), writable=False)

    # transition_name = d_(Unicode())
    #
    # translation_x = d_(Float())
    #
    # translation_y = d_(Float())
    #
    # translation_z = d_(Float())
    #
    # vertical_fading_edge_enabled = d_(Bool())
    #
    # vertical_scroll_bar_enabled = d_(Bool())
    #
    # vertical_scroll_bar_position = d_(Int())
    #
    # will_not_cache_drawing = d_(Bool())
    #
    # will_not_draw = d_(Bool())

    # Enum('', 'fill_parent', 'match_parent', 'wrap_content'))
    layout_width = d_(Unicode()).tag(ios=False)

    # Enum('', 'fill_parent', 'match_parent', 'wrap_content'))
    layout_height = d_(Unicode()).tag(ios=False)

    #: Left, top, right, bottom
    margins = d_(Tuple(int))

    #: Left, top, right, bottom
    padding = d_(Tuple(int))

    left = d_(Int())

    top = d_(Int())

    right = d_(Int())

    bottom = d_(Int())

    #
    x = d_(Float())

    y = d_(Float())

    z = d_(Float())
    #
    #: Width of frame
    #: on android use layout_width instead
    width = d_(Float()).tag(android=False)

    #: Height of frame
    #: on android use layout_width instead
    height = d_(Float()).tag(android=False)
    #
    #: Holder for flexbox layout parameters
    layout = d_(Dict())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe(
        'alpha',
        'background_color',
        'bottom',
        'camera_distance',
        'clip_bounds',
        'clip_to_outline',
        'content_description',
        'content_clickable',
        'drawing_cache_background_color',
        'drawing_cache_enabled',
        'drawing_cache_quality',
        'duplicate_parent_state_enabled',
        'elevation',
        'fading_edge_length',
        'filter_touches_when_obscured',
        'fits_system_windows',
        'focusable',
        'focusable_in_touch_mode',
        'hovered',
        'important_for_accessibility',
        'keeps_screen_on',
        'label_for',
        'layout_width',
        'layout_height',
        'layout_direction',
        'left',
        'long_clickable',
        'nested_scrolling_enabled',
        'margins',
        'over_scroll_mode',
        'padding',
        'padding_relative',
        'pivot_x',
        'pivot_y',
        'pressed',
        'right',
        'rotation',
        'rotation_x',
        'rotation_y',
        'save_enabled',
        'save_from_parent_enabled',
        'scale_x',
        'scale_y',
        'scroll_bar_default_delay_before_fade',
        'scroll_bar_fade_duration',
        'scroll_bar_size',
        'scroll_bar_style',
        'scroll_container',
        'scroll_indicators',
        'scroll_x',
        'scroll_y',
        'scrollbar_fading_enabled',
        'selected',
        'sound_effects_enabled',
        'system_ui_visibility',
        'text_alignment',
        'text_direction',
        'top',
        'transition_name',
        'translation_x',
        'translation_y',
        'translation_z',
        'vertical_fading_edge_enabled',
        'vertical_scroll_bar_enabled',
        'vertical_scroll_bar_position',
        'will_not_cache_drawing',
        'will_not_draw',
        'x',
        'y',
        'z',
        'width',
        'height',
        'layout',

    )
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(View, self)._update_proxy(change)
