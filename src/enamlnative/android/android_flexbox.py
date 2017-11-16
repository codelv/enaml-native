"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Atom, Typed, set_default

from enaml.widgets.toolkit_object import ProxyToolkitObject
from enamlnative.widgets.flexbox import ProxyFlexbox
from enamlnative.core.layout import FlexParams

from .android_view_group import AndroidViewGroup, ViewGroup, MarginLayoutParams
from .bridge import JavaMethod, JavaField


class Flexbox(ViewGroup):
    #__nativeclass__ = set_default('com.facebook.yoga.android.YogaLayout')
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


class FlexboxLayoutHelper(Atom):

    layout = Typed(FlexParams)
    layout_params = Typed(FlexboxLayoutParams)

    @staticmethod
    def apply_layout(proxy):
        if proxy.layout_params and isinstance(proxy.layout_params, FlexboxLayoutParams):
            d = proxy.declaration
            #: Create the helper
            helper = FlexboxLayoutHelper(
                layout=FlexParams(**d.layout),
                layout_params=proxy.layout_params
            )

            #: Do the layout
            helper.init_layout()

    def init_layout(self):
        d = self.layout
        #: TODO...
        if d.align_self != 'auto':
            self.set_align_self(d.align_self)
        if d.flex_basis:
            self.set_flex_basis(d.flex_basis)
        if d.flex_grow:
            self.set_flex_grow(d.flex_grow)
        if d.flex_shrink:
            self.set_flex_shrink(d.flex_shrink)
        if d.min_height:
            self.set_min_height(d.min_height)
        if d.max_height:
            self.set_max_height(d.max_height)
        if d.min_width:
            self.set_min_width(d.min_width)
        if d.max_width:
            self.set_max_width(d.max_width)

    def set_align_self(self, alignment):
        self.layout_params.setAlignSelf(Flexbox.ALIGN_SELF[alignment])

    def set_flex_grow(self, grow):
        self.layout_params.setFlexGrow(grow)

    def set_flex_shrink(self, shrink):
        self.layout_params.setFlexShrink(shrink)

    def set_flex_basis(self, basis):
        self.layout_params.setFlexBasisPercent(basis)

    def set_left(self, left):
        pass

    def set_top(self, top):
        pass

    def set_bottom(self, bottom):
        pass

    def set_right(self, right):
        pass

    def set_start(self, start):
        pass

    def set_end(self, end):
        pass

    def set_min_height(self, height):
        self.layout_params.setMinHeight(height)

    def set_max_height(self, height):
        self.layout_params.setMaxHeight(height)

    def set_min_width(self, width):
        self.layout_params.setMinWidth(width)

    def set_max_width(self, width):
        self.layout_params.setMaxWidth(width)

    def set_margin_left(self, left):
        #self.update_layout_params()
        pass

    def set_margin_top(self, top):
        #self.update_layout_params()
        pass

    def set_margin_bottom(self, bottom):
        #self.update_layout_params()
        pass

    def set_margin_right(self, right):
        #self.update_layout_params()
        pass

    def set_margin_start(self, start):
        #self.update_layout_params()
        pass

    def set_margin_end(self, end):
        #self.update_layout_params()
        pass

    def set_margin(self, margin):
        #self.update_layout_params()
        pass

    def set_padding_left(self, left):
        #self.update_layout_params()
        pass

    def set_padding_top(self, top):
        #self.update_layout_params()
        pass

    def set_padding_bottom(self, bottom):
        #self.update_layout_params()
        pass

    def set_padding_right(self, right):
        #self.update_layout_params()
        pass

    def set_padding_start(self, start):
        #self.update_layout_params()
        pass

    def set_padding_end(self, end):
        #self.update_layout_params()
        pass

    def set_padding(self, padding):
        #self.update_layout_params()
        pass

    def set_border_left(self, left):
        #self.update_layout_params()
        pass

    def set_border_top(self, top):
        #self.update_layout_params()
        pass

    def set_border_bottom(self, bottom):
        #self.update_layout_params()
        pass

    def set_border_right(self, right):
        #self.update_layout_params()
        pass

    def set_border_start(self, start):
        #self.update_layout_params()
        pass

    def set_border_end(self, end):
        #self.update_layout_params()
        pass

    def set_border(self, border):
        #self.update_layout_params()
        pass


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

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidFlexbox, self).init_widget()
        d = self.declaration
        if d.flex_direction != 'row':
            self.set_flex_direction(d.flex_direction)
        if d.flex_wrap != 'nowrap':
            self.set_flex_wrap(d.flex_wrap)
        if d.justify_content != 'flex_start':
            self.set_justify_content(d.justify_content)
        if d.align_items != 'stretch':
            self.set_align_items(d.align_items)
        if d.align_content != 'stretch':
            self.set_align_content(d.align_content)

        #: Dividers??

        #: Update all children to use FlexboxLayoutParams
        for c in self.children():
            if hasattr(c,'layout_param_type'):
                c.layout_param_type = FlexboxLayoutParams


    # def init_layout(self):
    #     """ Init flexbox params of children """
    #     super(AndroidFlexbox, self).init_layout()
    #
    #     for c in self.children():
    #         if isinstance(c.layout_params,FlexboxLayoutParams):
    #             FlexboxLayoutMixin.apply_layout(c)
    #
    #     FlexboxLayoutMixin.apply_layout(self)
    #
    # def init_layout(self):
    #     """ Add all child widgets to the view
    #     """
    #     widget = self.widget
    #     for i, child_widget in enumerate(self.child_widgets()):
    #         widget.addView(child_widget, i, )
    #
    # def child_added(self, child):
    #     """ Handle the child added event from the declaration.
    #
    #     This handler will unparent the child toolkit widget. Subclasses
    #     which need more control should reimplement this method.
    #
    #     """
    #     super(AndroidViewGroup, self).child_added(child)
    #
    #     widget = self.widget
    #     #: TODO: Should index be cached?
    #     for i, child_widget in enumerate(self.child_widgets()):
    #         if child_widget == child.widget:
    #             widget.addView(child_widget, i)

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
