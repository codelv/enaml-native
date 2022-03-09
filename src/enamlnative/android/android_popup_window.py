"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Mar 17, 2018


"""
from atom.api import Bool, Typed
from enamlnative.android.android_toolkit_object import AndroidToolkitObject
from enamlnative.android.bridge import JavaBridgeObject, JavaCallback, JavaMethod
from enamlnative.widgets.popup_window import ProxyPopupWindow
from .android_content import Context
from .android_image_view import Drawable
from .android_view import View
from .android_utils import ColorDrawable, AttributeSet


class PopupWindow(JavaBridgeObject):
    #: Show the view for the specified duration.
    __nativeclass__ = "android.widget.PopupWindow"
    __signature__ = [Context, AttributeSet, int, "android.R"]
    dismiss = JavaMethod()
    setContentView = JavaMethod(View)
    setAnimationStyle = JavaMethod(int)
    setHeight = JavaMethod(int)
    setWidth = JavaMethod(int)

    showAsDropDown = JavaMethod(View, int, int, int)
    showAtLocation = JavaMethod(View, int, int, int)

    setFocusable = JavaMethod(bool)
    setTouchable = JavaMethod(bool)
    setOutsideTouchable = JavaMethod(bool)

    setAnimationStyle = JavaMethod("android.R")

    setOnDismissListener = JavaMethod("android.widget.PopupWindow$OnDismissListener")
    onDismiss = JavaCallback()

    setTouchInterceptor = JavaMethod("android.view.View$OnTouchListener", returns=bool)
    onTouch = JavaCallback(View, "android.view.MotionEvent")

    update = JavaMethod(View, int, int, int, int)
    update_ = JavaMethod(int, int, int, int)

    setBackgroundDrawable = JavaMethod(Drawable)


class AndroidPopupWindow(AndroidToolkitObject, ProxyPopupWindow):
    """An Android implementation of an Enaml ProxyPopupWindow."""

    #: A reference to the widget created by the proxy.
    window = Typed(PopupWindow)

    #: Whether the popup has been shown
    showing = Bool()

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget.

        A dialog is not a subclass of view, hence we don't set name as widget
        or children will try to use it as their parent.

        """
        d = self.declaration
        style = d.style or "@style/Widget.DeviceDefault.PopupMenu"
        self.window = PopupWindow(self.get_context(), None, 0, style)
        self.showing = False

    def init_widget(self):
        """Set the listeners"""
        w = self.window
        d = self.declaration
        self.set_background_color(d.background_color)
        self.set_touchable(d.touchable)
        self.set_outside_touchable(d.outside_touchable)

        # Listen for events
        w.setOnDismissListener(w.getId())
        w.onDismiss.connect(self.on_dismiss)
        super().init_widget()

    def init_layout(self):
        """If a view is given show it"""
        super().init_layout()

        #: Set the content
        for view in self.child_widgets():
            self.window.setContentView(view)
            break

        #: Show it if needed
        d = self.declaration
        if d.show:
            self.set_show(d.show)

    def child_added(self, child):
        """Overwrite the content view"""
        view = child.widget
        if view is not None:
            self.window.setContentView(view)

    def destroy(self):
        """A reimplemented destructor that cancels
        the dialog before destroying.

        """
        super().destroy()
        window = self.window
        if window:
            #: Clear the dismiss listener
            #: (or we get an error during the callback)
            window.setOnDismissListener(None)
            # window.dismiss()
            del self.window

    # -------------------------------------------------------------------------
    # DismissListener API
    # -------------------------------------------------------------------------
    def on_dismiss(self, dialog=None):
        d = self.declaration
        self.showing = False
        with self.window.dismiss.suppressed():
            d.show = False

    # -------------------------------------------------------------------------
    # ProxyPopupWindow API
    # -------------------------------------------------------------------------
    def update(self):
        """Update the PopupWindow if it is currently showing. This avoids
        calling update during initialization.
        """
        if not self.showing:
            return
        d = self.declaration
        self.set_show(d.show)

    def set_background_color(self, color):
        color = color or "#FFF"
        self.window.setBackgroundDrawable(ColorDrawable(color))

    def set_touchable(self, enabled):
        self.window.setTouchable(enabled)

    def set_outside_touchable(self, enabled):
        self.window.setOutsideTouchable(enabled)

    def set_focusable(self, enabled):
        self.window.setFocusable(enabled)

    def set_width(self, width):
        self.window.setWidth(width)
        self.update()

    def set_height(self, height):
        self.window.setHeight(height)
        self.update()

    def set_x(self, x):
        self.update()

    def set_y(self, y):
        self.update()

    def set_position(self, position):
        self.update()

    def set_show(self, show: bool):
        d = self.declaration
        assert d is not None
        w = self.window
        assert w is not None
        dp = self.get_display_density()
        if show and self.showing:
            x, y = int(d.x * dp), int(d.y * dp)
            view = self.parent_widget()
            if d.position == "relative":
                w.update(view, x, y, d.width, d.height)
            else:
                w.update_(x, y, d.width, d.height)
        elif show:
            x, y = int(d.x * dp), int(d.y * dp)
            self.showing = True
            view = self.parent_widget()
            if d.position == "relative":
                w.showAsDropDown(view, x, y, d.gravity)
            else:
                w.showAtLocation(view, d.gravity, x, y)
        else:
            self.showing = False
            w.dismiss()

    def set_animation(self, style: str):
        w = self.window
        assert w is not None
        w.setAnimationStyle(style)

    def set_style(self, style: str):
        d = self.declaration
        assert d is not None
        if d.show and self.window is not None:
            self.window.dismiss()

        #: Recreate window with new style
        self.create_widget()
        self.init_widget()
        self.init_layout()
