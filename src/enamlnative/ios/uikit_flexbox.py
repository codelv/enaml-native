"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""

from atom.api import Atom, Typed, Instance, set_default
from enamlnative.core.layout import FlexParams
from enamlnative.widgets.flexbox import ProxyFlexbox

from .bridge import NestedBridgeObject, ObjcMethod, ObjcProperty
from .uikit_view import UIView, UiKitView


class Yoga(NestedBridgeObject):
    isEnabled = ObjcProperty('bool')

    flexDirection = ObjcProperty('YGFlexDirection')
    justifyContent = ObjcProperty('YGJustify')
    alignContent = ObjcProperty('YGAlign')
    alignItems = ObjcProperty('YGAlign')
    alignSelf = ObjcProperty('YGAlign')
    overflow = ObjcProperty('YGOverflow')
    display = ObjcProperty('YGDisplay')

    flexWrap = ObjcProperty('YGWrap')
    flexGrow = ObjcProperty('CGFloat')
    flexShrink = ObjcProperty('CGFloat')
    flexBasis = ObjcProperty('YGValue')

    left = ObjcProperty('YGValue')
    top = ObjcProperty('YGValue')
    right = ObjcProperty('YGValue')
    bottom = ObjcProperty('YGValue')
    start = ObjcProperty('YGValue')
    end = ObjcProperty('YGValue')

    marginLeft = ObjcProperty('YGValue')
    marginTop = ObjcProperty('YGValue')
    marginRight = ObjcProperty('YGValue')
    marginBottom = ObjcProperty('YGValue')
    marginStart = ObjcProperty('YGValue')
    marginEnd = ObjcProperty('YGValue')
    margin = ObjcProperty('YGValue')

    paddingLeft = ObjcProperty('YGValue')
    paddingTop = ObjcProperty('YGValue')
    paddingRight = ObjcProperty('YGValue')
    paddingBottom = ObjcProperty('YGValue')
    paddingStart = ObjcProperty('YGValue')
    paddingEnd = ObjcProperty('YGValue')
    padding = ObjcProperty('YGValue')
    
    borderLeftWidth = ObjcProperty('YGValue')
    borderTopWidth = ObjcProperty('YGValue')
    borderRightWidth = ObjcProperty('YGValue')
    borderBottomWidth = ObjcProperty('YGValue')
    borderStartWidth = ObjcProperty('YGValue')
    borderEndWidth = ObjcProperty('YGValue')
    borderWidth = ObjcProperty('YGValue')

    width = ObjcProperty('YGValue')
    height = ObjcProperty('YGValue')
    minWidth = ObjcProperty('YGValue')
    maxWidth = ObjcProperty('YGValue')
    minHeight = ObjcProperty('YGValue')
    maxHeight = ObjcProperty('YGValue')

    markDirty = ObjcMethod()

    applyLayoutPreservingOrigin = ObjcMethod('bool')

    YGAlignAuto = 0
    YGAlignFlexStart = 1
    YGAlignCenter = 2
    YGAlignFlexEnd = 3
    YGAlignStretch = 4
    YGAlignBaseline = 5
    YGAlignSpaceBetween = 6
    YGAlignSpaceAround = 7


    YGDirectionInherit = 0
    YGDirectionLTR = 1
    YGDirectionRTL = 2

    YGDisplayFlex = 0
    YGDisplayNone = 1

    YGFlexDirectionColumn = 0
    YGFlexDirectionColumnReverse = 1
    YGFlexDirectionRow = 2
    YGFlexDirectionRowReverse = 3

    YGJustifyFlexStart = 0
    YGJustifyCenter = 1
    YGJustifyFlexEnd = 2
    YGJustifySpaceBetween = 3
    YGJustifySpaceAround = 4

    YGOverflowVisible = 0
    YGOverflowHidden = 1
    YGOverflowScroll = 2

    YGWrapNoWrap = 0
    YGWrapWrap = 1
    YGWrapWrapReverse = 2

    FLEX_DIRECTION = {
        'row': YGFlexDirectionRow,
        'row_reverse': YGFlexDirectionRowReverse,
        'column': YGFlexDirectionColumn,
        'column_reverse': YGFlexDirectionColumnReverse
    }

    FLEX_WRAP = {
        'nowrap': YGWrapNoWrap,
        'wrap': YGWrapWrap,
        'wrap_reverse': YGWrapWrapReverse,
    }

    JUSTIFY_CONTENT = {
        'flex_start': YGJustifyFlexStart,
        'flex_end': YGJustifyFlexEnd,
        'center': YGJustifyCenter,
        'space_between': YGJustifySpaceBetween,
        'space_around': YGJustifySpaceAround
    }

    ALIGN_ITEMS = {
        'flex_start': YGAlignFlexStart,
        'flex_end': YGAlignFlexEnd,
        'center': YGAlignCenter,
        'baseline': YGAlignBaseline,
        'stretch': YGAlignStretch
    }

    ALIGN_CONTENT = {
        'flex_start': YGAlignFlexStart,
        'flex_end': YGAlignFlexEnd,
        'center': YGAlignCenter,
        'space_between': YGAlignSpaceBetween,
        'space_around': YGAlignSpaceAround,
        'stretch': YGAlignStretch,
    }

    ALIGN_SELF = {
        'auto':YGAlignAuto,
        'flex_start': YGAlignFlexStart,
        'flex_end': YGAlignFlexEnd,
        'center': YGAlignCenter,
        'baseline': YGAlignBaseline,
        'stretch': YGAlignStretch
    }


