
from pythonforandroid.toolchain import Recipe, shprint, current_directory, info, warning
from os.path import join, exists
from os import chdir
import sh


class Hostpython2Recipe(Recipe):
    version = '2.7'
    # url = 'http://python.org/ftp/python/{version}/Python-{version}.tgz'
    # url = 'https://github.com/crystax/android-vendor-python-3-5/archive/master.zip'
    name = 'hostpython2crystax'

    conflicts = ['hostpython3','hostpython2','hostpython3crystax']

    # def prebuild_armeabi(self):
    #     # Override hostpython Setup?
    #     shprint(sh.cp, join(self.get_recipe_dir(), 'Setup'),
    #             join(self.get_build_dir('armeabi'), 'Modules', 'Setup'))

    def build_arch(self, arch):
        self.ctx.hostpython = '/usr/bin/false'
        self.ctx.hostpgen = '/usr/bin/false'


recipe = Hostpython2Recipe()
