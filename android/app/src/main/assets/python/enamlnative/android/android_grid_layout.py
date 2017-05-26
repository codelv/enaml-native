'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.grid_layout import ProxyGridLayout

from .android_widget import AndroidWidget

GridLayout = jnius.autoclass('android.widget.GridLayout')

class AndroidGridLayout(AndroidWidget, ProxyGridLayout):
    """ An Android implementation of an Enaml ProxyGridLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(GridLayout)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = GridLayout(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidGridLayout, self).init_widget()
        d = self.declaration
        self.set_orientation(d.orientation)
        self.set_alignment_mode(d.alignment_mode)
        self.set_columns(d.columns)
        self.set_column_order_preserved(d.column_order_preserved)
        self.set_rows(d.rows)
        self.set_row_order_preserved(d.row_order_preserved)
        self.set_use_default_margins(d.use_default_margins)


    #--------------------------------------------------------------------------
    # ProxyGridLayout API
    #--------------------------------------------------------------------------
    def set_orientation(self, orientation):
        v = getattr(GridLayout,orientation.upper())
        self.widget.setOrientation(v)

    def set_alignment_mode(self, mode):
        v = getattr(GridLayout,'ALIGN_{}'.format(mode.upper()))
        self.widget.setAlignmentMode(v)

    def set_columns(self, columns):
        self.setColumnCount(columns)

    def set_column_order_preserved(self, preserved):
        self.setColumnOrderPreserved(preserved)

    def set_rows(self, rows):
        self.setRowCount(rows)

    def set_row_order_preserved(self, preserved):
        self.setRowOrderPreserved(preserved)

    def set_use_default_margins(self, use_default):
        self.setUseDefaultMargins(use_default)