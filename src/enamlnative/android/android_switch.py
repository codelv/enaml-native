"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on June 7, 2017


"""
from atom.api import Typed
from enamlnative.widgets.switch import ProxySwitch
from .android_compound_button import AndroidCompoundButton, CompoundButton
from .bridge import JavaMethod


class Switch(CompoundButton):
    __nativeclass__ = "android.widget.Switch"
    setShowText = JavaMethod(bool)
    setSplitTrack = JavaMethod(bool)
    setTextOff = JavaMethod("java.lang.CharSequence")
    setTextOn = JavaMethod("java.lang.CharSequence")


class AndroidSwitch(AndroidCompoundButton, ProxySwitch):
    """An Android implementation of an Enaml ProxySwitch."""

    #: A reference to the widget created by the proxy.
    widget = Typed(Switch)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = Switch(self.get_context(), None, d.style or "@attr/switchStyle")

    def init_widget(self):
        """Initialize the underlying widget."""
        super().init_widget()
        d = self.declaration
        self.set_show_text(d.show_text)
        if d.split_track:
            self.set_split_track(d.split_track)
        if d.text_off:
            self.set_text_off(d.text_off)
        if d.text_on:
            self.set_text_on(d.text_on)

    # -------------------------------------------------------------------------
    # ProxySwitch API
    # -------------------------------------------------------------------------
    def set_show_text(self, show: bool):
        app = self.get_context()
        activity = app.activity
        assert activity is not None
        if activity.api_level >= 21:
            w = self.widget
            assert w is not None
            w.setShowText(show)

    def set_split_track(self, split: bool):
        w = self.widget
        assert w is not None
        w.setSplitTrack(split)

    def set_text_off(self, text: str):
        w = self.widget
        assert w is not None
        w.setTextOff(text)

    def set_text_on(self, text: str):
        w = self.widget
        assert w is not None
        w.setTextOn(text)
