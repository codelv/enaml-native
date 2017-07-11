'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 10, 2017

@author: jrm
'''
import os
import sys
import imp
from glob import glob


class AndroidLoader(object):
    """ Loads renamed .so files from the app's lib folder"""

    def load_module(self, mod):
        try:
            return sys.modules[mod]
        except KeyError:
            pass

        lib = AndroidFinder.so_modules[mod]
        m = imp.load_dynamic(mod, lib)
        #m.__file__ = mod
        #m.__path__ = []
        #m.__loader__ = self
        sys.modules[mod] = m
        return m


class AndroidFinder(object):
    """ Loads renamed so files from the app's lib folder"""
    so_modules = {}

    def __init__(self):
        #: Find all included so files
        lib_dir = os.environ['APK_LIB_DIR']
        #print("Loading libs from %s"%lib_dir)
        for lib in glob('%s/lib.*.so'%lib_dir):
            name = lib.split("/")[-1] # Lib filename
            mod = ".".join(name.split(".")[1:-1])  # Strip lib and so
            AndroidFinder.so_modules[mod] = lib
        #print(AndroidFinder.so_modules)

    def find_module(self, mod, path = None):
        if mod in self.so_modules:
            return AndroidLoader()
        return None

