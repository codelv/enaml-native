"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Apr 15, 2017

@author: jrm
"""
import sys
from .block import Block
from enaml.core.api import *

if sys.platform == 'darwin':
    pass  #: iOS
else:
    from enamlnative.android.http import AsyncHttpClient