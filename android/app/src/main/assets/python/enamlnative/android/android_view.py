#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import jnius
from atom.api import Typed

from enamlnative.widgets.view import ProxyView

from .android_widget import AndroidWidget

_LayoutDirection = jnius.autoclass('android.util.LayoutDirection')
_View = jnius.autoclass('android.view.View')

class AndroidView(AndroidWidget, ProxyView):
    """ An Android implementation of an Enaml ProxyView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(_View)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = _View(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidView, self).init_widget()
        d = self.declaration
        self.set_layout_direction(d.layout_direction)
        if d.top:
            self.set_top(d.top)
        if d.bottom:
            self.set_bottom(d.bottom)
        if d.left:
            self.set_left(d.left)
        if d.right:
            self.set_right(d.right)
        if d.x:
            self.set_x(d.x)
        if d.y:
            self.set_y(d.y)
        if d.z:
            self.set_y(d.z)

    #--------------------------------------------------------------------------
    # ProxyView API
    #--------------------------------------------------------------------------
    def set_top(self, top):
        self.widget.setTop(top)

    def set_bottom(self, bottom):
        self.widget.setBottom(bottom)

    def set_left(self, left):
        self.widget.setLeft(left)

    def set_right(self, right):
        self.widget.setRight(right)

    def set_layout_direction(self, direction):
        if direction != 'none':
            d = getattr(_LayoutDirection,direction.upper())
            self.widget.setLayoutDirection(d)


    def set_x(self, x):
        self.widget.setX(x)

    def set_y(self, y):
        self.widget.setY(y)

    def set_z(self, z):
        self.widget.setZ(z)


