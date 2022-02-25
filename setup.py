"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 10, 2017

@author
"""
import re
import os
from setuptools import setup, find_packages
#from distutils.extension import Extension
#from Cython.Build import cythonize

extensions = []
# extensions = cythonize([
#     Extension("enamlnative.android.ndk",
#             ["enamlnative/android/*.pyx"],
#             libraries=["android"])
# ])


def find_version():
    with open(os.path.join('src', 'enamlnative', '__init__.py')) as f:
        for line in f:
            m = re.search(r'version = [\'"](.+)[\'"]', line)
            if m:
                return m.group(1)
    raise Exception("Couldn't find the version number")


setup(
    name="enaml-native",
    version=find_version(),
    author="CodeLV",
    author_email="info@codelv.com",
    license='MIT',
    url='https://codelv.com/projects/enaml-native/',
    description="Build native mobile apps in python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.9',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
