'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 21, 2017

@author: jrm
'''

def main():
    #: Install Library Loader
    import enamlnative
    enamlnative.install()


    from enamlnative.ios.app import IPhoneApplication
    app = IPhoneApplication()
    app.debug = True
    app.deferred_call(load_view, app)
    app.start()
    print("Python app finished.")

def load_view(app):
    import enaml
    with enaml.imports():
        from view import MainView
    app.view = MainView()
    app.show_view()


if __name__ == '__main__':
    main()