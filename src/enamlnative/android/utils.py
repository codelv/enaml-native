'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 28, 2017

@author: jrm
'''
import re
import os
from glob import glob


def find_all_javaclasses(path=None, exts=['*.py','*.enaml']):
    """
        Attempts to find all the usage of autoclass in the given directory and
        filetypes. Return a list of java classes required (ie uses of autoclass).
        
        Example:
        
        ['android.app.Activity',
         'android.os.SystemClock',
         'android.support.v4.view.GravityCompat',
         'android.support.v4.view.ViewCompat',
         'android.support.v4.widget.DrawerLayout',
         'android.support.v4.widget.DrawerLayout$LayoutParams',
         # ... you get the idea
         'java.lang.Boolean']

    
        Meant to be passed to jnius.reflect.build_cache()
    """
    path = path or os.path.dirname(__file__)
    
    sources = []
    for ext in exts:
        sources.extend(glob(os.path.join(path,ext)))
    
    clsnames = []
    for filename in sources:
        with open(filename) as f:
            src = f.read()
            clsnames.extend(re.findall(r'autoclass\(\s*[\'"](.+)[\'"]\s*\)',src))
            
    return sorted(list(set(clsnames)))
    
def build_cache():
    from jnius import reflect
    if not hasattr(reflect,'build_cache'):
        raise RuntimeError("Using wrong version of jnius if you want caching to work!")
    reflect.build_cache(find_all_javaclasses())
    




