"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Mar 17, 2018
"""
from atom.api import Bool, Coerced, Enum, Float, ForwardTyped, Str, Typed
from enaml.core.declarative import d_, observe
from enaml.widgets.toolkit_object import ProxyToolkitObject, ToolkitObject
from .view import coerce_gravity, coerce_size


class ProxyPopupWindow(ProxyToolkitObject):
    """The abstract definition of a proxy dialgo object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: PopupWindow)

    def set_height(self, height):
        raise NotImplementedError

    def set_width(self, width):
        raise NotImplementedError

    def set_x(self, x):
        raise NotImplementedError

    def set_y(self, y):
        raise NotImplementedError

    def set_position(self, position):
        raise NotImplementedError

    def set_focusable(self, enabled):
        raise NotImplementedError

    def set_touchable(self, enabled):
        raise NotImplementedError

    def set_outside_touchable(self, enabled):
        raise NotImplementedError

    def set_background_color(self, color):
        raise NotImplementedError

    def set_show(self, show):
        raise NotImplementedError

    def set_style(self, style):
        raise NotImplementedError

    def set_animation(self, style):
        raise NotImplementedError


class PopupWindow(ToolkitObject):
    """A popup window that may contain a view."""

    #: Width and height or a string "match_parent" or "fill_parent"
    width = d_(Coerced(int, coercer=coerce_size))
    height = d_(Coerced(int, coercer=coerce_size))

    #: Layout gravity
    gravity = d_(Coerced(int, coercer=coerce_gravity))

    #: Position
    x = d_(Float(strict=False))
    y = d_(Float(strict=False))

    #: Set whether the popup window can be focused
    focusable = d_(Bool())

    #: Set whether the popup is touchable
    touchable = d_(Bool(True))

    #: Controls whether the pop-up will be informed of touch events outside
    #: of its window.
    outside_touchable = d_(Bool(True))

    #: Start the popup and display it on screen (or hide if False)
    show = d_(Bool())

    #: Background color of the window (white by default)
    background_color = d_(Str())

    #: If relative, show as a dropdown on the parent view, otherwise
    #: show at the position given by `x` and `y`.
    position = d_(Enum("relative", "absolute"))

    #: Animation style for the PopupWindow using the @style format
    #: (ex. @style/MyAnimation
    animation = d_(Str())

    #: PopupWindow style using the @style format
    #: (ex. @style/Theme_Light_NoTitleBar_Fullscreen
    style = d_(Str())

    #: A reference to the proxy object.
    proxy = Typed(ProxyPopupWindow)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe(
        "width",
        "height",
        "x",
        "y",
        "position",
        "focusable",
        "touchable",
        "outside_touchable",
        "show",
        "animation",
        "style",
        "background_color",
    )
    def _update_proxy(self, change):

        super()._update_proxy(change)

    def popup(self):
        """Show the window from code. This will initialize and activate
        if needed.

        Examples
        --------

        >>> enamldef ContextMenu(PopupWindow): popup:
              attr result: lambda text: None
              Button:
                text = "One"
                clicked ::
                  dialog.show = False
                  dialog.result(self.text)
              Button:
                text = "Two"
                clicked ::
                  dialog.show = False
                  dialog.result(self.text)
            def on_result(value):
              print("User clicked: {}".format(value))
            ContextMenu(result=on_result).popup()

        Notes
        ------
        This does NOT block. Callbacks should be used to handle click events
        or the `show` state should be observed to know when it is closed.

        """
        if not self.is_initialized:
            self.initialize()
        if not self.proxy_is_active:
            self.activate_proxy()
        self.show = True
