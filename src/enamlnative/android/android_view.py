"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, Dict, Instance, Subclass, Float, set_default

from .android_toolkit_object import AndroidToolkitObject
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback, JavaField

from enamlnative.widgets.view import ProxyView, coerce_size


LAYOUT_KEYS = (
    'x', 'y', 'z', 'width', 'height', 'gravity',
    'margin', 'padding', 'top', 'bottom', 'left', 'right',
    'align_self', 'flex_basis', 'flex_shrink', 'flex_grow', 'position',
    'max_width', 'min_width', 'max_height', 'min_height'
)


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

    setX = JavaMethod('float')
    setY = JavaMethod('float')
    setZ = JavaMethod('float')
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

    GRAVITIES = {
        'no_gravity': 0,
        'center_horizontal': 1,
        'center_vertical': 16,
        'center': 11,
        'fill': 119,
        'fill_horizontal': 7,
        'fill_vertical': 112,
        'top': 48,
        'bottom': 80,
        'left': 3,
        'right': 5,
        'start': 8388611,
        'end': 8388613
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


class AndroidView(AndroidToolkitObject, ProxyView):
    """ An Android implementation of an Enaml ProxyView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(View)

    #: Display metrics density
    dp = Float(1.0)

    #: Layout type
    layout_param_type = Subclass(LayoutParams)

    #: Layout params
    layout_params = Instance(LayoutParams)

    #: Default layout params
    default_layout = Dict(default={
        'width': 'wrap_content',
        'height': 'wrap_content'
    })

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
        
        This reads all items declared in the enamldef block for this node 
        and sets only the values that have been specified. All other values 
        will be left as default. Doing it this way makes atom to only create 
        the properties that need to be overridden from defaults thus greatly 
        reducing the number of initialization checks, saving time and memory.
        
        If you don't want this to happen override `get_declared_keys` 
        to return an empty list. 

        """
        super(AndroidView, self).init_widget()

        # Initialize the widget by updating only the members that
        # have read expressions declared. This saves a lot of time and
        # simplifies widget initialization code
        for k, v in self.get_declared_items():
            handler = getattr(self, 'set_'+k, None)
            if handler:
                handler(v)

    def get_declared_items(self):
        """ Get the members that were set in the enamldef block for this
        Declaration. Layout keys are grouped together until the end so as
        to avoid triggering multiple updates.
        
        Returns
        -------
        result: List of (k,v) pairs that were defined for this widget in enaml
            List of keys and values

        """
        d = self.declaration
        engine = d._d_engine
        if engine:
            layout = {}
            for k, h in engine._handlers.items():
                # Handlers with read operations
                if not h.read_pair:
                    continue
                v = getattr(d, k)
                if k in LAYOUT_KEYS:
                    layout[k] = v
                    continue
                yield (k, v)

            if layout:
                yield ('layout', layout)

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
        r = {'event': event, 'result': False}
        d.touch_event(r)
        return r['result']

    # -------------------------------------------------------------------------
    # ProxyView API
    # -------------------------------------------------------------------------
    def set_touch_events(self, enabled):
        w = self.widget
        if enabled:
            w.setOnTouchListener(w.getId())
            w.onTouch.connect(self.on_touch)
        else:
            w.onTouch.disconnect(self.on_touch)

    def set_key_events(self, enabled):
        w = self.widget
        if enabled:
            w.setOnKeyListener(w.getId())
            w.onKey.connect(self.on_key)
        else:
            w.onKey.disconnect(self.on_key)

    def set_clickable(self, clickable):
        w = self.widget
        if clickable:
            w.setOnClickListener(w.getId())
            w.onClick.connect(self.on_click)
        else:
            w.onClick.disconnect(self.on_click)
        w.setClickable(clickable)

    def set_enabled(self, enabled):
        """ Set the enabled state of the widget.

        """
        self.widget.setEnabled(enabled)

    def set_visible(self, visible):
        """ Set the visibility of the widget.

        """
        v = View.VISIBILITY_VISIBLE if visible else View.VISIBILITY_GONE
        self.widget.setVisibility(v)

    # -------------------------------------------------------------------------
    # Style updates
    # -------------------------------------------------------------------------
    def set_background_color(self, color):
        """ Set the background color of the widget.
        
        """
        self.widget.setBackgroundColor(color)

    def set_alpha(self, alpha):
        """ Sets the alpha or opacity of the widget. """
        self.widget.setAlpha(alpha)

    # -------------------------------------------------------------------------
    # Layout updates
    # -------------------------------------------------------------------------
    def set_layout(self, layout):
        """ Sets the LayoutParams of this widget. 
           
        Since the available properties that may be set for the layout params 
        depends on the parent, actual creation of the params is delegated to 
        the parent
        
        Parameters
        ----------
        layout: Dict
            A dict of layout parameters the parent should used to layout this
            child.  The widget defaults are updated with user passed values. 
        
        """
        # Update the layout with the widget defaults
        update = self.layout_params is not None
        params = self.default_layout.copy()
        params.update(layout)

        # Create the layout params
        parent = self.parent()

        if not isinstance(parent, AndroidView):
            # Root node
            parent = self
            update = True

        parent.apply_layout(self, params)
        if update:
            self.widget.setLayoutParams(self.layout_params)

    def update_layout(self, **params):
        """ Updates the LayoutParams of this widget. 
           
        This delegates to the parent and expects the parent to update the
        existing layout without recreating it.
        
        Parameters
        ----------
        params: Dict
            A dict of layout parameters the parent should used to layout this
            child.  The widget defaults are updated with user passed values. 
        
        """
        self.parent().apply_layout(self, params)

    def create_layout_params(self, child, layout):
        """ Create the LayoutParams for a child with it's requested
        layout parameters. Subclasses should override this as needed
        to handle layout specific needs.
        
        Parameters
        ----------
        child: AndroidView
            A view to create layout params for.
        layout: Dict
            A dict of layout parameters to use to create the layout.
             
        Returns
        -------
        layout_params: LayoutParams
            A LayoutParams bridge object with the requested layout options.
        
        """
        dp = self.dp
        w, h = (coerce_size(layout.get('width', 'wrap_content')),
                coerce_size(layout.get('height', 'wrap_content')))
        w = w if w < 0 else int(w * dp)
        h = h if h < 0 else int(h * dp)
        layout_params = self.layout_param_type(w, h)

        if layout.get('margin'):
            l, t, r, b = layout['margin']
            layout_params.setMargins(int(l*dp), int(t*dp),
                                     int(b*dp), int(r*dp))
        return layout_params

    def apply_layout(self, child, layout):
        """ Apply a layout to a child. This sets the layout_params
        of the child which is later used during the `init_layout` pass.
        Subclasses should override this as needed to handle layout specific
        needs of the ViewGroup.
        
        Parameters
        ----------
        child: AndroidView
            A view to create layout params for.
        layout: Dict
            A dict of layout parameters to use to create the layout.
        
        """
        layout_params = child.layout_params
        if not layout_params:
            layout_params = self.create_layout_params(child, layout)
        w = child.widget
        if w:
            dp = self.dp
            # padding
            if 'padding' in layout:
                l, t, r, b = layout['padding']
                w.setPadding(int(l*dp), int(t*dp),
                             int(b*dp), int(r*dp))

            # left, top, right, bottom
            if 'left' in layout:
                w.setLeft(int(layout['left']*dp))
            if 'top' in layout:
                w.setTop(int(layout['top']*dp))
            if 'right' in layout:
                w.setRight(int(layout['right']*dp))
            if 'bottom' in layout:
                w.setBottom(int(layout['bottom']*dp))

            # x, y, z
            if 'x' in layout:
                w.setX(layout['x']*dp)
            if 'y' in layout:
                w.setY(layout['y']*dp)
            if 'z' in layout:
                w.setZ(layout['z']*dp)

            # set min width and height
            # maximum is not supported by AndroidViews (without flexbox)
            if 'min_height' in layout:
                w.setMinimumHeight(int(layout['min_height']*dp))
            if 'min_width' in layout:
                w.setMinimumWidth(int(layout['min_width']*dp))

        child.layout_params = layout_params

    def set_width(self, width):
        self.update_layout(width=width)

    def set_height(self, height):
        self.update_layout(height=height)

    def set_padding(self, padding):
        self.update_layout(padding=padding)

    def set_margin(self, margin):
        self.update_layout(margin=margin)

    def set_x(self, x):
        self.update_layout(x=x)

    def set_y(self, y):
        self.update_layout(y=y)

    def set_z(self, z):
        self.update_layout(z=z)

    def set_top(self, top):
        self.update_layout(top=top)

    def set_left(self, left):
        self.update_layout(left=left)

    def set_right(self, right):
        self.update_layout(right=right)

    def set_bottom(self, bottom):
        self.update_layout(bottom=bottom)

    def set_gravity(self, gravity):
        self.update_layout(gravity=gravity)

    def set_min_height(self, min_height):
        self.update_layout(min_height=min_height)

    def set_max_height(self, max_height):
        self.update_layout(max_height=max_height)

    def set_min_width(self, min_width):
        self.update_layout(min_width=min_width)

    def set_max_width(self, max_width):
        self.update_layout(max_width=max_width)

    def set_flex_grow(self, flex_grow):
        self.update_layout(flex_grow=flex_grow)

    def set_flex_basis(self, flex_basis):
        self.update_layout(flex_basis=flex_basis)

    def set_flex_shrink(self, flex_shrink):
        self.update_layout(flex_shrink=flex_shrink)

    def set_align_self(self, align_self):
        self.update_layout(align_self=align_self)
