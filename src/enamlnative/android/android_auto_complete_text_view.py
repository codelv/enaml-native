"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

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
        context = self.get_context()
        self.widget = AutoCompleteTextView(context)
        self.adapter = ArrayAdapter(context, '@layout/simple_list_item_1')

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidAutoCompleteTextView, self).init_widget()
        self.widget.setAdapter(self.adapter)

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


