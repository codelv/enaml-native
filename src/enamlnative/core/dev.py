# -*- coding: utf-8 -*-
'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
import os
import sys
import json
import shutil
import inspect
import traceback
from atom.api import Atom, ForwardInstance, Enum, Unicode, Int, Bool
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


DEFAULT_CODE = """
from enamlnative.core.api import *
from enamlnative.widgets.api import *


enamldef ContentView(Flexbox):
    TextView:
        text = "Hello world!"
"""

INDEX_PAGE = """<html>
<head>
  <title>Enaml-Native Playground</title>
  <!--Import Google Icon Font-->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

  <!-- Compiled and minified CSS -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css">
  <link rel="shortcut icon" href="https://www.codelv.com/static/faveicon.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body>
  <div class="nav-fixed">
    <nav role="navigation" class="teal">
      <div class="nav-wrapper" style="margin-left:1em;">
        <a href="#" class="brand-logo">Enaml-Native Playground</a>
        <ul id="nav-mobile" class="right hide-on-med-and-down">
          <li><a href="https://www.codelv.com/projects/enaml-native/">Project</a></li>
          <li><a href="https://www.codelv.com/projects/enaml-native/docs/">Docs</a></li>
        </ul>
      </div>
    </nav>
  </div>
  <div class="row" style="margin-bottom:0;">
    <div class="col l3 m2 s12" style="padding:0; max-height:100%; overflow-y:scroll;">
      <nav>
        <div class="nav-wrapper grey darken-3">
          <a href="#components" style="margin-left:1em;">Components</a>
        </div>
      </nav>
      <ul id="components" data-collapsible="accordion">
        ${components}
      </ul>
    </div>
    <div class="col l9 m10 s12" style="padding:0;">
      <div id="editor" style="height:100%;width:100%;">${code}</div> <!-- code -->
    </div>
  </div>
  <div class="fixed-action-btn">
    <a id="run" class="btn-floating btn-large blue" href="#">
       <i class="large material-icons">play_arrow</i>
     </a>
  </div>
  <footer class="page-footer teal">
    <div>
      <div class="row">
        <div class="col l6 s12">
          <h5 class="white-text">Enaml-Native Playground</h5>
          <p class="grey-text text-lighten-4">Test out enaml native app code right from the browser!</p>
        </div>
        <div class="col l4 offset-l2 s12">
          <h5 class="white-text">Links</h5>
          <ul>
            <li><a class="grey-text text-lighten-3" href="https://www.codelv.com/projects/enaml-native/docs/">Docs</a></li>
            <li><a class="grey-text text-lighten-3" href="https://github.com/frmdstryr/enaml-native/">Code</a></li>
            <li><a class="grey-text text-lighten-3" href="https://www.codelv.com/projects/enaml-native/support/">Support</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-copyright">
      <div style="margin-left:1em;">
        © 2017 <a href="https://www.codelv.com">codelv.com</a>
        <a class="grey-text text-lighten-4 right" href="https://www.codelv.com/projects/enaml-native/">Python powered native apps</a>
      </div>
    </div>
  </footer>

  <!--Import jQuery before materialize.js-->
  <script type="text/javascript" src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
  <!-- Compiled and minified JavaScript -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js"></script>
  <!-- Editor -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.2.8/ace.js"></script>
  <script type="text/javascript">
    $(document).ready(function(){
        // Init components
        $('#components').collapsible();

        // Init editor
        var editor = ace.edit("editor");
        editor.setTheme("ace/theme/github");
        editor.getSession().setMode("ace/mode/python");

        // Init app dev session
        var enaml;
        $('#run').click(function(e){
            try {
                // Trigger a reload
                enaml.send(JSON.stringify({
                    'type':'reload',
                    'files':{
                        'view.enaml':editor.getValue(),
                    }
                }));
            } catch (ex) {
                console.log(ex);
            }
        });
        var connect = function(){
            var url = "ws://"+window.location.hostname+":8888/dev";
            enaml = new WebSocket(url);

            enaml.onopen = function(e) {
                console.log("Connected");
            }
            enaml.onmessage = function(e) {

            }
            enaml.onclose = function(e) {
                console.log("Disconnected");
                connect();
            }
        }
        connect();
    });
  </script>
</body>
</html>"""

