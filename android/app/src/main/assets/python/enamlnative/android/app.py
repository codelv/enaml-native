'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
import jnius
from atom.api import List, Float, Value, Dict, Int, Typed, Bool
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


class AndroidApplication(Application):
    """ An Android implementation of an Enaml application.

    A AndroidApplication uses the native Android widget toolkit to implement an Enaml UI that
    runs in the local process.

    """
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


    loop = Value()

    def _default_loop(self):
        #from twisted.internet import reactor
        from tornado.ioloop import IOLoop
        return IOLoop.current()

    #: Save reference to the event listener
    listener = Typed(AppEventListener)

    #: Events to send to Java
    _bridge_queue = List()

    #: Delay to wait before sending events (in ms)
    _bridge_timeout = Int(10)

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
        #reactor.run()

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
        #reactor.stop()
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
        #reactor.callWhenRunning(callback, *args, **kwargs)

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
        #reactor.callLater(ms/1000.0, callback, *args, **kwargs)

    def is_main_thread(self):
        """ Indicates whether the caller is on the main gui thread.

        Returns
        -------
        result : bool
            True if called from the main gui thread. False otherwise.

        """
        return False

    # --------------------------------------------------------------------------
    # AppEventListener API Implementation
    # --------------------------------------------------------------------------
    def on_events(self, data):
        #: Pass to event loop thread
        self.deferred_call(bridge.loads, data)
        #reactor.callFromThread(bridge.loads, data)

    def on_pause(self):
        pass

    def on_resume(self):
        pass

    def on_stop(self):
        pass