"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 10, 2017

@author
"""
import os
import fnmatch
from setuptools import setup


def find_data_files(dest, *folders):
    matches = {}
    #: Want to install outside the venv volder in the packages folder
    dest = os.path.join('packages', dest)

    excluded_types = ['.pyc', '.enamlc', '.apk', '.iml', '.tar.gz',
                      '.so', '.gif', '.svg', 'local.properties']
    excluded_dirs = ['android/build', 'android/captures', 'android/assets',
                     'docs/imgs']
    for folder in folders:
        if not os.path.isdir(folder):
            k = os.path.join(dest, dirpath)
            matches[k].append(os.path.join(dest, folder))
            continue
        for dirpath, dirnames, files in os.walk(folder):
            #: Skip build folders and exclude hidden dirs
            if ([d for d in dirpath.split("/") if d.startswith(".")] or
                    [excluded_dir for excluded_dir in excluded_dirs
                        if excluded_dir in dirpath]):
                continue
            k = os.path.join(dest, dirpath)
            if k not in matches:
                matches[k] = []
            for f in fnmatch.filter(files, '*'):
                if [p for p in excluded_types if f.endswith(p)]:
                    continue
                m = os.path.join(dirpath, f)
                matches[k].append(m)
    return matches.items()


setup(
    name="enaml-native",
    version="4.4.2",
    author="CodeLV",
    author_email="frmdstryr@gmail.com",
    license='MIT',
    url='https://github.com/codelv/enaml-native/',
    description="Build native mobile apps in python",
    long_description=open("README.md").read(),
    data_files=find_data_files("enaml-native", 'android', 'ios', 'src',
                               'tests', 'docs', 'examples'),
)
