"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, Subclass, set_default

from enamlnative.widgets.view_group import ProxyViewGroup
from enamlnative.widgets.view import coerce_size

from .android_view import AndroidView, View, LayoutParams
from .bridge import JavaMethod


class ViewGroup(View):
    __nativeclass__ = set_default('android.view.ViewGroup')
    addViewWithParams = JavaMethod('android.view.View', 'int',
                         'android.view.ViewGroup$LayoutParams')
    addView = JavaMethod('android.view.View', 'int')

    removeView = JavaMethod('android.view.View')

    def __init__(self, *args, **kwargs):
        ViewGroup.addViewWithParams.set_name('addView')
        super(ViewGroup, self).__init__(*args, **kwargs)



class MarginLayoutParams(LayoutParams):
    __nativeclass__ = set_default('android.view.ViewGroup$MarginLayoutParams')
    __signature__ = set_default(('int', 'int'))
    setMargins = JavaMethod('int', 'int', 'int', 'int')
    setLayoutDirection = JavaMethod('int')


class AndroidViewGroup(AndroidView, ProxyViewGroup):
    """ An Android implementation of an Enaml ProxyViewGroup.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ViewGroup)

    #: Layout type
    layout_param_type = Subclass(LayoutParams, default=MarginLayoutParams)

    #: Default layout params
    default_layout = set_default({
        'width': 'match_parent',
        'height': 'match_parent'
    })

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ViewGroup(self.get_context())

    def init_layout(self):
        """ Add all child widgets to the view
        """
        super(AndroidViewGroup, self).init_layout()
        widget = self.widget
        i = 0
        for child in self.children():
            child_widget = child.widget
            if child_widget:
                if child.layout_params:
                    widget.addViewWithParams(child_widget, i,
                                             child.layout_params)
                else:
                    widget.addView(child_widget, i)
                i += 1

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
                if child.layout_params:
                    widget.addViewWithParams(child_widget, i,
                                             child.layout_params)
                else:
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
                                     int(r*dp), int(b*dp))
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
            # padding
            if 'padding' in layout:
                dp = self.dp
                l, t, r, b = layout['padding']
                w.setPadding(int(l*dp), int(t*dp),
                             int(r*dp), int(b*dp))

            # left, top, right, bottom
            if 'left' in layout:
                w.setLeft(layout['left'])
            if 'top' in layout:
                w.setTop(layout['top'])
            if 'right' in layout:
                w.setRight(layout['right'])
            if 'bottom' in layout:
                w.setBottom(layout['bottom'])

            # x, y, z
            if 'x' in layout:
                w.setX(layout['x'])
            if 'y' in layout:
                w.setY(layout['y'])
            if 'z' in layout:
                w.setZ(layout['z'])

            # set min width and height
            # maximum is not supported by AndroidViews (without flexbox)
            if 'min_height' in layout:
                w.setMinimumHeight(layout['min_height'])
            if 'min_width' in layout:
                w.setMinimumWidth(layout['min_width'])

        child.layout_params = layout_params
