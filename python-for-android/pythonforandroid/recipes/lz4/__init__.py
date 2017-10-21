from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe


class Liblz4Recipe(CppCompiledComponentsPythonRecipe):
    version = '0.10.1'
    url = 'https://github.com/python-lz4/python-lz4/archive/v{version}.tar.gz'
    patches = ['setup.py.patch']

recipe = Liblz4Recipe()