#: This is why enaml-web is awesome, doing this sucks!
COMPONENT_FIELD_TMPL = """

"""

COMPONENT_TMPL = """
<li>
    <div class="collapsible-header" id="component-{id}">{name}</div>
    <div class="collapsible-body" style="padding:0 1em;">
        <table class="bordered striped" style="font-size: small;">
          <thead>
            <tr><td>Attr</td><td>Info</td></tr>
          </thead>
          <tbody>
            {info}
            {items}
          </tbody>
        </table>
    </div>
</li>"""

DROPDOWN_TMPL = """
<a class='dropdown-button' href='#' data-activates='{id}'>{name}</a>
<ul id='{id}' class='dropdown-content'>
{items}
</ul>"""


def get_app():
    from .app import BridgedApplication
    return BridgedApplication


class DevServerSession(Atom):
    """ Connect to a dev server running on the LAN
        or if host is 0.0.0.0 server a page to let
        code be pasted in. Note this should NEVER be used
        in a released app!
    """
    _instance = None
    app = ForwardInstance(get_app)
    host = Unicode()
    port = Int(8888)
    url = Unicode('ws://192.168.21.119:8888/dev')
    connected = Bool()
    buf = Unicode()
    mode = Enum('client', 'server')

    def _default_url(self):
        return 'ws://{}:{}/dev'.format(self.host,self.port)

    def _default_app(self):
        return get_app().instance()

    @classmethod
    def initialize(cls,*args, **kwargs):
        try:
            return DevServerSession(*args, **kwargs)
        except ImportError:
            #: TODO: Try twisted
            pass

    @classmethod
    def instance(cls):
        return DevServerSession._instance

    def __init__(self, *args, **kwargs):
        if self.instance() is not None:
            raise RuntimeError("A DevServerClient instance already exists!")
        super(DevServerSession, self).__init__(*args, **kwargs)
        DevServerSession._instance = self

    def _default_mode(self):
        """ If host is set to server then serve it from the app! """
        return "server" if self.host=="server" else "client"

    def start(self):
        print("Starting debug client cwd: {}".format(os.getcwd()))
        print("Sys path: {}".format(sys.path))
        if self.mode=='client':
            try:
                self.start_tornado_client()
            except ImportError:
                self.start_twisted_client()
        else:
            try:
                self.start_tornado_server()
            except ImportError:
                self.start_twisted_server()

    def start_tornado_server(self):
        """ Run a server in the app and host a page that does what the dev server does """
        import tornado.ioloop
        import tornado.web
        import tornado.websocket
        ioloop = tornado.ioloop.IOLoop.current()
        server = self

        class DevWebSocketHandler(tornado.websocket.WebSocketHandler):
            def open(self):
                print("Dev server client connected!")

            def on_message(self, message):
                server.handle_message(message)

            def on_close(self):
                print("Dev server client lost!")

        class MainHandler(tornado.web.RequestHandler):

            def get_members(self, declaration):
                members = declaration.members().values()

                try:
                    #: Exclude parent class members
                    parent = declaration.__mro__[1]
                    class_members = []
                    inherited = parent.members().keys()
                    class_members = [m for m in members if m.name not in inherited]

                    #: If not a direct subclass of View, show the parent members
                    if not class_members and parent.__name__ != 'View':
                        #: Try again one more time
                        parent = parent.__mro__[1]
                        inherited = parent.members().keys()
                        class_members = [m for m in members if m.name not in inherited]

                    members = class_members
                except:
                    pass

                return [m for m in members if not m.name.startswith("_")]

            def render_component_types(self, declaration, member):
                """ """
                node_type = member.__class__.__name__.lower()
                node_id = "{}-{}".format(declaration.__name__, member.name).lower()
                #: Build items
                items = []
                if isinstance(member, Enum):
                    items = ["<li><a href='#1'>{}</a></li>".format(it) for it in member.items]
                #: TODO: show instance types for instances, tuples, lists, etc..
                #elif isinstance(member, )

                #: Render dropdown if needed
                if items:
                    return DROPDOWN_TMPL.format(id=node_id, name=node_type, items="".join(items))
                return "{}".format(node_type)

            def render_code(self):
                """ Try to load the previous code (if we had a crash or something)
                    I should allow saving.
                """
                tmp_dir = os.environ.get('TMP','')
                view_code = os.path.join(tmp_dir,'view.enaml')
                if os.path.exists(view_code):
                    try:
                        with open(view_code) as f:
                            return f.read()
                    except:
                        pass
                return DEFAULT_CODE

            def render_component(self, declaration):
                """ Render a row of all the attributes """
                items = ["""<tr><td>{name}</td><td>{type}</td></tr>"""
                             .format(name=m.name,type=self.render_component_types(declaration, m))
                         for m in self.get_members(declaration)]

                info = []
                parent = declaration.__mro__[1]
                #: Superclass
                info.append("<tr><td>extends component</td><td><a href='#component-{id}'>{name}</a></td></td>"
                            .format(id=parent.__name__.lower(), name=parent.__name__))

                #: Source and example, only works with enamlnative builtins
                source_path = inspect.getfile(declaration).replace(".pyo", ".py").replace(".pyc", ".py")
                if 'enamlnative' in source_path:
                    source_link = "https://github.com/frmdstryr/enaml-native/tree/master/src/{}".format(
                        "enamlnative"+source_path.split("enamlnative")[1]
                    )
                    info.append("<tr><td>source code</td><td><a href='{}' target='_blank'>show</a></td></td>"
                                .format(source_link))

                    #: Examples link
                    example_link = "https://www.codelv.com/projects/enaml-native/docs/components#{}" \
                        .format(declaration.__name__.lower())
                    info.append("<tr><td>example usage</td><td><a href='{}' target='_blank'>view</a></td></td>"
                                .format(example_link))

                return COMPONENT_TMPL.format(id=declaration.__name__.lower(),
                                             name=declaration.__name__,
                                             info="".join(info),
                                             items="".join(items))

            def get(self):
                from enaml.widgets.toolkit_object import ToolkitObject
                from enamlnative.widgets import api

                #: Get all declared widgets
                widgets = [obj for (n,obj) in inspect.getmembers(api) if inspect.isclass(obj)
                           and issubclass(obj,ToolkitObject)]
                #: Render to html
                components = "\n".join([self.render_component(w) for w in widgets])

                #: Just a little hackish, but hey it works
                self.write(INDEX_PAGE.replace("${components}", components).replace("${code}",self.render_code()))

        app = tornado.web.Application([
            (r"/", MainHandler),
            (r"/dev", DevWebSocketHandler),
        ])

        #: Start listening
        app.listen(self.port)

    def start_tornado_client(self):
        """ Connect to a dev server running on a pc. """
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
        #: TODO:...
        raise NotImplementedError

    def start_twisted_server(self):
        #: TODO:...
        raise NotImplementedError

    def _observe_connected(self, change):
        print("Dev server {}".format("connected" if self.connected else "disconnected"))

    def handle_message(self, data):
        """ When we get a message """
        msg = json.loads(data)
        print("Dev server message: {}".format(msg))
        if msg['type'] == 'reload':
            #: Show loading screen
            try:
                self.app.widget.showLoading("Reloading... Please wait.", now=True)
            except:
                #: TODO: Implement for iOS...
                traceback.print_exc()

            #: On iOS we can't write in the app bundle
            if os.environ.get('TMP'):
                tmp_dir = os.environ['TMP']
                if not os.path.exists(tmp_dir):
                    os.makedirs(tmp_dir)
                if tmp_dir not in sys.path:
                    sys.path.insert(0, tmp_dir)

                    import site
                    reload(site)

            with cd(sys.path[0]):
                #: Clear cache
                if os.path.exists('__enamlcache__'):
                    shutil.rmtree('__enamlcache__')
                for fn in msg['files']:
                    print("Updating {}".format(fn))
                    with open(fn, 'wb') as f:
                        f.write(msg['files'][fn].encode('utf-8'))

            self.app.reload()