"""
 This file is executed when the Python interpreter is started.
 Use this file to configure all your necessary python code.

"""

import sys
import json
import traceback

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
    import jnius
    import enaml
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

def invoke(callback_id):
    """ Display the view """
    from enamlnative.android.app import AndroidApplication
    app = AndroidApplication.instance()
    app.invoke_callback(callback_id)


