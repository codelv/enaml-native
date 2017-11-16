"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 24, 2017

@author: jrm
"""

from atom.api import set_default
from .bridge import JavaBridgeObject, JavaMethod


class Window(JavaBridgeObject):
    """ Access to the activity over the bridge """
    __nativeclass__ = set_default('android.view.Window')

    #: https://developer.android.com/reference/android/
    # view/WindowManager.LayoutParams.html#FLAG_KEEP_SCREEN_ON
    FLAG_KEEP_SCREEN_ON = 128

    addFlags = JavaMethod('int')
    clearFlags = JavaMethod('int')
