# -*- coding: utf-8 -*-
"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

@author jrm

"""
import json
import traceback
from asyncio import Future
from time import time
from typing import Optional, Union
from inspect import iscoroutinefunction
from atom.api import Atom, Bool, Dict, Float, Event, Instance, Int, List, Str, Value
from enaml.application import Application
from tornado.ioloop import IOLoop
from enamlnative.core.bridge import (
    BridgeFuture,
    Command,
    loads,
    dumps,
    encode,
    get_handler,
    BridgeReferenceError,
    BridgeException,
)
from enamlnative.widgets.activity import Activity


class Plugin(Atom):
    """Simplified way to load a plugin from an entry_point line.
    The enaml-native and p4a build process removes pkg_resources
    and all package related metadata this simply imports from an
    entry point string in the format "package.path.module:attr"

    """

    name = Str()
    source = Str()

    def load(self):
        """Load the object defined by the plugin entry point"""
        print(f"[DEBUG] Loading plugin {self.name} from {self.source}")
        import pydoc

        path, attr = self.source.split(":")
        module = pydoc.locate(path)
        return getattr(module, attr)


class BridgedApplication(Application):
    """An abstract implementation of an Enaml application.

    This serves as a base class for both Android and iOS applications and
    provides support for the python event loop, the development server
    and the bridge.

    """

    __id__ = Int(-1)

    #: View to display within the activity
    activity = Instance(Activity)

    #: If true, debug bridge statements
    debug = Bool()

    #: Use dev server
    dev = Str()
    _dev_session = Value()

    #: Event loop
    loop = Instance(IOLoop, factory=IOLoop.current)

    #: Events to send to the bridge
    _bridge_queue = List()

    #: Time last sent
    _bridge_max_delay = Float(0.005)

    #: Time last sent
    _bridge_last_scheduled = Float()

    #: Entry points to load plugins
    plugins = Dict()

    #: Event triggered when an error occurs
    error_occurred = Event(Exception)

    # -------------------------------------------------------------------------
    # Defaults
    # -------------------------------------------------------------------------
    def _default_plugins(self):
        """Get entry points to load any plugins installed.
        The build process should create an "entry_points.json" file
        with all of the data from the installed entry points.

        """
        plugins = {}
        try:
            with open("entry_points.json") as f:
                entry_points = json.load(f)
            for ep, obj in entry_points.items():
                plugins[ep] = []
                for name, src in obj.items():
                    plugins[ep].append(Plugin(name=name, source=src))
        except Exception as e:
            print(f"Failed to load entry points {e}")
        return plugins

    # -------------------------------------------------------------------------
    # BridgedApplication Constructor
    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Initialize the event loop error handler.  Subclasses must properly
        initialize the proxy resolver.

        """
        super().__init__(*args, **kwargs)
        if self.dev:
            self.start_dev_session()
        self.init_error_handler()
        self.load_plugin_widgets()
        self.load_plugin_factories()

    # -------------------------------------------------------------------------
    # Abstract API Implementation
    # -------------------------------------------------------------------------
    def start(self):
        """Start the application event loop"""
        #: Schedule a load view if given and remote debugging is not active
        #: the remote debugging init call this after dev connection is ready
        if self.dev != "remote":
            self.deferred_call(self.activity.start)
        self.loop.start()

    def stop(self):
        """Stop the application's main event loop."""
        self.loop.stop()

    def deferred_call(self, callback, *args, **kwargs):
        """Invoke a callable on the next cycle of the main event loop
        thread.

        Parameters
        ----------
        callback : callable
            The callable object to execute at some point in the future.

        *args, **kwargs
            Any additional positional and keyword arguments to pass to
            the callback.

        """
        self.loop.add_callback(callback, *args, **kwargs)

    def timed_call(self, ms, callback, *args, **kwargs):
        """Invoke a callable on the main event loop thread at a
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
        self.loop.call_later(ms / 1000, callback, *args, **kwargs)

    def is_main_thread(self):
        """Indicates whether the caller is on the main gui thread.

        Returns
        -------
        result : bool
            True if called from the main gui thread. False otherwise.

        """
        return False

    # -------------------------------------------------------------------------
    # App API Implementation
    # -------------------------------------------------------------------------
    async def has_permission(self, permission):
        """Return a future that resolves with the result of the permission"""
        raise NotImplementedError

    async def request_permissions(self, permissions):
        """Return a future that resolves with the result of the
        permission request

        """
        raise NotImplementedError

    # -------------------------------------------------------------------------
    # EventLoop API Implementation
    # -------------------------------------------------------------------------
    def init_error_handler(self):
        """When an error occurs, set the error view in the App"""
        # HACK: Reassign the discard method to show errors
        self.loop._discard_future_result = self._on_future_result

    def create_future(self, return_type: Optional[type] = None) -> BridgeFuture:
        """Create a future object using the EventLoop implementation"""
        return BridgeFuture(return_type)

    # -------------------------------------------------------------------------
    # Bridge API Implementation
    # -------------------------------------------------------------------------
    def show_error(self, msg: Union[bytes, str]):
        """Show the error view with the given message on the UI."""
        self.send_event(Command.ERROR, msg)

    def send_event(self, name: str, *args, **kwargs):
        """Send an event to the native handler. This call is queued and
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
        n = len(self._bridge_queue)

        # Add to queue
        self._bridge_queue.append((name, args))

        if n == 0:
            # First event, send at next available time
            self._bridge_last_scheduled = time()
            self.deferred_call(self._bridge_send)
            return
        elif kwargs.get("now"):
            self._bridge_send(now=True)
            return

        # If it's been over 5 ms since we last scheduled, run now
        dt = time() - self._bridge_last_scheduled
        if dt > self._bridge_max_delay:
            self._bridge_send(now=True)

    def force_update(self):
        """Force an update now."""
        #: So we don't get out of order
        self._bridge_send(now=True)

    def _on_future_result(self, future: Future) -> None:
        """Avoid unhandled-exception warnings from spawned coroutines."""
        try:
            future.result()
        except Exception as e:
            self.handle_error(future, e)

    def _bridge_send(self, now: bool = False):
        """Send the events over the bridge to be processed by the native
        handler.

        Parameters
        ----------
        now: boolean
            Send all pending events now instead of waiting for deferred calls
            to finish. Use this when you want to update the screen

        """
        if len(self._bridge_queue):
            if self.debug:
                print("======== Py --> Native ======")
                for i, event in enumerate(self._bridge_queue):
                    print(f"{i}: {event}")
                print("===========================")
            self.dispatch_events(dumps(self._bridge_queue))
            self._bridge_queue = []

    def dispatch_events(self, data):
        """Send events to the bridge using the system specific implementation."""
        raise NotImplementedError

    async def process_events(self, data: str):
        """The native implementation must use this call to"""
        events = loads(data)
        if self.debug:
            print("======== Py <-- Native ======")
            for event in events:
                print(event)
            print("===========================")
        for t, event in events:
            if t == "event":
                await self.handle_event(*event)

    async def handle_event(self, result_id: int, ptr: int, method: str, args: list):
        """When we get an 'event' type from the bridge
        handle it by invoking the handler and if needed
        sending back the result.

        """
        obj = None
        result = None
        try:
            obj, handler = get_handler(ptr, method)
            if method == "set_exception":
                # Remote call failed
                obj.set_exception(BridgeException(args))
            elif iscoroutinefunction(handler):
                result = await handler(*(v for t, v in args))
            else:
                result = handler(*(v for t, v in args))
        except BridgeReferenceError as e:
            #: Log the event, don't blow up here
            event = (result_id, ptr, method, args)
            print(f"Error processing event: {event} - {e}")
            self.error_occurred(e)  # type: ignore
            # self.show_error(msg)
        except Exception as e:
            #: Log the event, blow up in user's face
            self.error_occurred(e)  # type: ignore
            err = traceback.format_exc()
            event = (result_id, ptr, method, args)
            msg = f"Error processing event: {event} - {err}"
            print(msg)
            self.show_error(msg)
            raise
        finally:
            if result_id:
                if hasattr(obj, "__nativeclass__"):
                    sig, ret_type = getattr(obj.__class__, method).__returns__
                else:
                    sig = result.__class__.__name__

                self.send_event(
                    Command.RESULT,  #: method
                    result_id,
                    (sig, encode(result)),  #: args
                    now=True,
                )

    def handle_error(self, callback, exc: Exception):
        """Called when an error occurs in an event loop callback.
        By default, sets the error view.

        """
        self.error_occurred(exc)  # type: ignore
        msg = f"Exception in callback {callback}: {traceback.format_exc()}"
        self.show_error(msg.encode("utf-8"))

    # -------------------------------------------------------------------------
    # AppEventListener API Implementation
    # -------------------------------------------------------------------------
    def on_events(self, data):
        """Called when the bridge sends an event. For instance the return
        result of a method call or a callback from a widget event.

        """
        #: Pass to event loop thread
        self.deferred_call(self.process_events, data)

    def on_pause(self):
        """Called when the app is paused."""
        self.activity.paused()

    def on_resume(self):
        """Called when the app is resumed."""
        self.activity.resumed()

    def on_stop(self):
        """Called when the app is stopped."""
        #: Called from thread, make sure the correct thread detaches
        self.activity.stopped()

    def on_destroy(self):
        """Called when the app is destroyed."""
        self.deferred_call(self.stop)

    # -------------------------------------------------------------------------
    # Dev Session Implementation
    # -------------------------------------------------------------------------
    def start_dev_session(self):
        """Start a client that attempts to connect to the dev server
        running on the host `app.dev`

        """
        try:
            from .dev import DevServerSession

            session = DevServerSession.initialize(host=self.dev)
            session.start()

            #: Save a reference
            self._dev_session = session
        except Exception:
            self.show_error(traceback.format_exc())

    # -------------------------------------------------------------------------
    # Plugin implementation
    # -------------------------------------------------------------------------
    def get_plugins(self, group: str) -> list[Plugin]:
        """Was going to use entry points but that requires a ton of stuff
        which will be extremely slow.

        """
        return self.plugins.get(group, [])

    def load_plugin_widgets(self):
        """Pull widgets added via plugins using the `enaml_native_widgets`
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

        for plugin in self.get_plugins(group="enaml_native_widgets"):
            get_widgets = plugin.load()
            for name, widget in iter(get_widgets()):
                #: Update the core api with these widgets
                setattr(api, name, widget)

    def load_plugin_factories(self):
        """Pull widgets added via plugins using the
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
