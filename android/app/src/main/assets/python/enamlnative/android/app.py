'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
import jnius
import traceback
from atom.api import Atom, List, Float, Instance, Value, Dict, Int, Unicode, Typed, Bool
from enaml.application import Application, ProxyResolver
from . import factories
from . import bridge


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


class Activity(bridge.JavaBridgeObject):
    """ Access to the activity over the bridge """
    __javaclass__ = Unicode('android.support.v7.app.AppCompatActivity')
    __id__ = Int(-1) #: ID of -1 is a special reference on the bridge to the activity.

    def __init__(self):
        """ This is only a reference, no object needs created by the bridge """
        Atom.__init__(self)

    setActionBar = bridge.JavaMethod('android.widget.Toolbar')
    setSupportActionBar = bridge.JavaMethod('android.support.v7.widget.Toolbar')
    setContentView = bridge.JavaMethod('android.view.View')


class EventLoop(Atom):
    """ Event loop delegation api

    """

    loop = Value()

    def start(self):
        self.loop.start()

    def stop(self):
        self.loop.stop()

    def deferred_call(self, callback, *args, **kwargs):
        raise NotImplementedError

    def timed_call(self, ms, callback, *args, **kwargs):
        raise NotImplementedError

    def create_future(self):
        raise NotImplementedError

    def set_error_handler(self, handler):
        raise NotImplementedError

    def add_done_callback(self, future, callback):
        raise NotImplementedError

    def set_future_result(self, future, result):
        raise NotImplementedError


class TornadoEventLoop(EventLoop):
    """ Eventloop using tornado's ioloop """

    def _default_loop(self):
        from tornado.ioloop import IOLoop
        return IOLoop.current()

    def deferred_call(self, callback, *args, **kwargs):
        return self.loop.add_callback(callback, *args, **kwargs)

    def timed_call(self, ms, callback, *args, **kwargs):
        return self.loop.call_later(ms/1000.0, callback, *args, **kwargs)

    def set_error_handler(self, handler):
        self.loop.handle_callback_exception = handler

    def create_future(self):
        from tornado.concurrent import Future
        return Future()

    def add_done_callback(self, future, callback):
        return future.add_done_callback(callback)

    def set_future_result(self, future, result):
        future.result(result)


class TwistedEventLoop(EventLoop):
    """ Eventloop using twisted's reactor """

    def _default_loop(self):
        from twisted.internet import reactor
        return reactor

    def start(self):
        self.loop.run()

    def deferred_call(self, callback, *args, **kwargs):
        return self.loop.callWhenRunning(callback, *args, **kwargs)

    def timed_call(self, ms, callback, *args, **kwargs):
        return self.loop.callLater(ms/1000.0, callback, *args, **kwargs)

    def set_error_handler(self, handler):
        #self.loop.handle_callback_exception = handler
        raise NotImplementedError

    def create_future(self):
        from twisted.internet.defer import Deferred
        return Deferred()

    def add_done_callback(self, future, callback):
        future.addCallback(callback)

    def set_future_result(self, future, result):
        future.callback(result)


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

    def _default_widget(self):
        return Activity()

    #: Android Activity
    activity = Value(object)

    #: View to display within the activity
    view = Value(object)

    #: If true, debug bridge statements
    debug = Bool(False)

    #:
    dp = Float()

    def _default_dp(self):
        return self.activity.getResources().getDisplayMetrics().density

    #: Event loop
    loop = Instance(EventLoop)

    def _default_loop(self):
        return TornadoEventLoop()

    #: Save reference to the event listener
    listener = Typed(AppEventListener)

    #: Events to send to Java
    _bridge_queue = List()

    #: Delay to wait before sending events (in ms)
    _bridge_timeout = Int(3)

    #: Count of pending send calls
    _bridge_pending = Int(0)

    def __init__(self, activity):
        """ Initialize a AndroidApplication

        """
        super(AndroidApplication, self).__init__()
        self.activity = activity
        self.resolver = ProxyResolver(factories=factories.ANDROID_FACTORIES)
        self.init_error_handler()

    # --------------------------------------------------------------------------
    # Abstract API Implementation
    # --------------------------------------------------------------------------
    def start(self):
        """ Start the application's main event loop.

        """
        activity = self.activity
        self.listener = AppEventListener(self)
        activity.setAppEventListener(self.listener)
        self.loop.start()
        #self.loop.run()

    def show_view(self):
        """ Show the view. It uses the first view created.

        """
        view = self.get_view()
        self.send_event(bridge.Command.SHOW)

    def show_error(self, msg):
        """ Show the error view with the given message

        """
        self.send_event(bridge.Command.ERROR, msg)

    def get_view(self):
        """ Prepare the view

        """
        view = self.view
        if not view.is_initialized:
            view.initialize()
        if not view.proxy_is_active:
            view.activate_proxy()
        return view.proxy.widget

    def stop(self):
        """ Stop the application's main event loop.

        """
        self.loop.stop()

    def send_event(self, name, *args):
        """ Send an event to Java.
            This call is queued and batched.

       Parameters
        ----------
        name : str
            The event name to be processed by MainActivity.processMessages.
        *args: args
            The arguments required by the event.

        """
        self._bridge_pending += 1
        self._bridge_queue.append((name, args))
        self.timed_call(self._bridge_timeout, self._bridge_send)

    def _bridge_send(self):
        """  Send the events over the bridge to be processed by Java

        """
        self._bridge_pending -= 1
        if self._bridge_pending == 0:
            if self.debug:
                print("======== Py --> Java ======")
                for event in self._bridge_queue:
                    print(event)
                print("===========================")

            self.activity.processEvents(
                bridge.dumps(self._bridge_queue)
            )
            self._bridge_queue = []

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
        except:
            #: Log the event
            print("Error processing event: {}".format(event))
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
        from tornado.log import app_log
        app_log.error("Exception in callback %r", callback, exc_info=True)
        msg = "\n".join([
            "Exception in callback %r"%callback,
            traceback.format_exc()
        ])
        self.send_event(bridge.Command.ERROR, msg)

    # --------------------------------------------------------------------------
    # AppEventListener API Implementation
    # --------------------------------------------------------------------------
    def on_events(self, data):
        #: Pass to event loop thread
        self.deferred_call(self.process_events, data)

    def on_pause(self):
        # self.loop.stop()
        pass

    def on_resume(self):
        #self.loop.start()
        pass

    def on_stop(self):
        #: Called from thread, make sure the correct thread detaches
        pass

    def on_destroy(self):
        self.deferred_call(self.stop)