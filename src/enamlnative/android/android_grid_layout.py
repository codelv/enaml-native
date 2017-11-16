"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.grid_layout import ProxyGridLayout

from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaMethod


class GridLayout(ViewGroup):
    __nativeclass__ = set_default('android.widget.GridLayout')
    setOrientation = JavaMethod('int')
    setAlignmentMode = JavaMethod('int')
    setColumnCount = JavaMethod('int')
    setColumnOrderPreserved = JavaMethod('boolean')
    setRowCount = JavaMethod('int')
    setRowOrderPreserved = JavaMethod('boolean')
    setUseDefaultMargins = JavaMethod('boolean')


class AndroidGridLayout(AndroidViewGroup, ProxyGridLayout):
    """ An Android implementation of an Enaml ProxyGridLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(GridLayout)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = GridLayout(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidGridLayout, self).init_widget()
        d = self.declaration
        self.set_orientation(d.orientation)
        self.set_alignment_mode(d.alignment_mode)
        if d.columns:
            self.set_columns(d.columns)
        if d.column_order_preserved:
            self.set_column_order_preserved(d.column_order_preserved)
        if d.rows:
            self.set_rows(d.rows)
        if d.row_order_preserved:
            self.set_row_order_preserved(d.row_order_preserved)
        if d.use_default_margins:
            self.set_use_default_margins(d.use_default_margins)

    # -------------------------------------------------------------------------
    # ProxyGridLayout API
    # -------------------------------------------------------------------------
    def set_orientation(self, orientation):
        self.widget.setOrientation(0 if orientation == 'horizontal' else 1)

    def set_alignment_mode(self, mode):
        self.widget.setAlignmentMode(1 if mode == 'margins' else 0)

    def set_columns(self, columns):
        self.widget.setColumnCount(columns)

    def set_column_order_preserved(self, preserved):
        self.widget.setColumnOrderPreserved(preserved)

    def set_rows(self, rows):
        self.widget.setRowCount(rows)

    def set_row_order_preserved(self, preserved):
        self.widget.setRowOrderPreserved(preserved)

    def set_use_default_margins(self, use_default):
        self.widget.setUseDefaultMargins(use_default)
