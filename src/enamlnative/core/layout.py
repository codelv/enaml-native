"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 29, 2017

@author jrm

"""


from atom.api import Atom, Int, Enum, Float, Bool


class FlexParams(Atom):
    """ Attributes for a child of a Flexbox node."""
    #: How to align children along the cross axis of their container
    align_self = Enum('auto', 'stretch', 'flex_start', 'flex_end', 'center')

    #: The FlexBasis property is an axis-independent way of providing the
    #: default size of an item on the main axis. Setting the FlexBasis of a
    #: child is similar to setting the Width of that child if its parent is a
    #: container with FlexDirection = row or setting the Height of a child
    #: if its parent is a container with FlexDirection = column. The FlexBasis
    #: of an item is the default size of that item, the size of the item
    #: before any FlexGrow and FlexShrink calculations are performed.
    flex_basis = Float()

    #: The FlexGrow property describes how any space within a container should
    #: be distributed among its children along the main axis. After laying out
    #: its children, a container will distribute any remaining space according
    #: to the FlexGrow values specified by its children.
    flex_grow = Float(strict=False)

    #: The FlexShrink property describes how to shrink children along the
    #: main axisin the case that the total size of the children overflow the
    #: size of the containeron the main axis.
    flex_shrink = Float(strict=False)

    left = Int()
    top = Int()
    right = Int()
    bottom = Int()
    start = Int()
    end = Int()

    min_height = Int()
    max_height = Int()

    min_width = Int()
    max_width = Int()

    margin_left = Int()
    margin_top = Int()
    margin_right = Int()
    margin_bottom = Int()
    margin_start = Int()
    margin_end = Int()
    margin = Int()

    padding_left = Int()
    padding_top = Int()
    padding_right = Int()
    padding_bottom = Int()
    padding_start = Int()
    padding_end = Int()
    padding = Int()

    border_left = Int()
    border_top = Int()
    border_right = Int()
    border_bottom = Int()
    border_start = Int()
    border_end = Int()
    border = Int()


class FlexboxLayoutParams(FlexParams):
    """ A model for flexbox layout parameters """
    #: How to align children along the cross axis of their container
    align_items = Enum('stretch', 'flex_start', 'flex_end', 'center')

    #: Control how multiple lines of content are aligned within a
    #: container which uses FlexWrap
    align_content = Enum('flex_start', 'flex_end', 'center',
                         'space_between', 'space_around')

    #: Should the layout be a column or a row.
    flex_direction = Enum('row', 'column', 'row_reversed', 'column_reversed')

    #: Wrap or nowrap
    flex_wrap = Bool()

    #: How to align children within the main axis of a container
    justify_content = Enum('flex_start', 'flex_end', 'center',
                           'space_between', 'space_around')

    #: The Position property tells Flexbox how you want your item to be
    #: positioned within its parent.
    position = Enum('relative', 'absolute')

