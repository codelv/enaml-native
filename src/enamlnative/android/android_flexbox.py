"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.flexbox import ProxyFlexbox

from .android_view_group import AndroidViewGroup, ViewGroup, MarginLayoutParams
from .bridge import JavaMethod


class Flexbox(ViewGroup):
    __nativeclass__ = set_default('com.google.android.flexbox.FlexboxLayout')
    setFlexDirection = JavaMethod('int')
    setFlexWrap = JavaMethod('int')
    setJustifyContent = JavaMethod('int')
    setAlignItems = JavaMethod('int')
    setAlignContent = JavaMethod('int')
    setFlexLines = JavaMethod('java.util.List')
    setDividerDrawable = JavaMethod('android.graphics.drawable.Drawable')
    setDividerDrawableHorizontal = JavaMethod(
        'android.graphics.drawable.Drawable')
    setDividerDrawableVertical = JavaMethod(
        'android.graphics.drawable.Drawable')
    setShowDivider = JavaMethod('int')
    setShowDividerVertical = JavaMethod('int')
    setShowDividerHorizontal = JavaMethod('int')

    FLEX_DIRECTION = {
        'row': 0,
        'row_reversed': 1,
        'column': 2,
        'column_reversed': 3
    }

    FLEX_WRAP = {
        'nowrap': 0,
        'wrap': 1,
        'wrap_reverse': 2,
    }

    JUSTIFY_CONTENT = {
        'flex_start': 0,
        'flex_end': 1,
        'center': 2,
        'space_between': 3,
        'space_around': 4
    }

    ALIGN_ITEMS = {
        'flex_start': 0,
        'flex_end': 1,
        'center': 2,
        'baseline': 3,
        'stretch': 4
    }

    ALIGN_CONTENT = {
        'flex_start': 0,
        'flex_end': 1,
        'center': 2,
        'space_between': 3,
        'space_around': 4,
        'stretch': 5,
    }

    ALIGN_SELF = {
        'auto':-1,
        'flex_start': 0,
        'flex_end': 1,
        'center': 2,
        'baseline': 3,
        'stretch': 4
    }


    SHOW_DIVIDER = {
        'none': 0,
        'beginning': 1,
        'middle': 2,
        'end': 3,
    }


class FlexboxLayoutParams(MarginLayoutParams):
    """ Update the child widget with the given params 
    
    """
    __nativeclass__ = set_default(
        'com.google.android.flexbox.FlexboxLayout$LayoutParams')

    setWidth = JavaMethod('int')
    setHeight = JavaMethod('int')
    setOrder = JavaMethod('int')
    setFlexGrow = JavaMethod('float')
    setFlexShrink = JavaMethod('float')
    setAlignSelf = JavaMethod('int')
    setMinWidth = JavaMethod('int')
    setMinHeight = JavaMethod('int')
    setMaxWidth = JavaMethod('int')
    setMaxHeight = JavaMethod('int')
    setWrapBefore = JavaMethod('boolean')
    setFlexBasisPercent = JavaMethod('float')


class AndroidFlexbox(AndroidViewGroup, ProxyFlexbox):
    """ An Android implementation of an Enaml ProxyFlexbox.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Flexbox)

    #: Update default
    layout_param_type = set_default(FlexboxLayoutParams)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = Flexbox(self.get_context())

    # -------------------------------------------------------------------------
    # ProxyFlexbox API
    # -------------------------------------------------------------------------
    def set_align_content(self, alignment):
        self.widget.setAlignContent(Flexbox.ALIGN_CONTENT[alignment])

    def set_align_items(self, alignment):
        self.widget.setAlignItems(Flexbox.ALIGN_ITEMS[alignment])

    def set_flex_direction(self, direction):
        self.widget.setFlexDirection(Flexbox.FLEX_DIRECTION[direction])

    def set_flex_wrap(self, wrap):
        self.widget.setFlexWrap(Flexbox.FLEX_WRAP[wrap])

    def set_justify_content(self, justify):
        self.widget.setJustifyContent(Flexbox.JUSTIFY_CONTENT[justify])

    def create_layout_params(self, child, layout):
        params = super(AndroidFlexbox, self).create_layout_params(child,
                                                                  layout)
        dp = self.dp
        if 'align_self' in layout:
            params.setAlignSelf(Flexbox.ALIGN_SELF[layout['align_self']])
        if 'flex_basis' in layout:
            params.setFlexBasisPercent(layout['flex_basis'])
        if 'flex_grow' in layout:
            params.setFlexGrow(layout['flex_grow'])
        if 'flex_shrink' in layout:
            params.setFlexShrink(layout['flex_shrink'])
        if 'min_height' in layout:
            params.setMinHeight(int(layout['min_height']*dp))
        if 'max_height' in layout:
            params.setMinHeight(int(layout['max_height']*dp))
        if 'min_width' in layout:
            params.setMinWidth(int(layout['min_width']*dp))
        if 'max_width' in layout:
            params.setMaxWidth(int(layout['max_width']*dp))

        return params

    def apply_layout(self, child, layout):
        """ Apply the flexbox specific layout.
        
        """
        params = self.create_layout_params(child, layout)
        w = child.widget
        if w:
            # padding
            if layout.get('padding'):
                dp = self.dp
                l, t, r, b = layout['padding']
                w.setPadding(int(l*dp), int(t*dp),
                             int(b*dp), int(r*dp))
        child.layout_params = params