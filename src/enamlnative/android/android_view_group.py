"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017


"""
from atom.api import Typed, set_default
from enamlnative.widgets.view_group import ProxyViewGroup
from .android_view import AndroidView, LayoutParams, View
from .bridge import JavaBridgeObject, JavaMethod


class ViewGroup(View):
    __nativeclass__ = "android.view.ViewGroup"
    addView_ = JavaMethod(View, int, "android.view.ViewGroup$LayoutParams")
    addView = JavaMethod(View, int)

    removeView = JavaMethod(View)

    setLayoutTransition = JavaMethod("android.animation.LayoutTransition")


class MarginLayoutParams(LayoutParams):
    __nativeclass__ = "android.view.ViewGroup$MarginLayoutParams"
    __signature__ = [int, int]
    setMargins = JavaMethod(int, int, int, int)
    setLayoutDirection = JavaMethod(int)


class LayoutTransition(JavaBridgeObject):
    __nativeclass__ = "android.animation.LayoutTransition"


class AndroidViewGroup(AndroidView, ProxyViewGroup):
    """An Android implementation of an Enaml ProxyViewGroup."""

    #: A reference to the widget created by the proxy.
    widget = Typed(ViewGroup)

    #: Layout type
    layout_param_type = set_default(MarginLayoutParams)  # type: ignore

    #: Default layout params
    default_layout = set_default({"width": "match_parent", "height": "match_parent"})  # type: ignore

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        raise NotImplementedError

    def init_layout(self):
        """Add all child widgets to the view"""
        super().init_layout()
        widget = self.widget
        i = 0
        for child in self.children():
            child_widget = child.widget
            if child_widget:
                if child.layout_params:
                    widget.addView_(child_widget, i, child.layout_params)
                else:
                    widget.addView(child_widget, i)
                i += 1

        # Force layout using the default params
        if not self.layout_params:
            self.set_layout({})

    def child_added(self, child):
        """Handle the child added event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super().child_added(child)

        widget = self.widget
        #: TODO: Should index be cached?
        for i, child_widget in enumerate(self.child_widgets()):
            if child_widget == child.widget:
                if child.layout_params:
                    widget.addView_(child_widget, i, child.layout_params)
                else:
                    widget.addView(child_widget, i)

    def child_moved(self, child):
        """Handle the child moved event from the declaration."""
        super().child_moved(child)
        #: Remove and re-add in correct spot
        self.child_removed(child)
        self.child_added(child)

    def child_removed(self, child):
        """Handle the child removed event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super().child_removed(child)
        if child.widget is not None:
            self.widget.removeView(child.widget)

    def set_transition(self, transition):
        t = LayoutTransition() if transition == "default" else None
        self.widget.setLayoutTransition(t)
