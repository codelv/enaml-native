from pythonforandroid.recipe import PythonRecipe


class EnamlNativeRecipe(PythonRecipe):
    site_packages_name = 'enamlnative'
    version = '3.0'
    url = 'https://github.com/frmdstryr/enaml-native/archive/master.zip'
    depends = [('python2', 'python2crystax'), 'enaml', 'msgpack-python']#, 'pyjnius']#, 'lz4']


recipe = EnamlNativeRecipe()
