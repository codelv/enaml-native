import sh
from os.path import join, exists
import os
from toolchain import CppPythonRecipe, shprint, current_directory

class EnamlRecipe(CppPythonRecipe):
    site_packages_name = 'enaml'
    version = '0.9.8'
    url = 'https://github.com/frmdstryr/enaml/archive/master.zip'
    patches = ['0001-Update-setup.py.patch'] # Remove PyQt dependency
    depends = ['atom']

    # def install_package(self, arch):
    #     """Automate the installation of a Python package into the target
    #     site-packages.
    #
    #     """
    #     env = self.get_recipe_env(arch)
    #     build_dir = self.get_build_dir(arch.arch)
    #     try:
    #         super(EnamlRecipe, self).install_package()
    #     except:
    #         #: Dont ccare that this fails, we copy everything manually
    #         pass
    #     with current_directory(join(build_dir, 'build',
    #                                 'lib.{}-2.7'.format(env['_PYTHON_HOST_PLATFORM']))):
    #         dest = join(self.ctx.dist_dir, 'python', arch.arch, 'site-packages')
    #         if not exists(dest):
    #             os.makedirs(dest)
    #         #: Find all the so files
    #         shprint(sh.cp, '-R', 'enaml', dest)
    #
    #         #: Clean up crap from install fail above



recipe = EnamlRecipe()
