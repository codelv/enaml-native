'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Int, Enum, Float, Bool, Tuple, Unicode, Event, observe, set_default
)

from enaml.core.declarative import d_

from enaml.widgets.widget import Widget, ProxyWidget

class ProxyView(ProxyWidget):
    """ The abstract definition of a proxy relative layout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: View)

    def set_layout_direction(self, direction):
        raise NotImplementedError

    def set_alpha(self, alpha):
        raise NotImplementedError

    def set_top(top):
        raise NotImplementedError

    def set_left(left):
        raise NotImplementedError

    def set_right(right):
        raise NotImplementedError

    def set_bottom(bottom):
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

class View(Widget):
    """ View is a view group that displays
        child views in relative positions.

    """
    #: Describes how the child views are positioned.
    #: Defaults to Gravity.START | Gravity.TOP.

    alpha = d_(Int())

    background_color = d_(Int())

    bottom = d_(Int())

    camera_distance = d_(Float())

    clickable = d_(Bool())

    clip_bounds = d_(Tuple(int, default=(0, 0, 0, 0)))

    clip_to_outline = d_(Bool())

    content_description = d_(Unicode())

    content_clickable = d_(Bool())

    drawing_cache_background_color = d_(Int())

    drawing_cache_enabled = d_(Bool())

    drawing_cache_quality = d_(Bool())

    duplicate_parent_state_enabled = d_(Bool())

    elevation = d_(Float())

    fading_edge_length = d_(Int())

    filter_touches_when_obscured = d_(Bool())

    fits_system_windows = d_(Bool())

    focusable = d_(Bool())

    focusable_in_touch_mode = d_(Bool())

    hovered = d_(Bool())

    important_for_accessibility = d_(Int())

    keeps_screen_on = d_(Bool())

    label_for = d_(Int())

    layout_direction = d_(Enum('none','inherit','locale','ltr','rtl'))

    left = d_(Int())

    long_clickable = d_(Bool())

    nested_scrolling_enabled = d_(Bool())

    over_scroll_mode = d_(Int())

    padding = d_(Tuple(int,default=(0,0,0,0)))

    padding_relative = d_(Tuple(int,default=(0,0,0,0)))

    pivot_x = d_(Float())

    pivot_y = d_(Float())

    pressed = d_(Bool())

    right = d_(Int())

    rotation = d_(Float())

    rotation_x = d_(Float())

    rotation_y = d_(Float())

    save_enabled = d_(Bool())

    save_from_parent_enabled = d_(Bool())

    scale_x = d_(Float())

    scale_y = d_(Float())

    scroll_bar_default_delay_before_fade = d_(Int())

    scroll_bar_fade_duration = d_(Int())

    scroll_bar_size = d_(Int())

    scroll_bar_style = d_(Int())

    scroll_container = d_(Bool())

    scroll_indicators = d_(Tuple(int))

    scroll_x = d_(Int())

    scroll_y = d_(Int())

    scrollbar_fading_enabled = d_(Int())

    selected = d_(Bool())

    sound_effects_enabled = d_(Bool())

    system_ui_visibility = d_(Int())

    text_alignment = d_(Int())

    text_direction = d_(Int())

    top = d_(Int())

    transition_name = d_(Unicode())

    translation_x = d_(Float())

    translation_y = d_(Float())

    translation_z = d_(Float())

    vertical_fading_edge_enabled = d_(Bool())

    vertical_scroll_bar_enabled = d_(Bool())

    vertical_scroll_bar_position = d_(Int())

    will_not_cache_drawing = d_(Bool())

    will_not_draw = d_(Bool())

    x = d_(Float())

    y = d_(Float())

    z = d_(Float())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyView)

    #--------------------------------------------------------------------------
    # Observers
    #--------------------------------------------------------------------------
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
        'layout_direction',
        'left',
        'long_clickable',
        'nested_scrolling_enabled',
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
    )
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(View, self)._update_proxy(change)
