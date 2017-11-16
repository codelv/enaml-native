"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 10, 2017

@author: jrm
"""

import sys
from setuptools import setup, find_packages

setup(
    name="enaml-native",
    version="2.11.6",
    author="CodeLV",
    author_email="frmdstryr@gmail.com",
    license='MIT',
    url='https://github.com/codelv/enaml-native/',
    description="Build native mobile apps in python",
    long_description=open("README.md").read(),
    packages=find_packages(),
    install_requires=['enaml', 'msgpack-python'],
)