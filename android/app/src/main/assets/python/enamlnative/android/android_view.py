'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.view import ProxyView

from .android_widget import AndroidWidget, View


LayoutDirection = jnius.autoclass('android.util.LayoutDirection')


class OnClickListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/view/View$OnClickListener']

    def __init__(self, handler):
        self.__handler__ = handler
        super(OnClickListener, self).__init__()

    @jnius.java_method('(Landroid/view/View;)V')
    def onClick(self, view):
        self.__handler__.on_click(view)


class AndroidView(AndroidWidget, ProxyView):
    """ An Android implementation of an Enaml ProxyView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(View)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = View(self.get_context())

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
        if d.padding:
            self.set_padding(d.padding)

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
            d = getattr(LayoutDirection,direction.upper())
            self.widget.setLayoutDirection(d)

    def set_padding(self, padding):
        d = self.get_context().getResources().getDisplayMetrics().density
        t,l,b,r = padding
        self.widget.setPadding(t*d,l*d,b*d,r*d)

    def set_x(self, x):
        self.widget.setX(x)

    def set_y(self, y):
        self.widget.setY(y)

    def set_z(self, z):
        self.widget.setZ(z)


