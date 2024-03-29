"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.
"""
import inspect
import json
import os
import shutil
import sys
import traceback
import enaml
import enamlnative
from contextlib import contextmanager
from importlib import reload
from atom.api import Atom, Bool, Enum, ForwardInstance, Instance, Int, Str
from .bridge import Command

with enamlnative.imports():
    from .hotswap.core import Hotswapper


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

enamldef MainWindow(Window):
    Flexbox:
        flex_direction = "column"
        TextView:
            text = "Hello world!"
"""

INDEX_PAGE = """<html>
<head>
  <title>Enaml-Native Playground</title>
  <!--Import Google Icon Font-->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons"
    rel="stylesheet">

  <!-- Compiled and minified CSS -->
  <link rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css">
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
    <div class="col l3 m2 s12" style="padding:0; max-height:100%; overflow-y:scroll; background: #fff;">
      <nav>
        <div class="nav-wrapper grey darken-3">
          <a href="#files" style="margin-left:1em;">App</a>
        </div>
      </nav>
      <ul id="files" data-collapsible="accordion">
        ${files}
      </ul>
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
     <ul>
      <li><a id="hotswap" href="#" class="btn-floating red"><i class="material-icons">refresh</i></a></li>
    </ul>
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
        © 2017 <a href="https://www.codelv.com">www.codelv.com</a>
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

        // Saved files
        var state = {
            currentFile: "view.enaml",
            files: {},
        };

        $('.editor-file').click(function(e){
            var file = $(this).attr('id');

            // Save the current state
            state.files[state.currentFile] = editor.getValue();

            var updateEditor = function(text){
                // Load the new one
                state.currentFile = file;
                editor.setValue(text,1);
            };

            // Try to pull from tmp first (previous updates)
            // fallback to source code
            fetch("tmp/"+file).then(function(r){
                if (r.status==404) {
                    fetch("source/"+file).then(function(r){
                        r.text().then(updateEditor);
                    });
                } else {
                    r.text().then(updateEditor);
                }
            });
        });

        $('#run').click(function(e){
            try {
                // Trigger a reload
                // Update current file
                state.files[state.currentFile] = editor.getValue();

                enaml.send(JSON.stringify({
                    'type':'reload',
                    'files':state.files
                }));
            } catch (ex) {
                console.log(ex);
            }
        });
        $('#hotswap').click(function(e){
            try {
                // Trigger a reload

                // Update current file
                state.files[state.currentFile] = editor.getValue();

                // Push our changes updates
                enaml.send(JSON.stringify({
                    'type':'hotswap',
                    'files':state.files
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
</ul>
"""

FOLDER_TMPL = """
<li>
    <div class="collapsible-header" id="file-{id}">{name}</div>
    <div class="collapsible-body" style="padding:0 1em;">
        {items}
    </div>
</li>
"""
FILE_TMPL = """
<li>
    <div class="collapsible-header editor-file" id="{id}">{name}</div>
</li>
"""


def get_app():
    from .app import BridgedApplication

    return BridgedApplication


class DevClient(Atom):
    """Abstract dev client. Override `start` to implement"""

    #: Current websocket connection
    connection = Instance(object)

    #: Mode of operation
    mode = Enum("client", "remote")

    @classmethod
    def available(cls):
        """Return True if this dev client impl can be used."""
        return False

    def start(self, session):
        raise NotImplementedError

    def write_message(self, data, binary=False):
        """Write a message to the client"""
        raise NotImplementedError


