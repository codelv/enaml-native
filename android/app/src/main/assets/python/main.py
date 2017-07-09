'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

Forked from https://github.com/joaoventura/pybridge
@author joaoventura
@author: jrm
'''
import traceback

# ### Comment out to disable profiling
# import cProfile
# pr = cProfile.Profile()
# pr.enable()
## End profiling
import jnius
import enaml
from enamlnative.android.app import AndroidApplication

def main():
    """ Called by PyBridge.start()
    """
    MainActivity = jnius.autoclass('com.enaml.MainActivity')
    app = AndroidApplication(MainActivity.mActivity)
    #app.debug = True #: Makes a lot of lag!
    app.deferred_call(load_view, app)
    app.deferred_call(dump_stats)
    app.start()


def load_view(app):
    with enaml.imports():
        from view import ContentView
        app.view = ContentView()
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




