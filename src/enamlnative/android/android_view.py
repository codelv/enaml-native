"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, Instance, Subclass, Bool, Float, set_default

from enamlnative.widgets.view import ProxyView

from .android_toolkit_object import AndroidToolkitObject
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback, JavaField


class View(JavaBridgeObject):
    __nativeclass__ = set_default('android.view.View')
    __signature__ = set_default(('android.content.Context',))

    VISIBILITY_VISIBLE = 0
    VISIBILITY_INVISIBLE = 4
    VISIBILITY_GONE = 8

    onClick = JavaCallback('android.view.View')
    onKey = JavaCallback('android.view.View', 'int', 'android.view.KeyEvent')
    onTouch = JavaCallback('android.view.View', 'android.view.MotionEvent')
    setOnClickListener = JavaMethod('android.view.View$OnClickListener')
    setOnKeyListener = JavaMethod('android.view.View$OnKeyListener')
    setOnTouchListener = JavaMethod('android.view.View$OnTouchListener')
    setLayoutParams = JavaMethod('android.view.ViewGroup.LayoutParams')
    setBackgroundColor = JavaMethod('android.graphics.Color')
    setClickable = JavaMethod('boolean')
    setAlpha = JavaMethod('float')
    setTop = JavaMethod('int')
    setBottom = JavaMethod('int')
    setLeft = JavaMethod('int')
    setRight = JavaMethod('int')
    setLayoutDirection = JavaMethod('int')
    setLayoutParams = JavaMethod('android.view.ViewGroup$LayoutParams')
    setPadding = JavaMethod('int', 'int', 'int', 'int')

    getWindowToken = JavaMethod(returns='android.os.IBinder')

    setX = JavaMethod('int')
    setY = JavaMethod('int')
    setZ = JavaMethod('int')
    setMaximumHeight = JavaMethod('int')
    setMaximumWidth = JavaMethod('int')
    setMinimumHeight = JavaMethod('int')
    setMinimumWidth = JavaMethod('int')
    setEnabled = JavaMethod('boolean')
    setTag = JavaMethod('java.lang.Object')
    setToolTipText = JavaMethod('java.lang.CharSequence')
    setVisibility = JavaMethod('int')

    LAYOUT_DIRECTIONS = {
        'ltr': 0,
        'rtl': 1,
        'locale': 3,
        'inherit': 2,
    }


class LayoutParams(JavaBridgeObject):
    __nativeclass__ = set_default('android.view.ViewGroup$LayoutParams')
    width = JavaField('int')
    height = JavaField('int')
    LAYOUTS = {
        'fill_parent': -1,
        'match_parent': -1,
        'wrap_content': -2
    }


class MarginLayoutParams(LayoutParams):
    __nativeclass__ = set_default('android.view.ViewGroup$MarginLayoutParams')
    __signature__ = set_default(('int', 'int'))
    setMargins = JavaMethod('int', 'int', 'int', 'int')
    setLayoutDirection = JavaMethod('int')


