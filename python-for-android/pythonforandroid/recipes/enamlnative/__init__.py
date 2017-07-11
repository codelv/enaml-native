from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe


class EnamlNativeRecipe(CppCompiledComponentsPythonRecipe):
    site_packages_name = 'atom'
    version = '2.1'
    url = 'http://github.com/frmdstryr/enaml-native'
    depends = [('python2', 'python2crystax'), 'enaml', 'msgpack-python', 'pyjnius']


recipe = EnamlNativeRecipe()