class FlexboxLayoutHelper(Atom):

    layout = Typed(FlexParams)
    yoga = Instance(Yoga)

    @staticmethod
    def apply_layout(proxy):
        d = proxy.declaration
        #: Create the helper
        helper = FlexboxLayoutHelper(
            layout=FlexParams(**d.layout),
            yoga=proxy.widget.yoga,
        )

        #: Do the layout
        helper.init_layout()

    def init_layout(self):
        d = self.layout
        #: TODO...
        self.yoga.isEnabled = True
        
        if d.align_self != 'auto':
            self.set_align_self(d.align_self)
        if d.flex_basis:
            self.set_flex_basis(d.flex_basis)
        if d.flex_grow:
            self.set_flex_grow(d.flex_grow)
        if d.flex_shrink:
            self.set_flex_shrink(d.flex_shrink)

        if d.top:
            self.set_top(d.top)
        if d.left:
            self.set_left(d.left)
        if d.right:
            self.set_right(d.right)
        if d.bottom:
            self.set_bottom(d.bottom)
        if d.start:
            self.set_start(d.start)
        if d.end:
            self.set_end(d.end)


        if d.min_height:
            self.set_min_height(d.min_height)
        if d.max_height:
            self.set_max_height(d.max_height)
        if d.min_width:
            self.set_min_width(d.min_width)
        if d.max_width:
            self.set_max_width(d.max_width)
            
        #: TODO: this only sets if not 0!
        if d.margin:
            self.set_margin(d.margin)
        if d.margin_top:
            self.set_margin_top(d.margin_top)
        if d.margin_left:
            self.set_margin_left(d.margin_left)
        if d.margin_right:
            self.set_margin_right(d.margin_right)
        if d.margin_bottom:
            self.set_margin_bottom(d.margin_bottom)
        if d.margin_start:
            self.set_margin_start(d.margin_start)
        if d.margin_end:
            self.set_margin_end(d.margin_end)
            
        if d.padding:
            self.set_padding(d.padding)
        if d.padding_top:
            self.set_padding_top(d.padding_top)
        if d.padding_left:
            self.set_padding_left(d.padding_left)
        if d.padding_right:
            self.set_padding_right(d.padding_right)
        if d.padding_bottom:
            self.set_padding_bottom(d.padding_bottom)
        if d.padding_start:
            self.set_padding_start(d.padding_start)
        if d.padding_end:
            self.set_padding_end(d.padding_end)

    def set_align_self(self, alignment):
        self.yoga.alignSelf = Yoga.ALIGN_SELF[alignment]

    def set_flex_grow(self, grow):
        self.yoga.flexGrow = grow

    def set_flex_shrink(self, shrink):
        self.yoga.flexShrink = shrink

    def set_flex_basis(self, basis):
        self.yoga.flexBasis = basis

    def set_left(self, left):
        self.yoga.left = left

    def set_top(self, top):
        self.yoga.top = top

    def set_bottom(self, bottom):
        self.yoga.bottom = bottom

    def set_right(self, right):
        self.yoga.right = right

    def set_start(self, start):
        self.yoga.start = start

    def set_end(self, end):
        self.yoga.end = end

    def set_min_height(self, height):
        self.yoga.minHeight = height

    def set_max_height(self, height):
        self.yoga.maxHeight = height

    def set_min_width(self, width):
        self.yoga.minWidth = width

    def set_max_width(self, width):
        self.yoga.maxWidth = width

    def set_margin_left(self, left):
        self.yoga.marginLeft = left

    def set_margin_top(self, top):
        self.yoga.marginTop = top

    def set_margin_bottom(self, bottom):
        self.yoga.marginBottom = bottom

    def set_margin_right(self, right):
        self.yoga.marginRight = right

    def set_margin_start(self, start):
        self.yoga.marginStart = start

    def set_margin_end(self, end):
        self.yoga.marginEnd = end

    def set_margin(self, margin):
        self.yoga.margin = margin

    def set_padding_left(self, left):
        self.yoga.paddingLeft = left

    def set_padding_top(self, top):
        self.yoga.paddingTop = top

    def set_padding_bottom(self, bottom):
        self.yoga.paddingBottom = bottom

    def set_padding_right(self, right):
        self.yoga.paddingRight = right

    def set_padding_start(self, start):
        self.yoga.paddingStart = start

    def set_padding_end(self, end):
        self.yoga.paddingEnd = end

    def set_padding(self, padding):
        self.yoga.padding = padding

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
    

