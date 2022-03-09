"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 25, 2017


"""
from atom.api import Typed
from enamlnative.widgets.time_picker import ProxyTimePicker
from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaCallback, JavaMethod


class TimePicker(FrameLayout):
    __nativeclass__ = "android.widget.TimePicker"
    onTimeChanged = JavaCallback("android.widget.TimePicker", int, int)
    setHour = JavaMethod(int)
    setMinute = JavaMethod(int)
    setCurrentHour = JavaMethod("java.lang.Integer")
    setCurrentMinute = JavaMethod("java.lang.Integer")
    setEnabled = JavaMethod(bool)
    setIs24HourView = JavaMethod("java.lang.Boolean")
    setOnTimeChangedListener = JavaMethod(
        "android.widget.TimePicker$OnTimeChangedListener"
    )


class AndroidTimePicker(AndroidFrameLayout, ProxyTimePicker):
    """An Android implementation of an Enaml ProxyTimePicker."""

    #: A reference to the widget created by the proxy.
    widget = Typed(TimePicker)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = TimePicker(
            self.get_context(), None, d.style or "@attr/timePickerStyle"
        )

    def init_widget(self):
        """Initialize the underlying widget."""
        super().init_widget()
        d = self.declaration
        w = self.widget
        self.set_hour(d.hour)
        self.set_minute(d.minute)
        self.set_hour_mode(d.hour_mode)

        w.setOnTimeChangedListener(w.getId())
        w.onTimeChanged.connect(self.on_time_changed)

    # -------------------------------------------------------------------------
    # OnTimeChangedListener API
    # -------------------------------------------------------------------------
    def on_time_changed(self, view, hour: int, minute: int):
        d = self.declaration
        assert d is not None
        w = self.widget
        assert w is not None
        with w.setHour.suppressed():
            d.hour = hour
        with w.setMinute.suppressed():
            d.minute = minute

    # -------------------------------------------------------------------------
    # ProxyFrameLayout API
    # -------------------------------------------------------------------------

    def _get_api_level(self) -> int:
        app = self.get_context()
        assert app.activity is not None
        return app.activity.api_level

    def set_hour(self, hour: int):
        w = self.widget
        assert w is not None
        if self._get_api_level() < 23:
            w.setCurrentHour(hour)
        else:
            w.setHour(hour)

    def set_minute(self, minute: int):
        w = self.widget
        assert w is not None
        if self._get_api_level() < 23:
            w.setCurrentMinute(minute)
        else:
            w.setMinute(minute)

    def set_hour_mode(self, mode: str):
        w = self.widget
        assert w is not None
        w.setIs24HourView(mode == "24")
