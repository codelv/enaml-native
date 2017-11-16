"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import set_default
from .bridge import JavaMethod, JavaBridgeObject


class ArrayList(JavaBridgeObject):
    __nativeclass__ = set_default('java.util.ArrayList')
    add = JavaMethod('int', 'java.lang.Object')
    addAll = JavaMethod('java.util.Collection')
    remove = JavaMethod('int')
    removeAll = JavaMethod('java.util.Collection')
    clear = JavaMethod()