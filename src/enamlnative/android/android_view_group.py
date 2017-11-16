"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.view_group import ProxyViewGroup

from .android_view import AndroidView, View, LayoutParams, MarginLayoutParams
from .bridge import JavaMethod

class Gravity:
    NO_GRAVITY = 0
    CENTER_HORIZONTAL = 1
    CENTER_VERTICAL = 16
    CENTER = 11
    FILL = 119
    FILL_HORIZONTAL = 7
    FILL_VERTICAL = 112
    TOP = 48
    BOTTOM = 80
    LEFT = 3
    RIGHT = 5
    START = 8388611
    END = 8388613


class ViewGroup(View):
    __nativeclass__ = set_default('android.view.ViewGroup')
    addView = JavaMethod('android.view.View', 'int')
    removeView = JavaMethod('android.view.View')


class AndroidViewGroup(AndroidView, ProxyViewGroup):
    """ An Android implementation of an Enaml ProxyViewGroup.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ViewGroup)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ViewGroup(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidViewGroup, self).init_widget()
        d = self.declaration
        if d.layout_gravity:
            self.set_layout_gravity(d.layout_gravity)

    def init_layout(self):
        """ Add all child widgets to the view
        """
        widget = self.widget
        for i, child_widget in enumerate(self.child_widgets()):
            widget.addView(child_widget, i)

    def child_added(self, child):
        """ Handle the child added event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super(AndroidViewGroup, self).child_added(child)

        widget = self.widget
        #: TODO: Should index be cached?
        for i, child_widget in enumerate(self.child_widgets()):
            if child_widget == child.widget:
                widget.addView(child_widget, i)

    def child_moved(self, child):
        """ Handle the child moved event from the declaration.

        """
        super(AndroidViewGroup, self).child_moved(child)
        #: Remove and re-add in correct spot
        self.child_removed(child)
        self.child_added(child)

    def child_removed(self, child):
        """ Handle the child removed event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super(AndroidViewGroup, self).child_removed(child)
        if child.widget is not None:
            self.widget.removeView(child.widget)

    # --------------------------------------------------------------------------
    # ProxyViewGroup API
    # --------------------------------------------------------------------------
    def set_layout_gravity(self, gravity):
        g = getattr(Gravity, gravity.upper())
        self.layout_params.gravity = g