class TornadoDevClient(DevClient):
    @classmethod
    def available(cls):
        """Return True if this dev client impl can be used."""
        try:
            import tornado  # noqa: F401

            return True
        except ImportError:
            return False

    def start(self, session):
        from tornado import gen
        from tornado.websocket import websocket_connect

        @gen.coroutine
        def run():
            #: Create local references
            mode = session.mode
            process_events = session.app.process_events
            app = session.app

            try:
                # print("Dev client connecting {}...".format(session.url))
                conn = yield websocket_connect(session.url)
                session.connected = True
                self.connection = conn

                #: Start remote debugger
                if mode == "remote":
                    app.load_view(app)

                while True:
                    msg = yield conn.read_message()
                    if msg is None:
                        break
                    if mode == "remote":
                        process_events(msg)
                    else:
                        r = session.handle_message(msg)
                        conn.write_message(json.dumps(r))
                session.connected = False
            except Exception as e:
                if "refused" not in f"{e}":
                    print(f"Dev client connection dropped: {e}")
            finally:
                if mode == "remote":
                    session.app.stop()
                else:
                    #: Try again in a few seconds
                    session.app.timed_call(1000, run)

        #: Start
        session.app.deferred_call(run)

    def write_message(self, data, binary=False):
        """Write a message to the client"""
        self.connection.write_message(data, binary)


class DevServer(Atom):
    """Abstract dev server. Override `start` to implement"""

    @classmethod
    def available(cls):
        """Return True if this dev server impl can be used."""
        return False

    def get_component_members(self, declaration):
        members = declaration.members().values()

        try:
            #: Exclude parent class members
            parent = declaration.__mro__[1]
            class_members = []
            inherited = parent.members().keys()
            class_members = [m for m in members if m.name not in inherited]

            #: If not a direct subclass of View, show the parent members
            if not class_members and parent.__name__ != "View":
                #: Try again one more time
                parent = parent.__mro__[1]
                inherited = parent.members().keys()
                class_members = [m for m in members if m.name not in inherited]

            members = class_members
        except Exception:
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
        # elif isinstance(member, )

        #: Render dropdown if needed
        if items:
            return DROPDOWN_TMPL.format(
                id=node_id, name=node_type, items="".join(items)
            )
        return "{}".format(node_type)

    def render_files(self, root=None):
        """Render the file path as accordions"""
        if root is None:
            root = sys.path[0]
        items = []
        for filename in sorted(os.listdir(root)):
            # for subdirname in dirnames:
            #     path = os.path.join(dirname, subdirname)
            #     items.append(FOLDER_TMPL.format(
            #         name=subdirname,
            #         id=path,
            #         items=self.render_files(path)
            #     ))
            # for filename in filenames:
            f, ext = os.path.splitext(filename)
            if ext in [".py", ".enaml"]:
                items.append(FILE_TMPL.format(name=filename, id=filename))

        return "".join(items)

    def render_code(self):
        """Try to load the previous code (if we had a crash or something)
        I should allow saving.
        """
        tmp_dir = os.environ.get("TMP", "")
        view_code = os.path.join(tmp_dir, "view.enaml")
        if os.path.exists(view_code):
            try:
                with open(view_code) as f:
                    return f.read()
            except Exception:
                pass
        return DEFAULT_CODE

    def render_component(self, declaration):
        """Render a row of all the attributes"""
        items = [
            """<tr><td>{name}</td><td>{type}</td></tr>""".format(
                name=m.name, type=self.render_component_types(declaration, m)
            )
            for m in self.get_component_members(declaration)
        ]

        info = []
        parent = declaration.__mro__[1]
        #: Superclass
        info.append(
            "<tr><td>extends component</td>"
            "<td><a href='#component-{id}'>{name}</a></td></td>".format(
                id=parent.__name__.lower(), name=parent.__name__
            )
        )

        #: Source and example, only works with enamlnative builtins
        source_path = (
            inspect.getfile(declaration).replace(".pyo", ".py").replace(".pyc", ".py")
        )
        if "enamlnative" in source_path:
            assets_path = os.environ.get("ASSETS", "assets/python/")
            cache_path = os.environ.get("CACHE", "cache/")
            if assets_path in source_path:
                url = source_path.split(assets_path)[-1]
            elif cache_path in source_path:
                url = source_path.split(cache_path)[-1]
            else:
                # Cant find the full path probably will be a dead link
                url = "enamlnative/{}".format(source_path.split("enamlnative")[-1])
            source_link = (
                "https://github.com/codelv/"
                "enaml-native/tree/master/src/{}".format(url)
            )
            info.append(
                "<tr><td>source code</td>"
                "<td><a href='{}' target='_blank'>show</a></td></td>".format(
                    source_link
                )
            )

            #: Examples link
            example_link = (
                "https://codelv.com/projects/"
                "enaml-native/docs/components#{}".format(declaration.__name__.lower())
            )
            info.append(
                "<tr><td>example usage</td>"
                "<td><a href='{}' target='_blank'>view</a></td></td>".format(
                    example_link
                )
            )

        return COMPONENT_TMPL.format(
            id=declaration.__name__.lower(),
            name=declaration.__name__,
            info="".join(info),
            items="".join(items),
        )

    def render_editor(self):
        from enaml.widgets.toolkit_object import ToolkitObject
        from enamlnative.widgets import api

        #: Get all declared widgets
        widgets = [
            obj
            for (n, obj) in inspect.getmembers(api)
            if inspect.isclass(obj) and issubclass(obj, ToolkitObject)
        ]
        #: Render to html
        components = "\n".join([self.render_component(w) for w in widgets])

        #: Just a little hackish, but hey it works
        return (
            INDEX_PAGE.replace("${components}", components)
            .replace("${code}", self.render_code())
            .replace("${files}", self.render_files())
        )

    def start(self, session):
        raise NotImplementedError


