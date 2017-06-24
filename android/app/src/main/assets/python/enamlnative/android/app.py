'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''

import jnius
import msgpack
from atom.api import List, Value, Dict, Int, Typed
from enaml.application import Application, ProxyResolver
from twisted.internet import reactor
from . import factories

from .bridge import msgpack_encoder


class AppEventListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['com/enaml/MainActivity$AppEventListener']
    __javacontext__ = 'app'

    def __init__(self, handler):
        self.__handler__ = handler
        super(AppEventListener, self).__init__()

    @jnius.java_method('([B)V')
    def onEvents(self, data):
        self.__handler__.on_events(data)

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

    #: Save reference to the event listener
    listener = Typed(AppEventListener)

    #: Events to send to Java
    _bridge_queue = List()

    #: Delay to wait before sending events
    _bridge_timeout = Int(100)

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
        #assert view, "View does not exist!"
        #activity.setView(view)
        view = self.get_view()
        self.send_event('showView')
        reactor.run()

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
        reactor.stop()

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
            print self._bridge_queue
            self.activity.processEvents(
                msgpack.dumps(self._bridge_queue)
                              #object_hook=msgpack_encoder)
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
        reactor.callWhenRunning(callback, *args, **kwargs)

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
        reactor.callLater(ms/1000.0, callback, *args, **kwargs)

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
        pass

    def on_pause(self):
        pass

    def on_resume(self):
        pass

    def on_stop(self):
        pass

