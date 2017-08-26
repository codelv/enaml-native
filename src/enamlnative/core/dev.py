import os
import sys
import json
import shutil
from atom.api import Atom, ForwardInstance, Unicode, Int, Bool
from contextlib import contextmanager

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        print("Entering into {}".format(newdir))
        yield
        print("Returning to {}".format(prevdir))
    finally:
        os.chdir(prevdir)


def get_app():
    from .app import BridgedApplication
    return BridgedApplication


class DevServerClient(Atom):
    _instance = None
    app = ForwardInstance(get_app())
    host = Unicode()
    port = Int(8888)
    url = Unicode('ws://192.168.21.119:8888/dev')
    connected = Bool()
    buf = Unicode()

    def _default_url(self):
        return 'ws://{}:{}/dev'.format(self.host,self.port)

    def _default_app(self):
        return get_app().instance()

    @classmethod
    def initialize(cls,*args, **kwargs):
        try:
            return DevServerClient(*args, **kwargs)
        except ImportError:
            #: TODO: Try twisted
            pass

    @classmethod
    def instance(cls):
        return DevServerClient._instance

    def __init__(self, *args, **kwargs):
        if self.instance() is not None:
            raise RuntimeError("A DevServerClient instance already exists!")
        super(DevServerClient, self).__init__(*args, **kwargs)
        DevServerClient._instance = self

    def start(self):
        print("Starting debug client cwd: {}".format(os.getcwd()))
        print("Sys path: {}".format(sys.path))
        try:
            self.start_tornado_client()
        except ImportError:
            self.start_twisted_client()

    def start_tornado_client(self):
        from tornado.websocket import websocket_connect
        from tornado import gen

        @gen.coroutine
        def run():
            try:
                print("Dev server connecting {}...".format(self.url))
                conn = yield websocket_connect(self.url)
                self.connected = True
                while True:
                    msg = yield conn.read_message()
                    if msg is None: break
                    self.handle_message(msg)
                self.connected = False
            except Exception as e:
                print("Dev server connection dropped: {}".format(e))
            finally:
                #: Try again in a few seconds
                self.app.timed_call(1000, run)

        #: Start
        self.app.deferred_call(run)

    def start_twisted_client(self):
        raise NotImplementedError

    def _observe_connected(self, change):
        print("Dev server {}".format("connected" if self.connected else "disconnected"))

    def handle_message(self, data):
        """ When we get a message """
        msg = json.loads(data)
        print("Dev server message: {}".format(msg))
        if msg['type'] == 'reload':
            #: Show loading screen
            self.app.widget.showLoading("Reloading... Please wait.", now=True)

            with cd(sys.path[0]):
                #: Clear cache
                if os.path.exists('__enamlcache__'):
                    shutil.rmtree('__enamlcache__')
                for fn in msg['files']:
                    print("Updating {}".format(fn))
                    with open(fn, 'w') as f:
                        f.write(msg['files'][fn])

            self.app.reload()