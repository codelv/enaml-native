'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed, Subclass, Float

from enamlnative.widgets.view import ProxyView

from .android_widget import AndroidWidget, View


#Color = jnius.autoclass('android.graphics.Color')
LayoutParams = jnius.autoclass('android.view.ViewGroup$LayoutParams')
MarginLayoutParams = jnius.autoclass('android.view.ViewGroup$MarginLayoutParams')
LayoutDirection = jnius.autoclass('android.util.LayoutDirection')


class OnClickListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/view/View$OnClickListener']

    def __init__(self, handler):
        self.__handler__ = handler
        super(OnClickListener, self).__init__()

    @jnius.java_method('(Landroid/view/View;)V')
    def onClick(self, view):
        self.__handler__.on_click(view)

CACHE = {}


class AndroidView(AndroidWidget, ProxyView):
    """ An Android implementation of an Enaml ProxyView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(View)

    #: Display metrics density
    dp = Float()
    
    #: Reference to click listener
    click_listener = Typed(OnClickListener)

    def _default_dp(self):
        if 'dp' not in CACHE:
            CACHE['dp'] = 1.0#self.get_context().getResources().getDisplayMetrics().density
        return CACHE['dp']

    #: Default layout params
    layout_params = Subclass(jnius.JavaClass)

    def _default_layout_params(self):
        return MarginLayoutParams


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
        if d.background_color:
            self.set_background_color(d.background_color)
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
        if d.margins:
            self.set_margins(d.margins)
        if d.layout_width or d.layout_height:
            self.get_layout_params()
        if d.clickable:
            self.click_listener = OnClickListener(self)
            self.widget.setOnClickListener(self.click_listener)
            self.set_clickable(d.clickable)

    def get_layout_params(self):
        """ Get the layout params for this widget. If none exists,
            set the layout params to an instance of ViewGroup.MarginLayoutParams

        """
        return  #: TODO: implement
        #: Try to get existing
        params = self.widget.getLayoutParams()
        if params:
            return params

        #:
        d = self.declaration
        if d.layout_width:
            layout_width = getattr(LayoutParams, d.layout_width.upper())
        else:
            layout_width = LayoutParams.MATCH_PARENT
        if d.layout_height:
            layout_height = getattr(LayoutParams, d.layout_height.upper())
        else:
            layout_height = LayoutParams.MATCH_PARENT

        params = self.layout_params(
            layout_width,
            layout_height
        )

        self.widget.setLayoutParams(params)

        return params
    

    def on_click(self, view):
        """ Trigger the click

        """
        d = self.declaration
        d.clicked()

    #--------------------------------------------------------------------------
    # ProxyView API
    #--------------------------------------------------------------------------
    def set_background_color(self, color):
        self.widget.setBackgroundColor(color)
        
    def set_clickable(self, clickable):
        self.widget.setClickable(clickable)    

    def set_top(self, top):
        self.widget.setTop(top)

    def set_bottom(self, bottom):
        self.widget.setBottom(bottom)

    def set_left(self, left):
        self.widget.setLeft(left)

    def set_right(self, right):
        self.widget.setRight(right)

    def set_layout_width(self, width):
        self.get_layout_params()

    def set_layout_height(self, height):
        self.get_layout_params()

    def set_layout_direction(self, direction):
        if direction != 'none':
            d = getattr(LayoutDirection,direction.upper())
            self.widget.setLayoutDirection(d)

    def set_margins(self, margins):
        dp = self.dp
        l, t, r, b = margins
        self.get_layout_params().setMargins(int(l*dp), int(t*dp),
                                            int(r*dp), int(b*dp))

    def set_padding(self, padding):
        dp = self.dp
        l, t, r, b = padding
        self.widget.setPadding(int(l*dp), int(t*dp),
                               int(r*dp), int(b*dp))

    def set_x(self, x):
        self.widget.setX(x)

    def set_y(self, y):
        self.widget.setY(y)

    def set_z(self, z):
        self.widget.setZ(z)


