"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, List, set_default

from enamlnative.widgets.spinner import ProxySpinner

from .android_adapter import ArrayAdapter, AndroidAdapterView, AdapterView
from .bridge import JavaMethod


class AbsSpinner(AdapterView):
    __nativeclass__ = set_default('android.widget.AbsSpinner')
    pointToPosition = JavaMethod('int', 'int')
    setAdapter = JavaMethod('android.widget.SpinnerAdapter')


class Spinner(AbsSpinner):
    __nativeclass__ = set_default('android.widget.Spinner')
    __signature__ = set_default(('android.content.Context', 'int'))
    setDropDownHorizontalOffset = JavaMethod('int')
    setDropDownVerticalOffset = JavaMethod('int')
    setDropDownWidth = JavaMethod('int')
    setEnabled = JavaMethod('boolean')
    setGravity = JavaMethod('int')
    setPrompt = JavaMethod('java.lang.CharSequence')


class AndroidSpinner(AndroidAdapterView, ProxySpinner):
    """ An Android implementation of an Enaml ProxySpinner.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Spinner)

    #: Reference to adapter
    adapter = Typed(ArrayAdapter)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        d = self.declaration
        mode = 1 if d.mode == 'dropdown' else 0
        self.widget = Spinner(self.get_context(), mode)

        # Create the adapter simple_spinner_item = 0x01090008
        self.adapter = ArrayAdapter(self.get_context(),
                                    '@layout/simple_spinner_dropdown_item')

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        w = self.widget
        # Selection listener
        w.setAdapter(self.adapter)
        w.setOnItemSelectedListener(w.getId())
        w.onItemSelected.connect(self.on_item_selected)
        w.onNothingSelected.connect(self.on_nothing_selected)
        super(AndroidSpinner, self).init_widget()

    def get_declared_items(self):
        selection = None
        for k, v in super(AndroidSpinner, self).get_declared_items():
            if k == 'selection':
                selection = (k, v)
            else:
                yield (k, v)
        # Select last
        if selection:
            yield selection

    # -------------------------------------------------------------------------
    # OnSelectionListener API
    # -------------------------------------------------------------------------
    def on_item_selected(self, parent, view, position, id):
        d = self.declaration
        with self.widget.setSelection.suppressed():
            d.selected = position

    def on_nothing_selected(self, parent):
        pass

    # -------------------------------------------------------------------------
    # ProxySpinner API
    # -------------------------------------------------------------------------
    def set_prompt(self, prompt):
        self.widget.setPrompt(prompt)

    def set_selected(self, selected):
        self.widget.setSelection(selected)

    def set_items(self, items):
        """ Generate the view cache

        """
        self.adapter.clear()
        self.adapter.addAll(items)

    def set_item_gravity(self, gravity):
        self.widget.setGravity(gravity)

    def set_drop_down_horizontal_offset(self, offset):
        self.widget.setDropDownHorizontalOffset(offset)

    def set_drop_down_vertical_offset(self, offset):
        self.widget.setDropDownVerticalOffset(offset)

    def set_drop_down_width(self, width):
        self.widget.setDropDownWidth(width)


