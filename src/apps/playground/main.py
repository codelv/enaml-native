# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

Forked from https://github.com/joaoventura/pybridge
@author joaoventura
@author: jrm
"""
import os
import sys

# ### Comment out to disable profiling
# import cProfile
# pr = cProfile.Profile()
# pr.enable()
## End profiling


def main():
    """ Called by PyBridge.start()
    """

    #: If we set the TMP env variable the dev reloader will save file
    #: and load changes in this directory instead of overwriting the
    #: ones installed with the app.
    os.environ['TMP'] = os.path.join(sys.path[0], '../tmp')

    from enamlnative.android.app import AndroidApplication

    app = AndroidApplication(
        debug=True,  #: Makes a lot of lag!
        dev='server',
        load_view=load_view,
    )
    app.start()


def load_view(app, should_reload=False):
    import enaml
    with enaml.imports():
        import view
        if should_reload:
            reload(view)
        app.view = view.ContentView()
    app.show_view()







