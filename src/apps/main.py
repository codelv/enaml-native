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

    from enamlnative.android.app import AndroidApplication
    app = AndroidApplication(
        debug=True,
        dev='remote',  # "10.0.2.2" # or 'server'
        load_view=load_view
    )
    app.start()


def load_view(app, should_reload=False):
    import enaml

    #: For debug purposes only!
    app.widget.resetBridgeStats()
    app.widget.resetBridgeCache()

    with enaml.imports():
        import view
        if should_reload:
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


if __name__ == '__main__':
    #: This is used when remote debugging
    sys.path.append(os.path.abspath('.'))

    #: Init remote nativehooks implementation
    from enamlnative.core import remotehooks
    remotehooks.init()
    main()