class TornadoDevServer(DevServer):
    @classmethod
    def available(cls):
        """Return True if this dev server impl can be used."""
        try:
            import tornado  # noqa: F401

            return True
        except ImportError:
            return False

    def start(self, session):
        with enamlnative.imports():
            import tornado.ioloop
            import tornado.web
            import tornado.websocket
        server = self

        class DevWebSocketHandler(tornado.websocket.WebSocketHandler):
            def open(self):
                print("Dev server client connected!")

            def on_message(self, message):
                #: Delegate
                r = session.handle_message(message)
                self.write_message(json.dumps(r))

            def on_close(self):
                print("Dev server client lost!")

        class MainHandler(tornado.web.RequestHandler):
            def get(self):
                #: Delegate
                self.write(server.render_editor())

            def post(self):
                #: Allow posting events
                r = session.handle_message(self.request.body)
                self.write(json.dumps(r))

        app = tornado.web.Application(
            [
                (r"/", MainHandler),
                (r"/dev", DevWebSocketHandler),
                (
                    r"/tmp/(.*)",
                    tornado.web.StaticFileHandler,
                    {"path": os.environ.get("TMP", sys.path[0])},
                ),
                (r"/source/(.*)", tornado.web.StaticFileHandler, {"path": sys.path[0]}),
            ]
        )

        #: Start listening
        app.listen(session.port)
        print("Tornado dev server started on {}".format(session.port))


