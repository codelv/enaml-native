'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 3, 2017

@author: jrm
'''
import os
import enaml
import pytest
from app import MockApplication
from utils import load

def test_serialization():
    app = MockApplication.instance() or MockApplication()

    with enaml.imports():
        ContentView = load("""
        from enamlnative.core.api import *
        from enamlnative.widgets.api import *

        enamldef ContentView(Flexbox):
            Looper:
                iterable = range(1000)
                TextView:
                    padding = (10, 10, 10, 10)
                    text = "hello"
                    text_size = 32
                    font_family = "sans-serif"

        """)

    app.view = ContentView()
    app.run()






