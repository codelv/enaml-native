"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.auto_complete_text_view import ProxyAutoCompleteTextView

from .android_adapter import ArrayAdapter
from .android_edit_text import AndroidEditText, EditText
from .bridge import JavaMethod


class AutoCompleteTextView(EditText):
    __nativeclass__ = set_default('android.widget.AutoCompleteTextView')
    setAdapter = JavaMethod('android.widget.ListAdapter')
    setDropDownHeight = JavaMethod('int')
    setDropDownWidth = JavaMethod('int')
    setListSelection = JavaMethod('int')
    setThreshold = JavaMethod('int')


class AndroidAutoCompleteTextView(AndroidEditText, ProxyAutoCompleteTextView):
    """ An Android implementation of an Enaml ProxyAutoCompleteTextView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(AutoCompleteTextView)

    #: An adapter to hold the choices
    adapter = Typed(ArrayAdapter)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = AutoCompleteTextView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidAutoCompleteTextView, self).init_widget()
        d = self.declaration
        if d.threshold:
            self.set_threshold(d.threshold)
        if d.drop_down_width:
            self.set_drop_down_width(d.drop_down_width)
        if d.drop_down_height:
            self.set_drop_down_height(d.drop_down_height)

        self.adapter = ArrayAdapter(self.get_context(),
                                    '@layout/simple_list_item_1')

        if d.choices:
            self.set_choices(d.choices)

        self.widget.setAdapter(self.adapter)

    def destroy(self):
        """ Properly destroy adapter """
        super(AndroidAutoCompleteTextView, self).destroy()
        if self.adapter:
            del self.adapter

    # -------------------------------------------------------------------------
    # ProxyAutoCompleteTextView API
    # -------------------------------------------------------------------------
    def set_choices(self, choices):
        self.adapter.clear()
        self.adapter.addAll(choices)

    def set_drop_down_height(self, height):
        self.widget.setDropDownHeight(height)

    def set_drop_down_width(self, width):
        self.widget.setDropDownWidth(width)

    def set_list_selection(self, index):
        self.widget.setListSelection(index)

    def set_threshold(self, threshold):
        self.widget.setThreshold(threshold)


