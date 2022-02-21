"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed
from .android_content import Context
from .android_view import View
from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaBridgeObject, JavaCallback, JavaMethod


class ArrayAdapter(JavaBridgeObject):
    __nativeclass__ = "android.widget.ArrayAdapter"
    __signature__ = [Context, "android.R"]
    add = JavaMethod("java.lang.Object")
    addAll = JavaMethod("[Ljava.lang.Object;")
    remove = JavaMethod("java.lang.Object")
    clear = JavaMethod()


class AdapterView(ViewGroup):
    __nativeclass__ = "android.widget.AdapterView"
    setEmptyView = JavaMethod(View)
    setFocusableInTouchMode = JavaMethod(bool)
    setOnItemClickListener = JavaMethod(
        "android.widget.AdapterView$OnItemClickListener"
    )
    setOnItemLongClickListener = JavaMethod(
        "android.widget.AdapterView$OnItemLongClickListener"
    )
    setOnItemSelectedListener = JavaMethod(
        "android.widget.AdapterView$OnItemSelectedListener"
    )
    setSelection = JavaMethod(int)

    onItemClick = JavaCallback("android.widget.AdapterView", View, int, "long")
    onItemLongClick = JavaCallback("android.widget.AdapterView", View, int, "long")
    onItemSelected = JavaCallback("android.widget.AdapterView", View, int, "long")
    onNothingSelected = JavaCallback("android.widget.AdapterView")


class AndroidAdapterView(AndroidViewGroup):

    #: Adapter reference
    adapter = Typed(ArrayAdapter)
