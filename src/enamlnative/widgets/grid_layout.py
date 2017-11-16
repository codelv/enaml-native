"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Enum, Bool, Int, observe, set_default
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup


class ProxyGridLayout(ProxyViewGroup):
    """ The abstract definition of a proxy GridLayout object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: GridLayout)

    def set_orientation(self, orientation):
        raise NotImplementedError

    def set_alignment_mode(self, mode):
        raise NotImplementedError

    def set_columns(self, columns):
        raise NotImplementedError

    def set_column_order_preserved(self, preserved):
        raise NotImplementedError

    def set_rows(self, rows):
        raise NotImplementedError

    def set_row_order_preserved(self, preserved):
        raise NotImplementedError

    def set_use_default_margins(self, use_default):
        raise NotImplementedError


class GridLayout(ViewGroup):
    """ A layout that places its children in a rectangular grid.

    """
    #: Should the layout be a column or a row.
    orientation = d_(Enum('horizontal', 'vertical'))

    #: Sets the alignment mode to be used for all of the alignments
    #: between the children of this container.
    alignment_mode = d_(Enum('margins', 'bounds'))

    #: ColumnCount is used only to generate default column/column
    #: indices when they are not specified by a component's layout parameters.
    columns = d_(Int(1))

    #: When this property is true, GridLayout is forced to place the column
    #: boundaries so that their associated grid indices are in ascending order
    #: in the view.
    column_order_preserved = d_(Bool())

    #: RowCount is used only to generate default row/column indices when they
    #: are not specified by a component's layout parameters.
    rows = d_(Int(1))

    #: When this property is true, GridLayout is forced to place the row
    #: boundaries so that their associated grid indices are in ascending order
    #: in the view.
    row_order_preserved = d_(Bool())

    #: When true, GridLayout allocates default margins
    #: around children based on the child's visual characteristics.
    use_default_margins = d_(Bool())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyGridLayout)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('orientation', 'alignment_mode', 'columns',
             'column_order_preserved', 'rows', 'row_order_preserved',
             'use_default_margins')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(GridLayout, self)._update_proxy(change)
