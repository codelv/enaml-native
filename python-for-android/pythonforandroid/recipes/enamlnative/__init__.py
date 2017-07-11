from pythonforandroid.recipe import PythonRecipe


class EnamlNativeRecipe(PythonRecipe):
    #call_hostpython_via_targetpython = False
    site_packages_name = 'enamlnative'
    version = '2.1'
    url = 'https://github.com/frmdstryr/enaml-native/archive/master.zip'
    depends = [('python2', 'python2crystax'), 'enaml', 'msgpack-python', 'pyjnius']


recipe = EnamlNativeRecipe()
