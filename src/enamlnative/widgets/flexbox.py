"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Bool, Tuple, Float, Int, Enum, observe, set_default
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup


class ProxyFlexbox(ProxyViewGroup):
    """ The abstract definition of a proxy Flexbox object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Flexbox)

    def set_align_content(self, alignment):
        raise NotImplementedError

    def set_align_items(self, alignment):
        raise NotImplementedError

    def set_align_self(self, alignment):
        raise NotImplementedError

    def set_flex_direction(self, direction):
        raise NotImplementedError

    def set_flex_grow(self, grow):
        raise NotImplementedError

    def set_flex_shrink(self, shrink):
        raise NotImplementedError

    def set_flex_basis(self, basis):
        raise NotImplementedError

    def set_flex_wrap(self, wrap):
        raise NotImplementedError

    def set_left(self, left):
        raise NotImplementedError

    def set_top(self, top):
        raise NotImplementedError

    def set_bottom(self, bottom):
        raise NotImplementedError

    def set_right(self, right):
        raise NotImplementedError

    def set_start(self, start):
        raise NotImplementedError

    def set_end(self, end):
        raise NotImplementedError

    def set_justify_content(self, justify):
        raise NotImplementedError

    def set_min_height(self, height):
        raise NotImplementedError

    def set_max_height(self, height):
        raise NotImplementedError

    def set_min_width(self, width):
        raise NotImplementedError

    def set_max_width(self, width):
        raise NotImplementedError

    def set_margin_left(self, left):
        raise NotImplementedError

    def set_margin_top(self, top):
        raise NotImplementedError

    def set_margin_bottom(self, bottom):
        raise NotImplementedError

    def set_margin_right(self, right):
        raise NotImplementedError

    def set_margin_start(self, start):
        raise NotImplementedError

    def set_margin_end(self, end):
        raise NotImplementedError
    
    def set_margin(self, margin):
        raise NotImplementedError

    def set_padding_left(self, left):
        raise NotImplementedError

    def set_padding_top(self, top):
        raise NotImplementedError

    def set_padding_bottom(self, bottom):
        raise NotImplementedError

    def set_padding_right(self, right):
        raise NotImplementedError

    def set_padding_start(self, start):
        raise NotImplementedError

    def set_padding_end(self, end):
        raise NotImplementedError

    def set_padding(self, padding):
        raise NotImplementedError

    def set_border_left(self, left):
        raise NotImplementedError

    def set_border_top(self, top):
        raise NotImplementedError

    def set_border_bottom(self, bottom):
        raise NotImplementedError

    def set_border_right(self, right):
        raise NotImplementedError

    def set_border_start(self, start):
        raise NotImplementedError

    def set_border_end(self, end):
        raise NotImplementedError

    def set_border(self, border):
        raise NotImplementedError


class Flexbox(ViewGroup):
    """ A layout widget implementing flexbox's layout.

        This uses Facebook's yoga.

    """
    #: Default is to stretch so fill the parent
    layout_width = set_default('match_parent')

    #: Default is to stretch so fill the parent
    layout_height = set_default('match_parent')

    #: How to align children along the cross axis of their container
    align_items = d_(Enum('stretch', 'flex_start', 'flex_end', 'center'))

    #: How to align children along the cross axis of their container
    #align_self = d_(Enum('stretch', 'flex_start', 'flex_end', 'center'))

    #: Control how multiple lines of content are aligned within a
    #: container which uses FlexWrap
    align_content = d_(Enum('flex_start', 'flex_end', 'center',
                            'space_between', 'space_around'))

    #: Should the layout be a column or a row.
    flex_direction = d_(Enum('row', 'column', 'row_reversed',
                             'column_reversed'))

    #: The FlexBasis property is an axis-independent way of providing the default size of an item
    #: on the main axis. Setting the FlexBasis of a child is similar to setting the Width of that
    #: child if its parent is a container with FlexDirection = row or setting the Height of a child
    #: if its parent is a container with FlexDirection = column. The FlexBasis of an item is the d
    #: efault size of that item, the size of the item before any FlexGrow and FlexShrink
    #: calculations are performed.
    # flex_basis = d_(Int())
    #
    # #: The FlexGrow property describes how any space within a container should be distributed
    # #: among its children along the main axis. After laying out its children, a container will
    # #: distribute any remaining space according to the FlexGrow values specified by its children.
    # flex_grow = d_(Float(strict=False))
    #
    # #: The FlexShrink property describes how to shrink children along the main axis
    # #: in the case that the total size of the children overflow the size of the container
    # #: on the main axis.
    # flex_shrink = d_(Float(strict=False))
    #
    #: Wrap or nowrap
    flex_wrap = d_(Enum('nowrap', 'wrap', 'wrap_reverse'))

    #: How to align children within the main axis of a container
    justify_content = d_(Enum('flex_start', 'flex_end', 'center',
                              'space_between', 'space_around'))

    # #: The Position property tells Flexbox how you want your item to be positioned within its
    # #: parent.
    # position = d_(Enum('relative', 'absolute'))
    #
    # left = d_(Int())
    # top = d_(Int())
    # right = d_(Int())
    # bottom = d_(Int())
    # start = d_(Int())
    # end = d_(Int())
    #
    # min_height = d_(Int())
    # max_height = d_(Int())
    #
    # min_width = d_(Int())
    # max_width = d_(Int())
    #
    # margin_left = d_(Int())
    # margin_top = d_(Int())
    # margin_right = d_(Int())
    # margin_bottom = d_(Int())
    # margin_start = d_(Int())
    # margin_end = d_(Int())
    # margin = d_(Int())
    #
    # padding_left = d_(Int())
    # padding_top = d_(Int())
    # padding_right = d_(Int())
    # padding_bottom = d_(Int())
    # padding_start = d_(Int())
    # padding_end = d_(Int())
    # padding = d_(Int())
    #
    # border_left = d_(Int())
    # border_top = d_(Int())
    # border_right = d_(Int())
    # border_bottom = d_(Int())
    # border_start = d_(Int())
    # border_end = d_(Int())
    # border = d_(Int())

    #: A reference to the ProxyFlexbox object.
    proxy = Typed(ProxyFlexbox)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('align_items', 'align_content', 'align_self',
             'flex_direction', 'flex_wrap', 'flex_grow', 'flex_shrink',
             'flex_basis',
             'left', 'top', 'right', 'bottom', 'start', 'end',
             'margin_left', 'margin_top', 'margin_right', 'margin_bottom',
             'margin_start', 'margin_end', 'margin',
             'border_left', 'border_top', 'border_right', 'border_bottom',
             'border_start', 'border_end', 'border',
             'padding_left', 'padding_top', 'padding_right', 'padding_bottom',
             'padding_start', 'padding_end', 'padding',
             'min_width', 'min_height', 'max_width', 'max_height',
             'justify_content', 'position')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(Flexbox, self)._update_proxy(change)
