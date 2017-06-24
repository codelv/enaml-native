'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

Forked from https://github.com/joaoventura/pybridge
@author joaoventura
@author: jrm
'''
### Comment out to disable profiling
# import cProfile
# pr = cProfile.Profile()
# pr.enable()
#
# shared = {'pr':pr}
### End profiling
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

    from enamlnative.android.bridge import JavaBridgeObject, JavaMethod

    # class View(JavaBridgeObject):
    #     __javaclass__ = 'android.view.View'
    #     addView = JavaMethod('android.view.View')
    #     removeView = JavaMethod('android.view.View')
    #
    # class ScrollView(View):
    #     __javaclass__ = 'android.widget.ScrollView'
    #
    # class LinearLayout(View):
    #     __javaclass__ = 'android.widget.LinearLayout'
    #     setOrientation = JavaMethod('int')
    #
    # class TextView(View):
    #     __javaclass__ = 'android.widget.TextView'
    #     setText = JavaMethod('java.lang.CharSequence')
    #
    # root = ScrollView(app)
    # layout = LinearLayout(app)
    # layout.setOrientation(1)
    # root.addView(layout)
    # for i in range(1000):
    #     tv = TextView(app)
    #     tv.setText("Widget {}".format(i))
    #     layout.addView(tv)
    with enaml.imports():
        from test import ContentView
        app.view = ContentView()

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
    if pr:
        pr.disable()
        import pstats, StringIO
        for sort_by in ['cumulative', 'time']:
            s = StringIO.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
            ps.print_stats()
            print s.getvalue()

def callback(callback_id):
    """ Display the view """
    from enamlnative.android.app import AndroidApplication
    app = AndroidApplication.instance()
    app.invoke_callback(callback_id)




