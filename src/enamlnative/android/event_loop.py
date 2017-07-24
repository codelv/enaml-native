'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
from atom.api import Atom, Value
from functools import partial
from . import bridge

class EventLoop(Atom):
    """ Event loop delegation api

    """

    #: Actual event loop object
    loop = Value()

    @classmethod
    def default(cls):
        """ Get the first available event loop implementation
            based on which packages are installed."""
        for impl in [
                TornadoEventLoop,
                TwistedEventLoop
                ]:
            if impl.available():
                return impl()
        raise RuntimeError("No event loop implementation is available. Install tornado or twisted.")

    @classmethod
    def available(cls):
        """ Test if the event loop implementation is available.
        Return
        ---------
            bool: The event loop can be used.
        """
        raise NotImplementedError

    def start(self):
        self.loop.start()

    def stop(self):
        self.loop.stop()

    def deferred_call(self, callback, *args, **kwargs):
        """ Schedule the given callback to be invoked at the next available time. """
        raise NotImplementedError

    def timed_call(self, ms, callback, *args, **kwargs):
        """ Schedule the given callback to be invoked at a time `ms` later. """
        raise NotImplementedError

    def create_future(self):
        """ Create a future instance for this event loop.

            The future returned MUST have a method named `then` that
            takes adds callback that should be invoked when the future is complete
            and returns the future object.

            Likewise the future must be tagged with an id using
            `bridge.tag_object_with_id(obj)`

        """
        raise NotImplementedError

    def set_error_handler(self, handler):
        """ Set the error handler method to be the given handler. """
        raise NotImplementedError

    def add_done_callback(self, future, callback):
        """ Add a callback will be triggered when the callback completes. """
        raise NotImplementedError

    def set_future_result(self, future, result):
        """ Set the result of a Future to trigger any attached callbacks. """
        raise NotImplementedError

    def log_error(self, callback):
        """ Log the error that occurred when running the given callback. """
        raise NotImplementedError


class TornadoEventLoop(EventLoop):
    """ Eventloop using tornado's ioloop """
    @classmethod
    def available(cls):
        try:
            import tornado
            return True
        except ImportError:
            return False

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
        f = Future()
        bridge.tag_object_with_id(f)

        #: Add then method so you can easily chain callbacks
        #: Tornado returns the future not the result to callbacks
        def then(f, callback):
            def done(f, callback):
                callback(f.result())
            f.add_done_callback(partial(done, callback=callback))
            return f
        f.then = partial(then, f)

        return f

    def add_done_callback(self, future, callback):
        future.add_done_callback(callback)
        return future

    def set_future_result(self, future, result):
        future.set_result(result)

    def log_error(self, callback):
        from tornado.log import app_log
        app_log.error("Exception in callback %r", callback, exc_info=True)


class TwistedEventLoop(EventLoop):
    """ Eventloop using twisted's reactor """
    @classmethod
    def available(cls):
        try:
            import twisted
            return True
        except ImportError:
            return False

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
        d = Deferred()

        bridge.tag_object_with_id(d)

        #: Add then method so you can easily chain callbacks
        def then(d, callback):
            d.addBoth(callback)
            return d
        d.then = partial(then, d)
        return d

    def add_done_callback(self, future, callback):
        #: Both?
        future.addBoth(callback)

    def set_future_result(self, future, result):
        future.callback(result)
