"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Oct 4, 2017

@author: jrm
"""
import sh
import sys


def main():
    # Make sure instance is cleared
    from enaml.application import Application
    Application._instance = None

    from enamlnative.android.app import AndroidApplication
    app = AndroidApplication(
        debug=True,
        dev='remote',  # "10.0.2.2" # or 'server'
        load_view=load_view
    )
    app.timed_call(5000, run_gestures, app)
    app.start()


def run_gestures(app):
    for i in range(30):
        #: Swipe to next page
        t = i*2000
        app.timed_call(t,
            sh.adb, *'shell input swipe 250 300 -800 300'.split(), _bg=True)
        #: Tap a few places
        for j in range(4):
            app.timed_call(t+i*200,
                sh.adb, *'shell input tap 500 150'.split(), _bg=True)

    app.timed_call(120000, app.stop)


def load_view(app):
    import enaml

    #: For debug purposes only!
    app.widget.resetBridgeStats()
    app.widget.resetBridgeCache()

    with enaml.imports():
        import view
        if app.view:
            reload(view)
        app.view = view.ContentView()
    #: Time how long it takes
    app.show_view()


def test_remote_debug():
    sh.pip('install tornado --user'.split())
    enaml_native = sh.Command('enaml-native')
    enaml_native('start', '--remote-debugging', _bg=True)

    #: Add
    sys.path.append('src/apps/')
    sys.path.append('src/')

    #: Init remote nativehooks implementation
    from enamlnative.core import remotehooks
    remotehooks.init()
    main()

