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
    app = IPhoneApplication(
        debug=True,
        dev='server',
        load_view=load_view
    )
    app.start()
    print("Python app finished.")


def load_view(app):
    import enaml
    with enaml.imports():
        import view
        if app.view:
            reload(app.view)
    app.view = view.ContentView()
    app.show_view()


if __name__ == '__main__':
    main()