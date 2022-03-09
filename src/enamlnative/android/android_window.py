"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 24, 2017


"""
from atom.api import Typed
from enamlnative.widgets.window import ProxyWindow
from .android_toolkit_object import AndroidToolkitObject
from .bridge import JavaBridgeObject, JavaMethod


class Window(JavaBridgeObject):
    """Access to the activity over the bridge"""

    __nativeclass__ = "android.view.Window"

    #: https://developer.android.com/reference/android/
    # view/WindowManager.LayoutParams.html#FLAG_KEEP_SCREEN_ON
    FLAG_KEEP_SCREEN_ON = 128

    RESIZE_MODES = {
        "auto": 0,  # Pick pan or zoom based on presense of scroll view
        "resize": 16,
        "pan": 32,
    }

    addFlags = JavaMethod(int)
    clearFlags = JavaMethod(int)
    setStatusBarColor = JavaMethod("android.graphics.Color")
    setSoftInputMode = JavaMethod(int)

    def __del__(self):
        """Do not destroy the main window"""
        pass


class AndroidWindow(AndroidToolkitObject, ProxyWindow):
    widget = Typed(Window)

    def create_widget(self):
        self.widget = self.parent().window

    def init_widget(self):
        """ """
        d = self.declaration
        if d.keep_screen_on:
            self.set_keep_screen_on(d.keep_screen_on)
        if d.statusbar_color:
            self.set_statusbar_color(d.statusbar_color)
        self.set_keyboard_resize_mode(d.keyboard_resize_mode)

    def set_keep_screen_on(self, keep_on: bool):
        """Set or clear the window flag to keep the screen on"""
        widget = self.widget
        if widget is not None:
            if keep_on:
                widget.addFlags(Window.FLAG_KEEP_SCREEN_ON)
            else:
                widget.clearFlags(Window.FLAG_KEEP_SCREEN_ON)

    def set_statusbar_color(self, color: str):
        """Set the color of the system statusbar."""
        widget = self.widget
        if widget is not None:
            widget.setStatusBarColor(color)

    def set_keyboard_resize_mode(self, mode: str):
        widget = self.widget
        if widget is not None:
            widget.setSoftInputMode(Window.RESIZE_MODES[mode])