class UIFlexbox(UIView):
    """ Adds yoga as a nested object
    """
    __nativeclass__ = set_default("UIView")


class UiKitFlexbox(UiKitView, ProxyFlexbox):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit layout created by the proxy.
    widget = Typed(UIFlexbox)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        self.widget = UIFlexbox()

    def init_layout(self):
        """ Init layout using yoga """
        super(UiKitFlexbox, self).init_layout()

        d = self.declaration

        self.widget.yoga.isEnabled = True
        if d.width or d.height:
            yoga = self.widget.yoga
            yoga.width = float(d.width)
            yoga.height = float(d.height)

        #if d.layout_width == "match_parent" or d.layout_height == "match_parent":
        #    self.set_flex_grow(1)

        if d.flex_direction != 'column': # Default is column
            self.set_flex_direction(d.flex_direction)
        if d.flex_wrap != 'nowrap':
            self.set_flex_wrap(d.flex_wrap)
        if d.justify_content != 'flex_start':
            self.set_justify_content(d.justify_content)
        if d.align_items != 'stretch':
            self.set_align_items(d.align_items)
        if d.align_content != 'stretch':
            self.set_align_content(d.align_content)

        #: Enable for all children
        for w in self.child_widgets():
            #: Yoga is always required I gues...
            w.yoga.isEnabled = True

        #self.apply_layout()

    def apply_layout(self):
        #: Invoke it, TODO: This should only be done on the ROOT flex element!
        if self.parent() is None:
            self.widget.yoga.applyLayoutPreservingOrigin(True)

    # -------------------------------------------------------------------------
    # ProxyFlexbox API
    # -------------------------------------------------------------------------
    def set_align_content(self, alignment):
        self.widget.yoga.alignContent = Yoga.ALIGN_CONTENT[alignment]

    def set_align_items(self, alignment):
        self.widget.yoga.alignItems = Yoga.ALIGN_ITEMS[alignment]

    def set_align_self(self, alignment):
        self.widget.yoga.alignSelf = Yoga.ALIGN_SELF[alignment]

    def set_flex_direction(self, direction):
        self.widget.yoga.flexDirection = Yoga.FLEX_DIRECTION[direction]

    def set_flex_grow(self, grow):
        self.widget.yoga.flexGrow = grow

    def set_flex_shrink(self, shrink):
        self.widget.yoga.flexShrink = shrink

    def set_flex_basis(self, basis):
        self.widget.yoga.flexBasis = int(basis*100)

    def set_flex_wrap(self, wrap):
        self.widget.flexWrap = Yoga.FLEX_WRAP[wrap]

    def set_left(self, left):
        raise NotImplementedError

    def set_top(self, top):
        raise NotImplementedError

    def set_bottom(self, bottom):
        raise NotImplementedError

    def set_right(self, right):
        raise NotImplementedError

    def set_start(self, start):
        raise NotImplementedError

    def set_end(self, end):
        raise NotImplementedError

    def set_justify_content(self, justify):
        self.widget.yoga.justifyContent = Yoga.JUSTIFY_CONTENT[justify]

    def set_min_height(self, height):
        raise NotImplementedError

    def set_max_height(self, height):
        raise NotImplementedError

    def set_min_width(self, width):
        raise NotImplementedError

    def set_max_width(self, width):
        raise NotImplementedError

    def set_margin_left(self, left):
        raise NotImplementedError

    def set_margin_top(self, top):
        raise NotImplementedError

    def set_margin_bottom(self, bottom):
        raise NotImplementedError

    def set_margin_right(self, right):
        raise NotImplementedError

    def set_margin_start(self, start):
        raise NotImplementedError

    def set_margin_end(self, end):
        raise NotImplementedError

    def set_margin(self, margin):
        raise NotImplementedError

    def set_padding_left(self, left):
        raise NotImplementedError

    def set_padding_top(self, top):
        raise NotImplementedError

    def set_padding_bottom(self, bottom):
        raise NotImplementedError

    def set_padding_right(self, right):
        raise NotImplementedError

    def set_padding_start(self, start):
        raise NotImplementedError

    def set_padding_end(self, end):
        raise NotImplementedError

    def set_padding(self, padding):
        raise NotImplementedError

    def set_border_left(self, left):
        raise NotImplementedError

    def set_border_top(self, top):
        raise NotImplementedError

    def set_border_bottom(self, bottom):
        raise NotImplementedError

    def set_border_right(self, right):
        raise NotImplementedError

    def set_border_start(self, start):
        raise NotImplementedError

    def set_border_end(self, end):
        raise NotImplementedError

    def set_border(self, border):
        raise NotImplementedError
