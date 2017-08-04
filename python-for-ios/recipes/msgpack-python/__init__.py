from os.path import join
from toolchain import CythonRecipe, FrameworkLibrary


class MsgPackFramework(FrameworkLibrary):
    #: Include all msgpack dylibs
    libraries = ['python/{arch}/msgpack.*.dylib']


class MsgPackRecipe(CythonRecipe):
    version = '0.4.7'
    url = 'https://pypi.python.org/packages/source/m/msgpack-python/msgpack-python-{version}.tar.gz'
    depends = ['python']#,'host_setuptools']
    #library = "libmsgpack.a"
    pre_build_ext = True
    framework = MsgPackFramework()


recipe = MsgPackRecipe()
