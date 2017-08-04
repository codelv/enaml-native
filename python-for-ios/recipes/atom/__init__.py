import sh
from os.path import join, exists
import os
from glob import glob
from toolchain import CppPythonRecipe, FrameworkLibrary, shprint, current_directory


class AtomFramework(FrameworkLibrary):
    #: TODO: Would be nice if this was automatic!
    #: Collect all so files
    libraries = ['python/{arch}/atom.*.dylib']

    #: Collect all py files architecture
    resources = []


class AtomRecipe(CppPythonRecipe):
    site_packages_name = 'atom'
    version = '0.3.10'
    url = 'https://github.com/nucleic/atom/archive/master.zip'
    depends = ['python', 'host_setuptools']
    framework = AtomFramework()


recipe = AtomRecipe()
