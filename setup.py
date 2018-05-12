"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 10, 2017

@author
"""
from setuptools import setup, find_packages
#from distutils.extension import Extension
#from Cython.Build import cythonize

extensions = []
# extensions = cythonize([
#     Extension("enamlnative.android.ndk",
#             ["enamlnative/android/*.pyx"],
#             libraries=["android"])
# ])


setup(
    name="enaml-native",
    version="4.5.1",
    author="CodeLV",
    author_email="frmdstryr@gmail.com",
    license='MIT',
    url='https://github.com/codelv/enaml-native/',
    description="Build native mobile apps in python",
    long_description=open("README.md").read(),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    ext_modules=extensions
)
