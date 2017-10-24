from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe


class AtomRecipe(CppCompiledComponentsPythonRecipe):
    site_packages_name = 'atom'
    version = '0.3.10'
    url = 'https://pypi.python.org/packages/91/fa/63ac3a7a0f61f807c0cee2bfad35c5fb7ed37fa5185f9e05016ed4c69099/atom-0.3.10.zip'
    depends = [('python2', 'python2crystax')]
    
recipe = AtomRecipe()
