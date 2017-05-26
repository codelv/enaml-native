'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

Forked from https://github.com/joaoventura/pybridge
@author joaoventura
@author: jrm
'''

import time
import sys
import json
import traceback

shared = {}

def router(args):
    """
    Defines the router function that routes by function name.

    :param args: JSON arguments
    :return: JSON response
    """
    request = json.loads(args)
    response = handle(request)
    return json.dumps(response)

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
    import cProfile
    pr = cProfile.Profile()
    pr.enable()
    shared['pr'] = pr

    start_time = time.time()
    print "Start {}".format(start_time)
    import jnius
    print "Load jnius {}s".format(time.time()-start_time)
    import enaml
    print "Load enaml {}s".format(time.time()-start_time)
    from atom.api import Atom
    print "Load atom {}s".format(time.time()-start_time)

    from enamlnative.android.app import AndroidApplication
    print "Import AndroidApp {}s".format(time.time()-start_time)

    MainActivity = jnius.autoclass(activity)
    print "Create MainActiivty {}s".format(time.time()-start_time)

    app = AndroidApplication(MainActivity.mActivity)
    print "Create AndroidApp {}s".format(time.time()-start_time)

    #: Set the view
    with enaml.imports():
        print "Within imports {}s".format(time.time()-start_time)
        from view import ContentView
    print "Import View {}s".format(time.time()-start_time)
    app.view = ContentView()
    print "Created View {}s".format(time.time()-start_time)

def start():
    """ Display the view """
    from enamlnative.android.app import AndroidApplication
    app = AndroidApplication.instance()
    app.start()
    pr = shared['pr']
    pr.disable()
    import pstats, StringIO
    s = StringIO.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print s.getvalue()

def invoke(callback_id):
    """ Display the view """
    from enamlnative.android.app import AndroidApplication
    app = AndroidApplication.instance()
    app.invoke_callback(callback_id)


