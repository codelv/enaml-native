'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
import enamlnative
from atom.api import Atom, Value, Subclass, Callable, Unicode
from functools import partial
from . import bridge


class EventLoop(Atom):
    """ Event loop delegation api

    """
    #: So users can check if needed
    name = Unicode()

    #: Actual event loop object
    loop = Value()

    @classmethod
    def default(cls):
        """ Get the first available event loop implementation
            based on which packages are installed."""
        for impl in [
            TornadoEventLoop,
            TwistedEventLoop,
            BuiltinEventLoop,
        ]:
            if impl.available():
                print("Using {} event loop!".format(impl))
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

    #: Future implementation
    future = Subclass(object)

    @classmethod
    def available(cls):
        try:
            with enamlnative.imports():
                import unicodedata #: Required by tornado for encodings
                from tornado.ioloop import IOLoop
            return True
        except ImportError as e:
            print("Tornado event loop not available {}".format(e))
            return False

    def _default_name(self):
        return "tornado"

    def _default_loop(self):
        from tornado.ioloop import IOLoop
        return IOLoop.current()

    def deferred_call(self, callback, *args, **kwargs):
        return self.loop.add_callback(callback, *args, **kwargs)

    def timed_call(self, ms, callback, *args, **kwargs):
        return self.loop.call_later(ms/1000.0, callback, *args, **kwargs)

    def set_error_handler(self, handler):
        self.loop.handle_callback_exception = handler

    def _default_future(self):
        from tornado.concurrent import Future
        return Future

    def create_future(self):
        f = self.future()
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

    #: Attached to all "futures" and is invoked when an exception occurs
    _handler = Callable()

    def _default_name(self):
        return "twisted"

    @classmethod
    def available(cls):
        try:
            with enamlnative.imports():
                from twisted.internet import reactor
            return True
        except ImportError as e:
            print("Twisted event loop not available {}".format(e))
            return False

    def _default_loop(self):
        from twisted.internet import reactor
        return reactor

    def start(self):
        print("Starting reactor {}".format(self.loop))
        self.loop.run()

    def deferred_call(self, callback, *args, **kwargs):
        """ We have to wake up the reactor after every call because
            it may calculate a long delay where it can sleep which causes events that
            happen during this period to seem really slow as they do not get processed until
            after the reactor "wakes up"
        """
        r = self.loop.callLater(0, callback, *args, **kwargs)
        self.loop.wakeUp()
        return r

    def timed_call(self, ms, callback, *args, **kwargs):
        """ We have to wake up the reactor after every call because
            it may calculate a long delay where it can sleep which causes events that
            happen during this period to seem really slow as they do not get processed until
            after the reactor "wakes up"
        """
        r = self.loop.callLater(ms/1000.0, callback, *args, **kwargs)
        self.loop.wakeUp()
        return r

    def set_error_handler(self, handler):
        self._handler = handler

    def create_future(self):
        from twisted.internet.defer import Deferred
        d = Deferred()

        bridge.tag_object_with_id(d)

        #: Error handling support
        if self._handler:
            d.addErrback(self._handler)

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


class BuiltinEventLoop(TornadoEventLoop):
    """ Use the built in event loop. It's a stripped down version of tornado,
        It's currently slightly slower than tornado at the moment so use
        tornado if possible.
    """
    @classmethod
    def available(cls):
        try:
            with enamlnative.imports():
                from .eventloop.ioloop import IOLoop
            return True
        except ImportError:
            print("Error: Failed to load the builtin event loop. "
                  "This usually indicates missing or inaccessible shared libraries.")
            return False

    def _default_future(self):
        from .eventloop.concurrent import Future
        return Future

    def _default_loop(self):
        from .eventloop.ioloop import IOLoop
        return IOLoop.current()

    def set_error_handler(self, handler):
        self.loop.set_callback_exception_handler(handler)