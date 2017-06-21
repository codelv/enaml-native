from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe
from pythonforandroid.toolchain import current_directory
import sh


class ZopeInterfaceRecipe(CppCompiledComponentsPythonRecipe):
    call_hostpython_via_targetpython = False
    name = 'zope_interface'
    version = '4.1.3'
    url = 'https://pypi.python.org/packages/source/z/zope.interface/zope.interface-{version}.tar.gz'
    site_packages_name = 'zope.interface'

    depends = [('python2' ,'python2crystax')]
    patches = ['no_tests.patch', 'force_build_ext.patch']

    def prebuild_arch(self, arch):
        super(ZopeInterfaceRecipe, self).prebuild_arch(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            sh.rm('-rf', 'src/zope/interface/tests', 'src/zope/interface/common/tests')
            
    def postbuild_arch(self, arch):
        super(ZopeInterfaceRecipe, self).postbuild_arch(arch)
        with current_directory(self.ctx.get_site_packages_dir(arch)):
            sh.touch( 'zope/__init__.py')
        

recipe = ZopeInterfaceRecipe()
