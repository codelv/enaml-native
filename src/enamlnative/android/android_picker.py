"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 6, 2017


"""
from atom.api import Typed, set_default
from enamlnative.widgets.picker import ProxyPicker
from .android_linear_layout import AndroidLinearLayout, LinearLayout
from .bridge import JavaCallback, JavaMethod


class Picker(LinearLayout):
    __nativeclass__ = "android.widget.NumberPicker"
    #: TODO: How to do a list??
    # setDisplayedValues = JavaMethod('java.lang.String[]')
    setMaxValue = JavaMethod(int)
    setMinValue = JavaMethod(int)
    setValue = JavaMethod(int)
    setTextColor = JavaMethod("android.graphics.Color")
    setTextSize = JavaMethod(float)
    setSelectionDividerHeight = JavaMethod(int)
    setOnLongPressUpdateInterval = JavaMethod("long")
    setOnValueChangedListener = JavaMethod(
        "android.widget.NumberPicker$OnValueChangeListener"
    )
    onValueChange = JavaCallback("android.widget.NumberPicker", int, int)
    setDisplayedValues = JavaMethod(list[str])
    setWrapSelectorWheel = JavaMethod(bool)


class AndroidPicker(AndroidLinearLayout, ProxyPicker):
    """An Android implementation of an Enaml ProxyPicker."""

    #: A reference to the widget created by the proxy.
    widget = Typed(Picker)

    default_layout = set_default({"width": "wrap_content", "height": "wrap_content"})  # type: ignore

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = Picker(
            self.get_context(), None, d.style or "@attr/numberPickerStyle"
        )

    def init_widget(self):
        """Set the checked state after all children have
        been populated.

        """
        super().init_widget()
        d = self.declaration
        w = self.widget
        if d.text_color:
            self.set_text_color(d.text_color)
        if d.text_size:
            self.set_text_size(d.text_size)
        if d.divider_height:
            self.set_divider_height(d.divider_height)

        if d.items:
            self.set_items(d.items)
        else:
            if d.max_value:
                self.set_max_value(d.max_value)
            if d.min_value:
                self.set_min_value(d.min_value)
        self.set_value(d.value)
        if d.wraps:
            self.set_wraps(d.wraps)

        if d.long_press_update_interval:
            self.set_long_press_update_interval(d.long_press_update_interval)

        w.setOnValueChangedListener(w.getId())
        w.onValueChange.connect(self.on_value_change)

    # -------------------------------------------------------------------------
    # OnValueChangeListener API
    # -------------------------------------------------------------------------
    def on_value_change(self, picker, old, new):
        """Set the checked property based on the checked state
        of all the children

        """
        d = self.declaration
        with self.widget.setValue.suppressed():
            d.value = new

    # -------------------------------------------------------------------------
    # ProxyNumberPicker API
    # -------------------------------------------------------------------------
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

    def set_items(self, items):
        w = self.widget
        w.setMinValue(0)
        w.setDisplayedValues(items)
        w.setMaxValue(len(items) - 1)  # max-min + 1 wtf

    def set_text_color(self, color: str):
        w = self.widget
        assert w is not None
        w.setTextColor(color)

    def set_text_size(self, size: float):
        w = self.widget
        assert w is not None
        w.setTextSize(size)

    def set_divider_height(self, height: int):
        w = self.widget
        assert w is not None
        w.setSelectionDividerHeight(height)
