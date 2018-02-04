"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Coerced, Bool, Int, Tuple, Event, Float, Unicode,
    Enum, observe
)

from enaml.core.declarative import d_
from enaml.widgets.toolkit_object import ToolkitObject, ProxyToolkitObject


LAYOUT_GRAVITIES = {
    'top', 'left', 'right',
    'bottom', 'center',
    'end', 'start', 'no_gravity',
    'fill_horizontal'
}

LAYOUT_GRAVITIES = {
    'no_gravity': 0,
    'center_horizontal': 1,
    'center_vertical': 16,
    'center': 11,
    'fill': 119,
    'fill_horizontal': 7,
    'fill_vertical': 112,
    'top': 48,
    'bottom': 80,
    'left': 3,
    'right': 5,
    'start': 8388611,
    'end': 8388613
}


def coerce_size(v):
    if v == 'match_parent':
        return -1
    elif v == 'wrap_content':
        return -2
    return int(v)


def coerce_gravity(v):
    if isinstance(v, int):
        return v
    g = 0
    for r in v.split("|"):
        g |= LAYOUT_GRAVITIES[r]
    return g


class ProxyView(ProxyToolkitObject):
    """ The abstract definition of a proxy relative layout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: View)

    def set_clickable(self, clickable):
        raise NotImplementedError

    def set_long_clickable(self, clickable):
        raise NotImplementedError

    def set_focusable(self, focusable):
        raise NotImplementedError

    def set_key_events(self, focusable):
        raise NotImplementedError

    def set_animations(self, animations):
        raise NotImplementedError

    def set_style(self, style):
        raise NotImplementedError

    def set_background_color(self, color):
        raise NotImplementedError

    def set_alpha(self, alpha):
        raise NotImplementedError

    def set_layout(self, layout):
        raise NotImplementedError

    def set_width(self, width):
        raise NotImplementedError

    def set_height(self, height):
        raise NotImplementedError

    def set_x(self, x):
        raise NotImplementedError

    def set_y(self, y):
        raise NotImplementedError

    def set_z(self, z):
        raise NotImplementedError

    def set_margin(self, margin):
        raise NotImplementedError

    def set_padding(self, padding):
        raise NotImplementedError

    def set_gravity(self, gravity):
        raise NotImplementedError

    def set_min_height(self, min_height):
        raise NotImplementedError

    def set_max_height(self, max_height):
        raise NotImplementedError

    def set_min_width(self, min_width):
        raise NotImplementedError

    def set_max_width(self, max_width):
        raise NotImplementedError

    def set_flex_grow(self, flex_grow):
        raise NotImplementedError

    def set_flex_basis(self, flex_basis):
        raise NotImplementedError

    def set_flex_shrink(self, flex_shrink):
        raise NotImplementedError

    def set_align_self(self, align_self):
        raise NotImplementedError


class View(ToolkitObject):
    """ View is a view group that displays
        child views in relative positions.

    """
    #: Widget is enabled
    enabled = d_(Bool(True))

    #: Show or hide
    visible = d_(Bool(True))

    #: Observe click events
    clickable = d_(Bool())

    #: Set whether the view can be long clicked
    long_clickable = d_(Bool())

    #: Set whether the view can be focused
    focusable = d_(Bool())

    #: Observe key events
    key_events = d_(Bool())

    #: Observe touch events
    touch_events = d_(Bool())

    #: Called when view is clicked
    clicked = d_(Event(), writable=False)

    #: Called when a key event occurs
    key_event = d_(Event(dict), writable=False)

    #: Called when a touch event occurs
    touch_event = d_(Event(dict), writable=False)

    #: Animations
    animations = d_(Typed(dict))
    animate = d_(Bool())

    # -------------------------------------------------------------------------
    # Style
    # -------------------------------------------------------------------------
    #: Foreground alpha
    alpha = d_(Float(1.0, strict=False))

    #: Background color
    background_color = d_(Unicode())

    # -------------------------------------------------------------------------
    # Layout
    # -------------------------------------------------------------------------
    #: Width and height or a string "match_parent" or "fill_parent"
    width = d_(Coerced(int, coercer=coerce_size))
    height = d_(Coerced(int, coercer=coerce_size))

    #: Layout gravity
    gravity = d_(Coerced(int, coercer=coerce_gravity))

    left = d_(Int())
    top = d_(Int())
    right = d_(Int())
    bottom = d_(Int())

    min_height = d_(Int())
    max_height = d_(Int())

    min_width = d_(Int())
    max_width = d_(Int())

    margin = d_(Tuple(int))
    padding = d_(Tuple(int))

    x = d_(Float(strict=False))
    y = d_(Float(strict=False))
    z = d_(Float(strict=False))

    #: The Position property tells Flexbox how you want your item to be
    #: positioned within its parent.
    position = d_(Enum('relative', 'absolute'))

    #: How to align children along the cross axis of their container
    align_self = d_(Enum('auto', 'stretch', 'flex_start',
                         'flex_end', 'center'))

    #: The FlexBasis property is an axis-independent way of providing the
    #: default size of an item on the main axis. Setting the FlexBasis of a
    #: child is similar to setting the Width of that child if its parent is a
    #: container with FlexDirection = row or setting the Height of a child
    #: if its parent is a container with FlexDirection = column. The FlexBasis
    #: of an item is the default size of that item, the size of the item
    #: before any FlexGrow and FlexShrink calculations are performed.
    flex_basis = d_(Float(strict=False))
    flex_grow = d_(Float(strict=False))
    flex_shrink = d_(Float(strict=False))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('enabled', 'clickable', 'long_clickable', 'focusable',
             'animate', 'animations', 'key_events', 'touch_events', 'visible',
             'background_color', 'alpha', 'width', 'height', 'min_height', 
             'min_width', 'max_height', 'max_width', 'x', 'y', 'z', 'gravity', 
             'top', 'bottom', 'right', 'left', 'margin', 'padding', 
             'flex_basis', 'flex_grow', 'flex_shrink', 'align_self',
             'position')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(View, self)._update_proxy(change)