class DevServerSession(Atom):
    """Connect to a dev server running on the LAN
    or if host is 0.0.0.0 server a page to let
    code be pasted in. Note this should NEVER be used
    in a released app!
    """

    #: Singleton Instance of this class
    _instance = None

    #: Reference to the current Application
    app = ForwardInstance(get_app)

    #: Host to connect to (in client mode) or
    #: if set to "server" it will enable "server" mode
    host = Str()

    #: Port to serve on (in server mode) or port to connect to (in client mode)
    port = Int(8888)

    #: URL to connect to (in client mode)
    url = Str("ws://192.168.21.119:8888/dev")

    #: Websocket connection state
    connected = Bool()

    #: Message buffer
    buf = Str()

    #: Dev session mode
    mode = Enum("client", "server", "remote")

    #: Hotswap support class
    hotswap = Instance(Hotswapper)

    #: Delegate dev server
    server = Instance(DevServer)

    #: Delegate client
    client = Instance(DevClient)

    # -------------------------------------------------------------------------
    # Initialization
    # -------------------------------------------------------------------------
    @classmethod
    def initialize(cls, *args, **kwargs):
        """Create an instance of this class."""
        try:
            return DevServerSession(*args, **kwargs)
        except ImportError:
            pass

    @classmethod
    def instance(cls):
        """Get the singleton instance"""
        return cls._instance

    def __init__(self, *args, **kwargs):
        """Overridden constructor that forces only one instance to ever exist."""
        if self.instance() is not None:
            raise RuntimeError("A DevServerClient instance already exists!")
        super().__init__(*args, **kwargs)
        DevServerSession._instance = self

    def start(self):
        """Start the dev session. Attempt to use tornado first, then try
        twisted

        """
        print("Starting debug client cwd: {}".format(os.getcwd()))
        print("Sys path: {}".format(sys.path))

        #: Initialize the hotswapper
        self.hotswap = Hotswapper(debug=False)

        if self.mode == "server":
            self.server.start(self)
        else:
            self.client.start(self)

    # -------------------------------------------------------------------------
    # Defaults
    # -------------------------------------------------------------------------
    def _default_mode(self):
        """If host is set to server then serve it from the app!"""
        host = self.host
        if host == "server":
            return "server"
        elif host == "remote":
            return "remote"
        return "client"

    def _default_url(self):
        """Websocket URL to connect to and listen for reload requests"""
        host = "localhost" if self.mode == "remote" else self.host
        return "ws://{}:{}/dev".format(host, self.port)

    def _default_app(self):
        """Application instance"""
        return get_app().instance()

    def _default_server(self):
        if TornadoDevServer.available():
            return TornadoDevServer()
        raise NotImplementedError(
            "No dev servers are available! "
            "Include tornado or twisted in your requirements!"
        )

    def _default_client(self):
        if TornadoDevClient.available():
            return TornadoDevClient()
        raise NotImplementedError(
            "No dev clients are available! "
            "Include tornado or twisted in your requirements!"
        )

    def _observe_connected(self, change):
        """Log connection state changes"""
        state = "connected" if self.connected else "disconnected"
        print(f"Dev session {state}")

    # -------------------------------------------------------------------------
    # Dev Session API
    # -------------------------------------------------------------------------
    def write_message(self, data, binary=False):
        """Write a message to the active client"""
        self.client.write_message(data, binary=binary)

    def handle_message(self, data):
        """When we get a message"""
        msg = json.loads(data)
        print("Dev server message: {}".format(msg))
        handler_name = "do_{}".format(msg["type"])
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            result = handler(msg)
            return {"ok": True, "result": result}
        else:
            err = "Warning: Unhandled message: {}".format(msg)
            print(err)
            return {"ok": False, "message": err}

    # -------------------------------------------------------------------------
    # Message handling API
    # -------------------------------------------------------------------------
    def do_reload(self, msg):
        """Called when the dev server wants to reload the view."""
        #: TODO: This should use the autorelaoder
        app = self.app
        app.activity.show_loading("Reloading...")
        self.save_changed_files(msg)
        try:
            with enaml.imports():
                app.activity.on_reload()
        except Exception:
            #: Display the error
            app.send_event(Command.ERROR, traceback.format_exc())

    def do_hotswap(self, msg):
        """Attempt to hotswap the code"""
        #: Show hotswap tooltip
        try:
            self.app.widget.showTooltip("Hot swapping...", now=True)
        except Exception:
            pass
        self.save_changed_files(msg)

        hotswap = self.hotswap
        app = self.app
        try:
            print("Attempting hotswap....")
            with hotswap.active():
                hotswap.update(app.view)
        except Exception:
            #: Display the error
            app.send_event(Command.ERROR, traceback.format_exc())

    # -------------------------------------------------------------------------
    # Utility methods
    # -------------------------------------------------------------------------
    def save_changed_files(self, msg):
        #: On iOS we can't write in the app bundle
        if os.environ.get("TMP"):
            tmp_dir = os.environ["TMP"]
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)
            if tmp_dir not in sys.path:
                sys.path.insert(0, tmp_dir)

                import site

                reload(site)

        with cd(sys.path[0]):
            #: Clear cache
            if os.path.exists("__enamlcache__"):
                shutil.rmtree("__enamlcache__")
            for fn in msg["files"]:
                print("Updating {}".format(fn))
                folder = os.path.dirname(fn)
                if folder and not os.path.exists(folder):
                    os.makedirs(folder)
                with open(fn, "wb") as f:
                    f.write(msg["files"][fn].encode("utf-8"))
