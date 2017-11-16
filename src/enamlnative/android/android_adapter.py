"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from .android_view_group import AndroidViewGroup, ViewGroup
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class ArrayAdapter(JavaBridgeObject):
    __nativeclass__ = set_default('android.widget.ArrayAdapter')
    __signature__ = set_default(('android.content.Context', 'android.R'))
    add = JavaMethod('java.lang.Object')
    addAll = JavaMethod('[Ljava.lang.Object;')
    remove = JavaMethod('java.lang.Object')
    clear = JavaMethod()


class AdapterView(ViewGroup):
    __nativeclass__ = set_default('android.widget.AdapterView')
    setEmptyView = JavaMethod('android.view.View')
    setFocusableInTouchMode = JavaMethod('boolean')
    setOnItemClickListener = JavaMethod(
        'android.widget.AdapterView$OnItemClickListener')
    setOnItemLongClickListener = JavaMethod(
        'android.widget.AdapterView$OnItemLongClickListener')
    setOnItemSelectedListener = JavaMethod(
        'android.widget.AdapterView$OnItemSelectedListener')
    setSelection = JavaMethod('int')

    onItemClick = JavaMethod('android.widget.AdapterView',
                             'android.view.View', 'int', 'long')
    onItemLongClick = JavaMethod('android.widget.AdapterView',
                                 'android.view.View', 'int', 'long')
    onItemSelected = JavaCallback('android.widget.AdapterView',
                                  'android.view.View', 'int', 'long')
    onNothingSelected = JavaCallback('android.widget.AdapterView')


class AndroidAdapterView(AndroidViewGroup):

    #: Adapter reference
    adapter = Typed(ArrayAdapter)

    def destroy(self):
        """ Destroy the adapter """
        super(AndroidAdapterView, self).destroy()
        if self.adapter:
            del self.adapter

