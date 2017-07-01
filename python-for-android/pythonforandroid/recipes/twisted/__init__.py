
import glob
from pythonforandroid.toolchain import (
    CythonRecipe,
    Recipe,
    current_directory,
    info,
    shprint,
)
from os.path import join
import sh


class TwistedRecipe(CythonRecipe):
    version = '17.5.0'
    url = 'https://github.com/twisted/twisted/archive/twisted-{version}.tar.gz'

    depends = [ 'zope_interface']
    call_hostpython_via_targetpython = False

    def prebuild_arch(self, arch):
        super(TwistedRecipe, self).prebuild_arch(arch)
        # TODO Need to whitelist tty.pyo and termios.so here
        with current_directory(self.get_build_dir(arch.arch)):
            sh.rm('-rf', glob.glob('src/twisted/*/test'))
            sh.rm('-f',glob.glob('src/twisted/test/*.py'))

    def get_recipe_env(self, arch):
        env = super(TwistedRecipe, self).get_recipe_env(arch)
        # We add BUILDLIB_PATH to PYTHONPATH so twisted can find _io.so
        env['PYTHONPATH'] = ':'.join([
            self.ctx.get_site_packages_dir(),
            env['BUILDLIB_PATH'],
        ])
        return env

recipe = TwistedRecipe()
