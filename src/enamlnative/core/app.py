# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

"""
import json
import traceback
from atom.api import (Atom, Enum, Callable, List, Instance, Value,
                      Int, Unicode, Bool, Dict)
from enaml.application import Application
from . import bridge
from .loop import EventLoop


class Plugin(Atom):
    """ Simplified way to load a plugin from an entry_point line. 
    The enaml-native and p4a build process removes pkg_resources 
    and all package related metadata this simply imports from an
    entry point string in the format "package.path.module:attr"
    
    """
    name = Unicode()
    source = Unicode()

    def load(self):
        """ Load the object defined by the plugin entry point """
        print("[DEBUG] Loading plugin {} from {}".format(self.name,
                                                         self.source))
        import pydoc
        path, attr = self.source.split(":")
        module = pydoc.locate(path)
        return getattr(module, attr)


class BridgedApplication(Application):
    """ An abstract implementation of an Enaml application.

    This serves as a base class for both Android and iOS applications and 
    provides support for the python event loop, the development server 
    and the bridge.

    """
    __id__ = Int(-1)

    #: Keep screen on by setting the WindowManager flag
    keep_screen_on = Bool()

    #: Application lifecycle state must be set by the implementation
    state = Enum('created', 'paused', 'resumed', 'stopped', 'destroyed')

    #: View to display within the activity
    view = Value()

    #: If true, debug bridge statements
    debug = Bool()

    #: Use dev server
    dev = Unicode()
    _dev_session = Value()
    reload_view = Callable()

    #: Event loop
    loop = Instance(EventLoop)

    #: Events to send to the bridge
    _bridge_queue = List()

    #: Delay to wait before sending events (in ms)
    _bridge_timeout = Int(1)

    #: Count of pending send calls
    _bridge_pending = Int(0)

    #: Entry points to load plugins
    plugins = Dict()

    # -------------------------------------------------------------------------
    # Defaults
    # -------------------------------------------------------------------------
    def _default_loop(self):
        """ Get the event loop based on what libraries are available. """
        return EventLoop.default()

    def _default_plugins(self):
        """ Get entry points to load any plugins installed. 
        The build process should create an "entry_points.json" file
        with all of the data from the installed entry points.
        
        """
        plugins = {}
        try:
            with open('entry_points.json') as f:
                entry_points = json.load(f)
            for ep, obj in entry_points.items():
                plugins[ep] = []
                for name, src in obj.items():
                    plugins[ep].append(Plugin(name=name, source=src))
        except Exception as e:
            print("Failed to load entry points {}".format(e))
        return plugins

    # -------------------------------------------------------------------------
    # BridgedApplication Constructor
    # -------------------------------------------------------------------------
    def __init__(self):
        """ Initialize the event loop error handler.  Subclasses must properly
        initialize the proxy resolver.
        
        """
        super(BridgedApplication, self).__init__()
        self.init_error_handler()
        self.load_plugin_widgets()
        self.load_plugin_factories()

    # -------------------------------------------------------------------------
    # Abstract API Implementation
    # -------------------------------------------------------------------------
    def start(self):
        """ Start the application's main event loop
        using either twisted or tornado.
        
        """
        if self.dev:
            self.start_dev_session()

        self.loop.start()

    def stop(self):
        """ Stop the application's main event loop.

        """
        self.loop.stop()

    def deferred_call(self, callback, *args, **kwargs):
        """ Invoke a callable on the next cycle of the main event loop
        thread.

        Parameters
        ----------
        callback : callable
            The callable object to execute at some point in the future.

        *args, **kwargs
            Any additional positional and keyword arguments to pass to
            the callback.

        """
        return self.loop.deferred_call(callback, *args, **kwargs)

    def timed_call(self, ms, callback, *args, **kwargs):
        """ Invoke a callable on the main event loop thread at a
        specified time in the future.

        Parameters
        ----------
        ms : int
            The time to delay, in milliseconds, before executing the
            callable.

        callback : callable
            The callable object to execute at some point in the future.

        *args, **kwargs
            Any additional positional and keyword arguments to pass to
            the callback.

        """
        return self.loop.timed_call(ms, callback, *args, **kwargs)

    def is_main_thread(self):
        """ Indicates whether the caller is on the main gui thread.

        Returns
        -------
        result : bool
            True if called from the main gui thread. False otherwise.

        """
        return False

    # -------------------------------------------------------------------------
    # App API Implementation
    # -------------------------------------------------------------------------
    def has_permission(self, permission):
        """ Return a future that resolves with the result of the permission """
        raise NotImplementedError

    def request_permissions(self, permissions):
        """ Return a future that resolves with the result of the 
        permission request
        
        """
        raise NotImplementedError

    # -------------------------------------------------------------------------
    # EventLoop API Implementation
    # -------------------------------------------------------------------------
    def init_error_handler(self):
        """ When an error occurs, set the error view in the App

        """
        self.loop.set_error_handler(self.handle_error)

    def create_future(self):
        """ Create a future object using the EventLoop implementation """
        return self.loop.create_future()

    def add_done_callback(self, future, callback):
        """ Add a callback on a future object put here so it can be
        implemented with different event loops.

        Parameters
        -----------
            future: Future or Deferred
                Future implementation for the current EventLoop
                
            callback: callable
                Callback to invoke when the future is done
                
        """
        if future is None:
            raise bridge.BridgeReferenceError(
                "Tried to add a callback to a nonexistent Future. "
                "Make sure you pass the `returns` argument to your JavaMethod")
        return self.loop.add_done_callback(future, callback)

    def set_future_result(self, future, result):
        """ Set the result of the future

        Parameters
        -----------
            future: Future or Deferred
                Future implementation for the current EventLoop
                
            result: object
                Result to set
        """
        return self.loop.set_future_result(future, result)

    # -------------------------------------------------------------------------
    # Bridge API Implementation
    # -------------------------------------------------------------------------
    def show_view(self):
        """ Show the current `app.view`. This will fade out the previous
        with the new view.
            
        """
        raise NotImplementedError

    def get_view(self):
        """ Get the root view to display. Make sure it is
        properly initialized.
        
        """
        view = self.view
        if not view.is_initialized:
            view.initialize()
        if not view.proxy_is_active:
            view.activate_proxy()
        return view.proxy.widget

    def show_error(self, msg):
        """ Show the error view with the given message on the UI.

        """
        self.send_event(bridge.Command.ERROR, msg)

    def send_event(self, name, *args, **kwargs):
        """ Send an event to the native handler. This call is queued and 
        batched.

        Parameters
        ----------
        name : str
            The event name to be processed by MainActivity.processMessages.
        *args: args
            The arguments required by the event.
        **kwargs: kwargs
            Options for sending. These are:

            now: boolean
                Send the event now

        """
        self._bridge_pending += 1
        self._bridge_queue.append((name, args))

        if kwargs.get('now'):
            self._bridge_send(now=True)
        else:
            self.timed_call(self._bridge_timeout, self._bridge_send)

    def force_update(self):
        """ Force an update now. """
        #: So we don't get out of order
        self._bridge_pending += 1
        self._bridge_send(now=True)

    def _bridge_send(self, now=False):
        """  Send the events over the bridge to be processed by the native
        handler.

        Parameters
        ----------
        now: boolean
            Send all pending events now instead of waiting for deferred calls 
            to finish. Use this when you want to update the screen

        """
        self._bridge_pending -= 1
        if self._bridge_queue and (self._bridge_pending == 0 or now):
            if self.debug:
                print("======== Py --> Native ======")
                for event in self._bridge_queue:
                    print(event)
                print("===========================")

            self.dispatch_events(bridge.dumps(self._bridge_queue))
            self._bridge_queue = []

    def dispatch_events(self, data):
        """ Send events to the bridge using the system specific implementation.
        
        """
        raise NotImplementedError

    def process_events(self, data):
        """ The native implementation must use this call to """
        events = bridge.loads(data)
        if self.debug:
            print("======== Py <-- Native ======")
            for event in events:
                print(event)
            print("===========================")
        for event in events:
            if event[0] == 'event':
                self.handle_event(event)

    def handle_event(self, event):
        """ When we get an 'event' type from the bridge
        handle it by invoking the handler and if needed
        sending back the result.
        
        """
        result_id, ptr, method, args = event[1]
        obj = None
        result = None
        try:
            obj, handler = bridge.get_handler(ptr, method)
            result = handler(*[v for t, v in args])
        except bridge.BridgeReferenceError as e:
            #: Log the event, don't blow up here
            msg = "Error processing event: {} - {}".format(
                  event, e).encode("utf-8")
            print(msg)
            self.show_error(msg)
        except:
            #: Log the event, blow up in user's face
            msg = "Error processing event: {} - {}".format(
                  event, traceback.format_exc()).encode("utf-8")
            print(msg)
            self.show_error(msg)
            raise
        finally:
            if result_id:
                if hasattr(obj, '__nativeclass__'):
                    sig = getattr(type(obj), method).__returns__
                else:
                    sig = type(result).__name__

                self.send_event(
                    bridge.Command.RESULT,  #: method
                    result_id,
                    bridge.msgpack_encoder(sig, result)  #: args
                )

    def handle_error(self, callback):
        """ Called when an error occurs in an event loop callback.
        By default, sets the error view.
        
        """
        self.loop.log_error(callback)
        msg = "\n".join([
            "Exception in callback %r"%callback,
            traceback.format_exc()
        ])
        self.show_error(msg.encode('utf-8'))

    # -------------------------------------------------------------------------
    # AppEventListener API Implementation
    # -------------------------------------------------------------------------
    def on_events(self, data):
        """ Called when the bridge sends an event. For instance the return 
        result of a method call or a callback from a widget event.
        
        """
        #: Pass to event loop thread
        self.deferred_call(self.process_events, data)

    def on_pause(self):
        """ Called when the app is paused.
        """
        pass

    def on_resume(self):
        """ Called when the app is resumed.
        """
        pass

    def on_stop(self):
        """ Called when the app is stopped.
        """
        #: Called from thread, make sure the correct thread detaches
        pass

    def on_destroy(self):
        """ Called when the app is destroyed.
        """
        self.deferred_call(self.stop)

    # -------------------------------------------------------------------------
    # Dev Session Implementation
    # -------------------------------------------------------------------------
    def start_dev_session(self):
        """ Start a client that attempts to connect to the dev server
        running on the host `app.dev`
        
        """
        try:
            from .dev import DevServerSession
            session = DevServerSession.initialize(host=self.dev)
            session.start()

            #: Save a reference
            self._dev_session = session
        except:
            self.show_error(traceback.format_exc())

    # -------------------------------------------------------------------------
    # Plugin implementation
    # -------------------------------------------------------------------------
    def get_plugins(self, group):
        """ Was going to use entry points but that requires a ton of stuff 
        which will be extremely slow.
        
        """
        return self.plugins.get(group, [])

    def load_plugin_widgets(self):
        """ Pull widgets added via plugins using the `enaml_native_widgets` 
        entry point. The entry point function must return a dictionary of 
        Widget declarations to add to the core api.

        def install():
            from charts.widgets.chart_view import BarChart, LineChart
            return {
                'BarChart': BarChart,
                'LineCart': LineChart,
            }

        """
        from enamlnative.widgets import api
        for plugin in self.get_plugins(group='enaml_native_widgets'):
            get_widgets = plugin.load()
            for name, widget in iter(get_widgets()):
                #: Update the core api with these widgets
                setattr(api, name, widget)

    def load_plugin_factories(self):
        """ Pull widgets added via plugins using the 
        `enaml_native_ios_factories` or `enaml_native_android_factories` 
        entry points. The entry point function must return a dictionary of 
        Widget declarations to add to the factories for this platform.

        def install():
            return {
                'MyWidget':my_widget_factory,
                # etc...
            }

        """
        raise NotImplementedError