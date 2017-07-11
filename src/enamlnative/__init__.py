'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import sys
from contextlib import contextmanager

@contextmanager
def imports():
    """ Import so files from android lib folder """
    from .android.import_hooks import AndroidFinder
    finder = AndroidFinder()
    sys.meta_path.append(finder)
    yield
    sys.meta_path.remove(finder)