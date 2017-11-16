# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

Forked from https://github.com/joaoventura/pybridge
@author joaoventura
@author: jrm
"""
import sys
import os

# ### Comment out to disable profiling
# import cProfile
# pr = cProfile.Profile()
# pr.enable()
## End profiling


def main():
    """ Called by PyBridge.start()
    """
    #: If we don't our code goes away
    os.environ['TMP'] = os.path.join(sys.path[0], '../tmp')

    import enamlnative
    from enamlnative.android.app import AndroidApplication
    app = AndroidApplication()
    #app.debug = True #: Makes a lot of lag!
    app.dev = 'server' # "10.0.2.2" # or 'server'
    app.reload_view = reload_view
    app.deferred_call(load_view, app)
    app.deferred_call(dump_stats)
    app.start()


def load_view(app):
    import enaml
    import enamlnative
    with enaml.imports():
        from view import ContentView
        app.view = ContentView()
    #: Time how long it takes
    app.show_view()


def reload_view(app):
    import enaml
    import enamlnative

    #: For Debug purposes only!
    app.widget.resetBridgeStats()

    with enaml.imports():
        import view
        reload(view)
        app.view = view.ContentView()

    #: Time how long it takes
    app.show_view()

def dump_stats():
    try:
        pr.disable()
        import pstats, StringIO
        for sort_by in ['cumulative', 'time']:
            s = StringIO.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
            ps.print_stats(0.3)
            print s.getvalue()
    except:
        pass




