"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Apr 15, 2017

@author: jrm
"""
# flake8: noqa F401
import sys
from enaml.application import Application
from enaml.core.api import Conditional, Include, Looper
from .block import Block

if sys.platform == "darwin":
    pass  #: iOS
else:
    from enamlnative.android.http import AsyncHttpClient