class AndroidView(AndroidToolkitObject, ProxyView):
    """ An Android implementation of an Enaml ProxyView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(View)

    #: Display metrics density
    dp = Float(1.0)

    #: Layout type
    layout_param_type = Subclass(LayoutParams, default=MarginLayoutParams)

    #: Layout params
    layout_params = Instance(LayoutParams)

    #: Flag to know if layout params should be destroyed
    _destroy_layout_params = Bool()

    def _observe_layout_params(self, change):
        """ If layout_params is set, make sure it get's deleted later. """
        self._destroy_layout_params = True

    def _default_dp(self):
        return self.get_context().dp

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = View(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidView, self).init_widget()
        d = self.declaration
        #if d.layout_direction != 'ltr':  #: Default, no need to set it
        #    self.set_layout_direction(d.layout_direction)
        if d.tool_tip:
            self.set_tool_tip(d.tool_tip)
        if d.status_tip:
            self.set_status_tip(d.status_tip)
        if not d.enabled:
            self.set_enabled(d.enabled)
        # Don't make toplevel widgets visible during init or they will
        # flicker onto the screen. This applies particularly for things
        # like status bar widgets which are created with no parent and
        # then reparented by the status bar. Real top-level widgets must
        # be explicitly shown by calling their .show() method after they
        # are created.
        if self.widget and not d.visible:
            self.set_visible(d.visible)
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
        if d.alpha != 1:
            self.set_alpha(d.alpha)
        if d.padding:
            self.set_padding(d.padding)
        if d.margins or d.layout_width or d.layout_height:
            self.set_layout_params(self.layout_params)
            if d.margins:
                self.set_margins(d.margins)
        if d.clickable:
            self.widget.setOnClickListener(self.widget.getId())
            self.widget.onClick.connect(self.on_click)
            self.set_clickable(d.clickable)
        if d.key_events:
            self.widget.setOnKeyListener(self.widget.getId())
            self.widget.onKey.connect(self.on_key)
        if d.touch_events:
            self.widget.setOnTouchListener(self.widget.getId())
            self.widget.onTouch.connect(self.on_touch)
        if d.layout:
            self.set_layout(d.layout)

    def _default_layout_params(self):
        d = self.declaration
        LayoutParamsFactory = self.layout_param_type
        try:
            w = int(int(d.layout_width)*self.dp)
        except ValueError:
            w = LayoutParams.LAYOUTS[d.layout_width or 'match_parent']
        try:
            h = int(int(d.layout_height)*self.dp)
        except ValueError:
            h = LayoutParams.LAYOUTS[d.layout_height or 'match_parent']
        return LayoutParamsFactory(w, h)

    def destroy(self):
        """ Destroy layout params if needed. """
        super(AndroidView, self).destroy()
        if self._destroy_layout_params:
            del self.layout_params

    # -------------------------------------------------------------------------
    # OnClickListener API
    # -------------------------------------------------------------------------
    def on_click(self, view):
        """ Trigger the click

        """
        d = self.declaration
        d.clicked()

    # -------------------------------------------------------------------------
    # OnKeyListener API
    # -------------------------------------------------------------------------
    def on_key(self, view, key, event):
        """ Trigger the key event

        Parameters
        ----------
        view: int
            The ID of the view that sent this event
        key: int
            The code of the key that was pressed
        data: bytes
            The msgpack encoded key event

        """
        d = self.declaration
        r = {'key': key, 'result': False}
        d.key_event(r)
        return r['result']

    # -------------------------------------------------------------------------
    # OnTouchListener API
    # -------------------------------------------------------------------------
    def on_touch(self, view, event):
        """ Trigger the touch event

        Parameters
        ----------
        view: int
            The ID of the view that sent this event
        data: bytes
            The msgpack encoded key event

        """
        d = self.declaration
        r = {'event':event,'result':False}
        d.touch_event(r)
        return r['result']


    # -------------------------------------------------------------------------
    # ProxyView API
    # -------------------------------------------------------------------------
    def set_alpha(self, alpha):
        self.widget.setAlpha(alpha)

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

    def set_layout_height(self, height):
        try:
            h = int(int(height)*self.dp)
        except ValueError:
            h = LayoutParams.LAYOUTS[height or 'match_parent']
        self.layout_params.height = h

    def set_layout_width(self, width):
        try:
            w = int(int(width)*self.dp)
        except ValueError:
            w = LayoutParams.LAYOUTS[width or 'match_parent']
        self.layout_params.width = w

    def set_layout_direction(self, direction):
        d = View.LAYOUT_DIRECTIONS[direction]
        self.widget.setLayoutDirection(d)

    def set_layout_params(self, params):
        self.widget.setLayoutParams(params)

    def set_margins(self, margins):
        dp = self.dp
        l, t, r, b = margins
        self.layout_params.setMargins(int(l*dp), int(t*dp),
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

    def set_layout(self, layout):
        #: Hack for flexbox
        from .android_flexbox import FlexboxLayoutHelper
        FlexboxLayoutHelper.apply_layout(self)

    def set_minimum_size(self, min_size):
        """ Sets the minimum size of the widget.

        """
        # QWidget uses (0, 0) as the minimum size.
        if -1 in min_size:
            min_size = (0, 0)
        w,h = min_size
        self.widget.setMinimumWidth(w)
        self.widget.setMinimumHeight(h)

    def set_maximum_size(self, max_size):
        """ Sets the maximum size of the widget.

        """
        # QWidget uses 16777215 as the max size
        if -1 in max_size:
            max_size = (16777215, 16777215)
        w, h = max_size
        self.widget.setMaximumWidth(w)
        self.widget.setMaximumHeight(h)

    def set_enabled(self, enabled):
        """ Set the enabled state of the widget.

        """
        self.widget.setEnabled(enabled)

    def set_visible(self, visible):
        """ Set the visibility of the widget.

        """
        v = View.VISIBILITY_VISIBLE if visible else View.VISIBILITY_GONE
        self.widget.setVisibility(v)

    def set_tool_tip(self, tool_tip):
        """ Set the tool tip for the widget.

        """
        self.widget.setToolTipText(tool_tip)

    def set_status_tip(self, status_tip):
        """ Set the status tip for the widget.

        """
        return # Not implemented on android

    def ensure_visible(self):
        """ Ensure the widget is visible.

        """
        # 0 - visible, 4 - invisible, 8 - gone
        self.widget.setVisibility(View.VISIBILITY_VISIBLE)

    def ensure_hidden(self):
        """ Ensure the widget is hidden.

        """
        # 0 - visible, 2 - invisible, 8 - gone
        self.widget.setVisibility(View.VISIBILITY_GONE)