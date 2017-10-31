'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 3, 2017

@author: jrm
'''
import sys
import time
import pstats
from atom.api import *
from cProfile import Profile

sys.path.append('src')

from enaml.application import ProxyResolver
from enamlnative.core.app import BridgedApplication
from enamlnative.core import bridge

class TestBridge(Atom):
    #: Mock native side
    app = ForwardInstance(lambda:MockApplication)

    data = Value()

    def reset(self, platform):
        #: Reset
        self.data = self._default_data()

    def _default_data(self):
        return self.app.create_future()

    def process_events(self, data):
        self.app.set_future_result(self.data, data)

    def addTarget(self, *args, **kwargs):
        """ For iOS tests... """
        pass

class MockApplication(BridgedApplication):
    started = Float()
    stopped = Float()
    events = List()
    bridge = Instance(TestBridge)
    profile = Bool()
    profiler = Instance(Profile, ())
    error = Value()
    #: Events
    done = Value()

    __id__ = Int(-1)
    __nativeclass__ = Unicode('com.enaml.MainApplication')

    dp = Float(1)
    api_level = Int(25)

    def _default_bridge(self):
        return TestBridge(app=self)

    def _default_done(self):
        return self.create_future()

    @classmethod
    def instance(cls, platform=None):
        from enaml.application import Application
        Application._instance = None
        app = cls()
        if platform:
            app.reset(platform)
        return app

    def __init__(self, platform="ios"):
        self.resolver = ProxyResolver()
        self.reset(platform) # Default
        self.debug = True
        super(MockApplication, self).__init__()

    def reset(self, platform, eventloop='builtin'):
        if eventloop=='builtin':
            from enamlnative.core.loop import BuiltinEventLoop
            self.loop = BuiltinEventLoop()
        elif eventloop=='twisted':
            from enamlnative.core.loop import TwistedEventLoop
            self.loop = TwistedEventLoop()
        elif eventloop=='tornado':
            from enamlnative.core.loop import TornadoEventLoop
            self.loop = TornadoEventLoop()

        #: Clear it again
        from enaml.application import Application
        Application._instance = None

        #: Update resolver
        if platform=='ios':
            from enamlnative.ios.app import IPhoneApplication

            app = IPhoneApplication()
            from enamlnative.ios.factories import IOS_FACTORIES
            self.resolver.factories = IOS_FACTORIES
        else:
            from enamlnative.android.app import AndroidApplication
            app = AndroidApplication()
            from enamlnative.android.factories import ANDROID_FACTORIES
            self.resolver.factories = ANDROID_FACTORIES

        #: Clear state
        self.error = None
        self.done = self._default_done()
        self.bridge.reset(platform)
        return app

    def start(self):
        if self.profile:
            self.profiler.enable()
        self.started = time.time()
        self.deferred_call(self.show_view)
        super(MockApplication, self).start()

    def show_view(self):
        try:
            result = self.get_view()
        except (NotImplementedError, Exception) as e:
            result = e

        if self.done.done():
            raise# self.done.result()
        else:
            self.set_future_result(self.done, result)

    def dispatch_events(self, data):
        print("Dispatch {} kbytes".format(len(data)/1000))
        self.bridge.process_events(data)

    def load_plugin_factories(self):
        pass

    def stop(self):
        """ Stop the profiler, print some info and the profiler stats"""
        if self.profile:
            self.profiler.disable()
        self.stopped = time.time()
        super(MockApplication, self).stop()

    def run(self):
        """ Start and run intl the events are processed """

        def stop(result):
            if isinstance(result, Exception):
                self.error = result
            self.stop()
            #for e in events[0:100]:
            #    print(e)
            dt = (self.stopped-self.started)*1000
            print("Took {}ms".format(dt))
            #print("Events: {}").format(len(events))
            if self.profile:
                stats = pstats.Stats(self.profiler)
                for sort in ['tottime','cumtime']:
                    stats.sort_stats(sort)
                    stats.print_stats(0.1)

        self.done.then(stop)
        self.deferred_call(self.show_view)
        self.start()
        if self.error:
            raise self.error



