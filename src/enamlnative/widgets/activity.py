"""
Copyright (c) 2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

"""
from atom.api import (
    Dict,
    Enum,
    Event,
    Float,
    ForwardTyped,
    Instance,
    Int,
    Str,
    Typed,
    observe,
)
from enaml.application import Application
from enaml.core.declarative import d_, d_func
from enaml.widgets.toolkit_object import ProxyToolkitObject, ToolkitObject
from .window import Window


class ProxyActivity(ProxyToolkitObject):
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Activity)

    async def start(self):
        raise NotImplementedError()

    def show_loading(self, message):
        raise NotImplementedError()


class Activity(ToolkitObject):
    #: Reference to the proxy
    proxy = Typed(ProxyActivity)

    #: Reference to the application
    app = Instance(Application)

    #: Activity lifecycle events
    started = d_(Event(), writable=False)
    paused = d_(Event(), writable=False)
    resumed = d_(Event(), writable=False)
    stopped = d_(Event(), writable=False)

    #: Activity lifecycle state must be set by the implementation
    state = Enum("created", "paused", "resumed", "stopped", "destroyed")

    #: Pixel density of the device
    #: Loaded immediately as this is used often.
    dp = Float()

    #: Width of the screen in dp
    width = Float(strict=False)

    #: Height of the screen in dp
    height = Float(strict=False)

    #: Screen orientation
    orientation = Enum("portrait", "landscape", "square")

    #: Build info from
    #: https://developer.android.com/reference/android/os/Build.VERSION.html
    build_info = Dict()

    #: SDK version
    #: Loaded immediately
    api_level = Int()

    async def start(self):
        """Start the activity."""
        if not self.is_initialized:
            self.initialize()
        await self.proxy.start()
        if not self.proxy_is_active:
            super().activate_proxy()

    def show_loading(self, message: str):
        self.proxy.show_loading(message)

    def _default_app(self):
        return Application.instance()

    @d_func
    def on_back_pressed(self) -> bool:
        """Override this to handle the back event"""
        return False

    @d_func
    def on_reload(self):
        """Override this to handle the back event"""
        pass

    def child_added(self, child):
        if isinstance(child, ToolkitObject) and not isinstance(child, Window):
            raise TypeError(f"An activity can only contain Windows, got: {child}")
        super().child_added(child)
