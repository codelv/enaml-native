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
import cProfile
pr = cProfile.Profile()
pr.enable()

## End profiling
import time
import sys
import jnius
import traceback
import msgpack

def main():
    """ Called by PyBridge.start()
    """
    import enaml
    from enamlnative.android.app import AndroidApplication
    MainActivity = jnius.autoclass('com.enaml.MainActivity')
    app = AndroidApplication(MainActivity.mActivity)
    #app.debug = True
    try:
        with enaml.imports():
            from view import ContentView
            app.view = ContentView()
        app.show_view()
        app.deferred_call(dump_stats)
    except:
        msg = traceback.format_exc()
        print msg
        app.deferred_call(lambda msg=msg:app.send_event('displayError', msg))
    app.start()


def router(args):
    """
    Defines the router function that routes by function name.

    :param args: JSON arguments
    :return: JSON response
    """
    request = msgpack.loads(args)
    response = handle(request)
    return msgpack.dumps(response)

def handle(request):
    """ Handle a json-rpc 2.0 request
    """
    response = {
        "jsonrpc":"2.0",
        "id":request.get("id")
    }
    try:
        if not request.get('method'):
            response['error'] = {"message":"Invalid request. Missing method."}
            return response
        scope = globals()
        if not scope.get(request.get('method')):
            response['error'] = {"message":"Method '{}' not found.".format(request.get('method'))}
            return response

        method = scope.get(request.get('method'))
        params = request.get('params')
        if not params:
            result = method()
        elif isinstance(params,dict):
            result = method(**params)
        else:
            result = method(*params)
        response['result'] = result
    except:
        response['error'] = {
            "message": traceback.format_exc(),
        }
    return response

def version():
    return 'Python version is %s. Path is %s' % (sys.version,sys.path)

def load(activity):
    """ Get and load the view """
    import jnius
    import enaml
    from atom.api import Atom
    from enamlnative.android.app import AndroidApplication
    MainActivity = jnius.autoclass(activity)
    app = AndroidApplication(MainActivity.mActivity)

    #: Set the view
    with enaml.imports():
        from view import ContentView
    app.view = ContentView()

def start():
    """ Display the view """
    from enamlnative.android.app import AndroidApplication
    app = AndroidApplication.instance()
    app.start()
    shared['app'] = app # So it doesn't get GC'd ?
    pr = shared.get('pr')

def dump_stats():
    pr.disable()
    import pstats, StringIO
    for sort_by in ['cumulative', 'time']:
        s = StringIO.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
        ps.print_stats(0.3)
        print s.getvalue()

def callback(callback_id):
    """ Display the view """
    from enamlnative.android.app import AndroidApplication
    app = AndroidApplication.instance()
    app.invoke_callback(callback_id)




