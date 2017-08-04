'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 24, 2017

@author: jrm
'''

from atom.api import Atom, Int, set_default
from .bridge import JavaBridgeObject, JavaMethod


class Activity(JavaBridgeObject):
    """ Access to the activity over the bridge """
    __nativeclass__ = set_default('com.enaml.MainActivity')
    __id__ = Int(-1) #: ID of -1 is a special reference on the bridge to the activity.

    setView = JavaMethod('android.view.View')
    showLoading = JavaMethod('java.lang.String')
    setActionBar = JavaMethod('android.widget.Toolbar')
    setSupportActionBar = JavaMethod('android.support.v7.widget.Toolbar')
    setContentView = JavaMethod('android.view.View')
    getWindow = JavaMethod(returns='android.view.Window')
