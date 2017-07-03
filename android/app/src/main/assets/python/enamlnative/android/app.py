'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
import jnius
import traceback
from atom.api import Atom, List, Float, Value, Dict, Int, Unicode, Typed, Bool
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


class Activity(bridge.JavaBridgeObject):
    """ Access to the activity over the bridge """
    __javaclass__ = Unicode('android.support.v7.app.AppCompatActivity')
    __id__ = Int(-1)

    def __init__(self):
        Atom.__init__(self)

    setActionBar = bridge.JavaMethod('android.widget.Toolbar')
    setSupportActionBar = bridge.JavaMethod('android.support.v7.widget.Toolbar')
    setContentView = bridge.JavaMethod('android.view.View')


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
    loop = Value()

    def _default_loop(self):
        #from twisted.internet import reactor
        #return reactor
        #from enamlnative.core.ioloop import IOLoop
        from tornado.ioloop import IOLoop
        return IOLoop.current()

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
        view = self.get_view()
        self.send_event('showView')

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
        self.loop.add_callback(callback, *args, **kwargs)
        #self.loop.callWhenRunning(callback, *args, **kwargs)

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
        self.loop.call_later(ms/1000.0, callback, *args, **kwargs)
        #self.loop.callLater(ms/1000.0, callback, *args, **kwargs)

    def is_main_thread(self):
        """ Indicates whether the caller is on the main gui thread.

        Returns
        -------
        result : bool
            True if called from the main gui thread. False otherwise.

        """
        return False

    def create_future(self):
        from tornado.concurrent import Future
        return Future()

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
        try:
            obj, handler = bridge.get_handler(ptr, method)
            result = handler(*[v for t, v in args])
            if result_id:
                if hasattr(obj, '__javaclass__'):
                    sig = getattr(type(obj), method).__returns__
                else:
                    sig = type(result).__name__

                self.send_event(
                    'setResult',  #: method
                    result_id,
                    bridge.msgpack_encoder(sig, result)  #: args
                )
        except:
            traceback.print_exc()

    # --------------------------------------------------------------------------
    # AppEventListener API Implementation
    # --------------------------------------------------------------------------
    def on_events(self, data):
        #: Pass to event loop thread
        self.deferred_call(self.process_events, data)

    def on_pause(self):
        pass

    def on_resume(self):
        pass

    def on_stop(self):
        pass
        #self.deferred_call(jnius.detach)