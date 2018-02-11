"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""
from .bridge import NestedBridgeObject, ObjcMethod, ObjcProperty


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
