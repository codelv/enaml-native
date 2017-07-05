'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed, List, set_default

from enamlnative.widgets.spinner import ProxySpinner

from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class AdapterView(ViewGroup):
    __javaclass__ = set_default('android.widget.AdapterView')
    setEmptyView = JavaMethod('android.view.View')
    setFocusableInTouchMode = JavaMethod('boolean')
    setOnItemClickListener = JavaMethod('android.widget.AdapterView$OnItemClickListener')
    setOnItemLongClickListener = JavaMethod('android.widget.AdapterView$OnItemLongClickListener')
    setOnItemSelectedListener = JavaMethod('android.widget.AdapterView$OnItemSelectedListener')
    setSelection = JavaMethod('int')

    onItemClick = JavaMethod('android.widget.AdapterView', 'android.view.View', 'int', 'long')
    onItemLongClick = JavaMethod('android.widget.AdapterView', 'android.view.View', 'int', 'long')
    onItemSelected = JavaCallback('android.widget.AdapterView', 'android.view.View', 'int', 'long')
    onNothingSelected = JavaCallback('android.widget.AdapterView')


class AbsSpinner(AdapterView):
    __javaclass__ = set_default('android.widget.AbsSpinner')
    pointToPosition = JavaMethod('int', 'int')
    setAdapter = JavaMethod('android.widget.SpinnerAdapter')


class Spinner(AbsSpinner):
    __javaclass__ = set_default('android.widget.Spinner')
    __signature__ = set_default(('android.content.Context', 'int'))
    setDropDownHorizontalOffset = JavaMethod('int')
    setDropDownVerticalOffset = JavaMethod('int')
    setDropDownWidth = JavaMethod('int')
    setEnabled = JavaMethod('boolean')
    setGravity = JavaMethod('int')
    setPrompt = JavaMethod('java.lang.CharSequence')


class ArrayAdapter(JavaBridgeObject):
    __javaclass__ = set_default('android.widget.ArrayAdapter')
    __signature__ = set_default(('android.content.Context', 'int'))
    add = JavaMethod('java.lang.Object')
    remove = JavaMethod('java.lang.Object')
    clear = JavaMethod()
    #addAll = JavaMethod('int...') #: TODO implement this...


class AndroidSpinner(AndroidViewGroup, ProxySpinner):
    """ An Android implementation of an Enaml ProxySpinner.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Spinner)

    #: Reference to adapter
    adapter = Typed(ArrayAdapter)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        d = self.declaration
        mode = 1 if d.mode == 'dropdown' else 0
        self.widget = Spinner(self.get_context(), mode)

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidSpinner, self).init_widget()
        d = self.declaration
        self.set_prompt(d.prompt)
        if d.drop_down_width:
            self.set_drop_down_width(d.drop_down_width)
        if d.drop_down_horizontal_offset:
            self.set_drop_down_horizontal_offset(d.drop_down_horizontal_offset)
        if d.drop_down_vertical_offset:
            self.set_drop_down_vertical_offset(d.drop_down_vertical_offset)
        if d.gravity:
            self.set_gravity(d.gravity)

        #: Create the adapter simple_spinner_item = 0x01090008
        self.adapter = ArrayAdapter(self.get_context(), 0x01090008)
        if d.items:
            self.set_items(d.items)
        self.widget.setAdapter(self.adapter)

        if d.selected:
            self.set_selected(d.selected)

        #: Selection listener
        self.widget.setOnItemSelectedListener(self.widget.getId())
        self.widget.onItemSelected.connect(self.on_item_selected)
        self.widget.onNothingSelected.connect(self.on_nothing_selected)

    def destroy(self):
        """ Properly destroy adapter """
        super(AndroidSpinner, self).destroy()
        if self.adapter:
            del self.adapter

    # --------------------------------------------------------------------------
    # OnSelectionListener API
    # --------------------------------------------------------------------------

    def on_item_selected(self, parent, view, position, id):
        d = self.declaration
        with self.widget.setSelection.suppressed():
            d.selected = position

    def on_nothing_selected(self, parent):
        pass

    # --------------------------------------------------------------------------
    # ProxySpinner API
    # --------------------------------------------------------------------------
    def set_prompt(self, prompt):
        self.widget.setPrompt(prompt)

    def set_selected(self, selected):
        self.widget.setSelection(selected)

    def set_items(self, items):
        """ Generate the view cache

        """
        self.adapter.clear()
        for item in items:
            self.adapter.add(item)

    def set_gravity(self, gravity):
        #g = getattr(Gravity,gravity.upper())
        #self.widget.setGravity(gravity)
        pass

    def set_drop_down_horizontal_offset(self, offset):
        self.widget.setDropDownHorizontalOffset(offset)

    def set_drop_down_vertical_offset(self, offset):
        self.widget.setDropDownVerticalOffset(offset)

    def set_drop_down_width(self, width):
        self.widget.setDropDownWidth(width)


