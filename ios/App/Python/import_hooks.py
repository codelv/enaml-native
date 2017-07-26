'''
Copyright (c) 2017, Jairus Martin.
Distributed under the terms of the MIT License.
The full license is in the file COPYING.txt, distributed with this software.
Created on July 10, 2017
@author: jrm
'''
import sys
import imp
from glob import glob
from os.path import dirname, join

class SoLoader(object):
    """ Loads renamed so files from the app's lib folder"""
    so_modules = {}

    def load_module(self, mod):
        try:
            return sys.modules[mod]
        except KeyError:
            pass

        lib = SoLoader.so_modules[mod]
        m = imp.load_dynamic(mod, lib)
        #m.__file__ = mod
        #m.__path__ = []
        #m.__loader__ = self
        sys.modules[mod] = m
        return m

    def __init__(self, path=None):
        #: Find all included so files
        lib_dir = join(dirname(sys.path[0]),'Lib')#path or os.environ['APK_LIB_DIR']
        print("Loading libs from %s"%lib_dir)
        print("Contents: {}".format(glob('%s/*'%lib_dir)))
        for lib in glob('%s/*.so'%lib_dir):

            name = lib.split("/")[-1] # Lib filename
            mod = ".".join(name.split(".")[:-1])  # Strip so
            SoLoader.so_modules[mod] = lib
            #print(AndroidFinder.so_modules)

    def find_module(self, mod, path = None):
        if mod in self.so_modules:
            return self
        return None
