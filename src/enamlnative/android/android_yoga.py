"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Nov 29, 2017

@author: jrm
"""
from atom.api import set_default
from .bridge import JavaBridgeObject, JavaMethod
from .android_view_group import ViewGroup, LayoutParams


class YogaNode(JavaBridgeObject):
    __nativeclass__ = set_default('com.facebook.yoga.YogaNode')
    reset = JavaMethod()
    addChildAt = JavaMethod('com.facebook.yoga.YogaNode', 'int')
    removeChildAt = JavaMethod('int', returns='com.facebook.yoga.YogaNode')
    calculateLayout = JavaMethod('float', 'float')
    markLayoutSeen = JavaMethod()
    copyStyle = JavaMethod('com.facebook.yoga.YogaNode')

    setDirection = JavaMethod('int')
    setFlexDirection = JavaMethod('int')
    setJustifyContent = JavaMethod('int')
    setAlignItems = JavaMethod('int')
    setAlignSelf = JavaMethod('int')
    setAlignContent = JavaMethod('int')
    setPositionType = JavaMethod('int')
    setWrap = JavaMethod('int')
    setOverflow = JavaMethod('int')
    setDisplay = JavaMethod('int')
    setFlex = JavaMethod('float')
    setFlexGrow = JavaMethod('float')
    setFlexShrink = JavaMethod('float')
    setFlexBasis = JavaMethod('float')
    setFlexBasisPercent = JavaMethod('float')
    setFlexBasisAuto = JavaMethod()
    setMargin = JavaMethod('int', 'float')
    setMarginPercent = JavaMethod('int', 'float')
    setMarginAuto = JavaMethod('int')
    setPadding = JavaMethod('int', 'float')
    setPaddingPercent = JavaMethod('int', 'float')
    setPaddingAuto = JavaMethod('int')
    setBorder = JavaMethod('int', 'float')
    setPosition = JavaMethod('int', 'float')
    setPositionPercent = JavaMethod('int', 'float')

    setWidth = JavaMethod('float')
    setWidthPercent = JavaMethod('float')
    setWidthAuto = JavaMethod()
    setHeight = JavaMethod('float')
    setHeightPercent = JavaMethod('float')
    setHeightAuto = JavaMethod()

    setMinWidth = JavaMethod('float')
    setMinWidthPercent = JavaMethod('float')
    setMinHeight = JavaMethod('float')
    setMinHeightPercent = JavaMethod('float')

    setMaxWidth = JavaMethod('float')
    setMaxWidthPercent = JavaMethod('float')
    setMaxHeight = JavaMethod('float')
    setMaxHeightPercent = JavaMethod('float')

    setAspectRatio = JavaMethod('float')



class YogaLayoutParams(LayoutParams):
    __nativeclass__ = set_default('com.facebook.yoga.YogaLayout$LayoutParams')


class YogaLayout(ViewGroup):
    __nativeclass__ = set_default('com.facebook.yoga.android.YogaLayout')
