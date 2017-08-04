import sh
from os.path import join, exists
import os
from toolchain import CppPythonRecipe, FrameworkLibrary, shprint, current_directory


class EnamlFramework(FrameworkLibrary):

    libraries = ['python/{arch}/enaml.*.dylib']

class EnamlRecipe(CppPythonRecipe):
    site_packages_name = 'enaml'
    version = '0.9.8'
    url = 'https://github.com/frmdstryr/enaml/archive/master.zip'
    patches = ['0001-Update-setup.py.patch'] # Remove PyQt dependency
    depends = ['atom']
    framework = EnamlFramework()



recipe = EnamlRecipe()
