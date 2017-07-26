from toolchain import PythonRecipe


class EnamlNativeRecipe(PythonRecipe):
    #call_hostpython_via_targetpython = False
    site_packages_name = 'enamlnative'
    version = '2.1'
    url = 'https://github.com/frmdstryr/enaml-native/archive/master.zip'
    depends = ['enaml', 'msgpack-python']


recipe = EnamlNativeRecipe()
