'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
import jnius
import traceback
import unicodedata #: Required by tornado for encodings
from atom.api import Atom, Callable, List, Float, Instance, Value, Dict, Int, Unicode, Typed, Bool
from enaml.application import Application, ProxyResolver
from . import factories
from . import bridge
from .android_activity import Activity
from .event_loop import EventLoop


class AppEventListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['com/enaml/MainActivity$AppEventListener']
    __javacontext__ = 'app'

    def __init__(self, handler):
        self.__handler__ = handler
        super(AppEventListener, self).__init__()

    @jnius.java_method('([B)V')
    def onEvents(self, data):
        self.__handler__.on_events(bytearray(data))

    @jnius.java_method('()V')
    def onResume(self):
        self.__handler__.on_resume()

    @jnius.java_method('()V')
    def onPause(self):
        self.__handler__.on_pause()

    @jnius.java_method('()V')
    def onStop(self):
        self.__handler__.on_stop()

    @jnius.java_method('()V')
    def onDestroy(self):
        self.__handler__.on_destroy()


class AndroidApplication(Application):
    """ An Android implementation of an Enaml application.

    A AndroidApplication uses the native Android widget toolkit to implement an Enaml UI that
    runs in the local process.

    """

    #: Attributes so it can be seralized over the bridge as a reference
    __javaclass__ = Unicode('android.content.Context')
    __id__ = Int(-1)

    #: Bridge widget
    widget = Typed(Activity)

    #: Android Activity
    activity = Value()

    #: Keep screen on by setting the WindowManager flag
    keep_screen_on = Bool()

    #: View to display within the activity
    view = Value()

    #: If true, debug bridge statements
    debug = Bool()

    #: Use dev server
    dev = Unicode()
    _dev_client = Value()
    reload_view = Callable()

    #: Pixel density of the device
    #: Loaded immediately as this is used often.
    dp = Float()

    #: Event loop
    loop = Instance(EventLoop)

    #: Save reference to the event listener
    listener = Typed(AppEventListener)

    #: Events to send to Java
    _bridge_queue = List()

    #: Delay to wait before sending events (in ms)
    _bridge_timeout = Int(3)

    #: Count of pending send calls
    _bridge_pending = Int(0)

    # --------------------------------------------------------------------------
    # Defaults
    # --------------------------------------------------------------------------

    def _default_widget(self):
        """ Return a bridge object reference to the MainActivity """
        return Activity(__id__=-1)

    def _default_loop(self):
        """ Get the event loop based on what libraries are available. """
        return EventLoop.default()

    def _default_dp(self):
        return self.activity.getResources().getDisplayMetrics().density

    # --------------------------------------------------------------------------
    # AndroidApplication Constructor
    # --------------------------------------------------------------------------
    def __init__(self, activity):
        """ Initialize a AndroidApplication. Uses jnius to retrieve
            an instance of the activity.
        """
        super(AndroidApplication, self).__init__()
        self.activity = jnius.autoclass(activity).mActivity
        self.resolver = ProxyResolver(factories=factories.ANDROID_FACTORIES)
        self.init_error_handler()

    # --------------------------------------------------------------------------
    # Abstract API Implementation
    # --------------------------------------------------------------------------
    def start(self):
        """ Start the application's main event loop. Bind the Android app event
            listener using jnius.
        """
        activity = self.activity

        #: Hook for JNI using jnius
        self.listener = AppEventListener(self)
        activity.setAppEventListener(self.listener)

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

    # --------------------------------------------------------------------------
    # EventLoop API Implementation
    # --------------------------------------------------------------------------
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
            raise bridge.JavaReferenceError(
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

    # --------------------------------------------------------------------------
    # Bridge API Implementation
    # --------------------------------------------------------------------------
    def show_view(self):
        """ Show the current `app.view`. This will fade out the previous
            with the new view.
        """
        self.widget.setView(self.get_view())

    def show_error(self, msg):
        """ Show the error view with the given message on the UI.

        """
        self.send_event(bridge.Command.ERROR, msg)

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

    def send_event(self, name, *args, **kwargs):
        """ Send an event to Java.
            This call is queued and batched.

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
        """  Send the events over the bridge to be processed by Java

        Parameters
        ----------
        now: boolean
            Send all pending events now instead of waiting for deferred calls to finish.
            Use this when you want to update the screen

        """
        self._bridge_pending -= 1
        if self._bridge_queue and (self._bridge_pending == 0 or now):
            if self.debug:
                print("======== Py --> Java ======")
                for event in self._bridge_queue:
                    print(event)
                print("===========================")

            self.activity.processEvents(
                bridge.dumps(self._bridge_queue)
            )
            self._bridge_queue = []

    def process_events(self, data):
        events = bridge.loads(data)
        if self.debug:
            print("======== Py <-- Java ======")
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
        except bridge.JavaReferenceError as e:
            #: Log the event, don't blow up here
            print("Error processing event: {} - {}".format(event, e))
        except:
            #: Log the event, blow up in user's face
            print("Error processing event: {} - {}".format(event, traceback.format_exc()))
            raise
        finally:
            if result_id:
                if hasattr(obj, '__javaclass__'):
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
        self.send_event(bridge.Command.ERROR, msg)

    # --------------------------------------------------------------------------
    # AppEventListener API Implementation
    # --------------------------------------------------------------------------
    def on_events(self, data):
        """ Called when the bridge sends an event. For instance the return result
            of a method call or a callback from a widget event.
        """
        #: Pass to event loop thread
        self.deferred_call(self.process_events, data)

    def on_pause(self):
        """ Called when the app activity is paused.
        """
        # self.loop.stop()
        pass

    def on_resume(self):
        """ Called when the app activity is resumed.
        """
        #self.loop.start()
        pass

    def on_stop(self):
        """ Called when the app activity is stopped.
        """
        #: Called from thread, make sure the correct thread detaches
        pass

    def on_destroy(self):
        """ Called when the app activity is destroyed.
        """
        self.deferred_call(self.stop)

    # --------------------------------------------------------------------------
    # Android utilities API Implementation
    # --------------------------------------------------------------------------
    def _observe_keep_screen_on(self, change):
        """ Sets or clears the flag to keep the screen on. """
        def set_screen_on(window):
            from .android_window import Window
            window = Window(__id__=window)
            if self.keep_screen_on:
                window.addFlags(Window.FLAG_KEEP_SCREEN_ON)
            else:
                window.clearFlags(Window.FLAG_KEEP_SCREEN_ON)

        self.widget.getWindow().then(set_screen_on)


    # --------------------------------------------------------------------------
    # Dev Session Implementation
    # --------------------------------------------------------------------------
    def start_dev_session(self):
        """ Start a client that attempts to connect to the dev server
            running on the host `app.dev`
        """
        from .dev import DevServerClient
        client = DevServerClient.initialize(host=self.dev)
        client.start()

        #: Save a reference
        self._dev_client = client

    def reload(self):
        """ Called when the dev server wants to reload the view. """
        if self.reload_view is None:
            print("Warning: Reloading the view is not implemented. "
                  "Please set `app.reload_view` to support this.")
            return
        if self.view is not None:
            try:
                self.view.destroy()
            except:
                pass
        self.view = None
        self.deferred_call(self.reload_view, self)
