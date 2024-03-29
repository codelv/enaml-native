"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Typed
from enamlnative.widgets.grid_layout import ProxyGridLayout
from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaMethod


class GridLayout(ViewGroup):
    __nativeclass__ = "android.widget.GridLayout"
    setOrientation = JavaMethod(int)
    setAlignmentMode = JavaMethod(int)
    setColumnCount = JavaMethod(int)
    setColumnOrderPreserved = JavaMethod(bool)
    setRowCount = JavaMethod(int)
    setRowOrderPreserved = JavaMethod(bool)
    setUseDefaultMargins = JavaMethod(bool)


class GridLayoutParams(ViewGroup):
    __nativeclass__ = "android.widget.GridLayout$LayoutParams"


class AndroidGridLayout(AndroidViewGroup, ProxyGridLayout):
    """An Android implementation of an Enaml ProxyGridLayout."""

    #: A reference to the widget created by the proxy.
    widget = Typed(GridLayout)

    #: Update default
    # layout_param_type = set_default(GridLayoutParams)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = GridLayout(self.get_context(), None, d.style)

    # -------------------------------------------------------------------------
    # ProxyGridLayout API
    # -------------------------------------------------------------------------
    def set_orientation(self, orientation):
        self.widget.setOrientation(0 if orientation == "horizontal" else 1)

    def set_alignment_mode(self, mode):
        self.widget.setAlignmentMode(1 if mode == "margins" else 0)

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
