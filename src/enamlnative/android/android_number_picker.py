'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 6, 2017

@author: jrm
'''
from atom.api import Typed, set_default

from enamlnative.widgets.number_picker import ProxyNumberPicker

from .android_linear_layout import AndroidLinearLayout, LinearLayout
from .bridge import JavaCallback, JavaMethod


class NumberPicker(LinearLayout):
    __nativeclass__ = set_default('android.widget.NumberPicker')
    #: TODO: How to do a list??
    #setDisplayedValues = JavaMethod('java.lang.String[]')
    setMaxValue = JavaMethod('int')
    setMinValue = JavaMethod('int')
    setValue = JavaMethod('int')
    setOnLongPressUpdateInterval = JavaMethod('long')
    setOnValueChangedListener = JavaMethod('android.widget.NumberPicker$OnValueChangeListener')
    onValueChange = JavaCallback('android.widget.NumberPicker', 'int', 'int')
    setWrapSelectorWheel = JavaMethod('boolean')


class AndroidNumberPicker(AndroidLinearLayout, ProxyNumberPicker):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(NumberPicker)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = NumberPicker(self.get_context())

    def init_layout(self):
        """ Set the checked state after all children have
            been populated.
        """
        super(AndroidNumberPicker, self).init_layout()
        d = self.declaration

        if d.value:
            self.set_value(d.value)
        if d.max_value:
            self.set_max_value(d.max_value)
        if d.min_value:
            self.set_min_value(d.min_value)
        if d.wraps:
            self.set_wraps(d.wraps)
        if d.long_press_update_interval:
            self.set_long_press_update_interval(d.long_press_update_interval)

        self.widget.setOnValueChangedListener(self.widget.getId())
        self.widget.onValueChange.connect(self.on_value_change)

    # --------------------------------------------------------------------------
    # OnValueChangeListener API
    # --------------------------------------------------------------------------
    def on_value_change(self, picker, old, new):
        """ Set the checked property based on the checked state
            of all the children
        """
        d = self.declaration
        with self.widget.setValue.suppressed():
            d.value = new

    # --------------------------------------------------------------------------
    # ProxyNumberPicker API
    # --------------------------------------------------------------------------
    def set_max_value(self, value):
        self.widget.setMaxValue(value)

    def set_min_value(self, value):
        self.widget.setMinValue(value)

    def set_value(self, value):
        self.widget.setValue(value)

    def set_long_press_update_interval(self, interval):
        self.widget.setOnLongPressUpdateInterval(interval)

    def set_wraps(self, wraps):
        self.widget.setWrapSelectorWheel(wraps)