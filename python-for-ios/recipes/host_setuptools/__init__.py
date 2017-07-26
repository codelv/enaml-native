from toolchain import PythonRecipe, shprint, current_directory
from os.path import join, exists
import sh
import os
import fnmatch
import shutil


class HostSetuptools(PythonRecipe):
    version = "36.2.0"
    #: Hostopenssl is required or hostpython https requests fail!
    depends = ["hostopenssl", "hostpython"]
    archs = ["x86_64"]
    url = "https://github.com/pypa/setuptools/archive/v{version}.tar.gz"

    def install_python_package(self, name=None, env=None, is_dir=True):
        hostpython = sh.Command(self.ctx.hostpython)
        arch = self.filtered_archs[0]
        build_dir = self.get_build_dir(arch.arch)
        self.build_dir = build_dir
        iosbuild = join(build_dir, "iosbuild")
        if env is None:
            env = self.get_recipe_env(arch)

        #: Patch it,  for some reason the fancy io.open doesn't work
        self.copy_file('build_ext.py',os.path.join(build_dir,'setuptools','command','build_ext.py'))

        with current_directory(build_dir):
            #: Patch bootstrap and easy install to not use io.open
            for f in ['bootstrap.py', 'easy_install.py']:
                shprint(sh.sed,"-i.bak","s/with io.open(/with open(/g",f)

            shprint(hostpython,'bootstrap.py',_env=env)
            shprint(hostpython,'easy_install.py','.',_env=env)



        # sh.curl("-O",  "https://bootstrap.pypa.io/ez_setup.py")
        # shprint(hostpython, "./ez_setup.py")
        # # Extract setuptools egg and remove .pth files. Otherwise subsequent
        # # python package installations using setuptools will raise exceptions.
        # # Setuptools version 28.3.0
        # site_packages_path = join(
        #     self.ctx.dist_dir, 'hostpython',
        #     'lib', 'python2.7', 'site-packages')
        # os.chdir(site_packages_path)
        # with open('setuptools.pth', 'r') as f:
        #     setuptools_egg_path = f.read().strip('./').strip('\n')
        #     unzip = sh.Command('unzip')
        #     shprint(unzip, setuptools_egg_path)
        # os.remove(setuptools_egg_path)
        # os.remove('setuptools.pth')
        # os.remove('easy-install.pth')
        # shutil.rmtree('EGG-INFO')

recipe = HostSetuptools()
