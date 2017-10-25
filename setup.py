'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 10, 2017

@author: jrm
'''
import os
import fnmatch
from setuptools import setup, find_packages


def find_data_files(dest, *folders):
    matches = {}
    excluded_types = ['.pyc', '.enamlc', '*.apk', '*.iml']
    excluded_dirs = ['android/build']
    for folder in folders:
        for dirpath, dirnames, files in os.walk(folder):
            #: Skip build folders and exclude hidden dirs
            if ([d for d in dirpath.split("/") if d.startswith(".")] or
                    [pattern for pattern in excluded_dirs if fnmatch.fnmatch(dirpath,pattern)]):
                continue
            k = os.path.join(dest,dirpath)
            if k not in matches:
                matches[k] = []
            for f in fnmatch.filter(files, '*'):
                if [p for p in excluded_types if f.endswith(p)]:
                    continue
                m = os.path.join(dirpath, f)
                matches[k].append(m)
    return matches.items()


setup(
    name="enaml-native-cli",
    version="1.0",
    author="frmdstryr",
    author_email="frmdstryr@gmail.com",
    license='MIT',
    url='https://github.com/frmdstryr/enaml-native/s',
    description="Build native mobile apps in python",
    scripts=['enaml-native'],
    long_description=open("README.md").read(),
    data_files=find_data_files('enaml-native-cli', 'android', 'docs', 'examples', 'ios',
                               'python-for-android', 'python-for-ios', 'tests', 'src'),
    install_requires=['atom', 'appdirs', 'colorama>=0.3.3', 'sh>=1.10,<1.12.5', 'jinja2',
                      'six', 'pipdeptree'],
    setup_requires=['virtualenv'],
    #: TODO: Automatically add enamlnative recipe to p4a
    # entry_points={
    #     'enaml_native_package': [
    #         'enaml_native = ',
    #     ],
    #     'p4a_recipe':[
    #         'enamlnative = '
    #     ]
    # },
)