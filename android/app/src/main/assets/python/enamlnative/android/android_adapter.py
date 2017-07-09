'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import set_default

from .bridge import JavaBridgeObject, JavaMethod


class ArrayAdapter(JavaBridgeObject):
    __javaclass__ = set_default('android.widget.ArrayAdapter')
    __signature__ = set_default(('android.content.Context', 'android.R'))
    add = JavaMethod('java.lang.Object')
    addAll = JavaMethod('[Ljava.lang.Object;')
    remove = JavaMethod('java.lang.Object')
    clear = JavaMethod()


