"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 30, 2017

@author
"""
from pythonforandroid.recipe import EnamlNativeRecipe


class EnamlNativeCoreRecipe(EnamlNativeRecipe):
    version = '1.0'
    depends = [('python2', 'python2crystax'), 'enaml', 'msgpack-python']
    name = 'enaml-native'
    url = 'src.zip'


def get_recipe():
    return (EnamlNativeCoreRecipe(), __file__)
