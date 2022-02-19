"""
Copyright (c) 2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

"""
from atom.api import Bool, ForwardTyped, Str, Typed
from enaml.core.declarative import d_, observe
from enaml.widgets.toolkit_object import ProxyToolkitObject, ToolkitObject


class ProxyWindow(ProxyToolkitObject):
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Window)

    def set_statusbar_color(self, color: str):
        raise NotImplementedError

    def set_keep_screen_on(self, enabled: bool):
        raise NotImplementedError


class Window(ToolkitObject):
    #: Reference to the proxy
    proxy = Typed(ProxyWindow)

    #: Statusbar color
    statusbar_color = d_(Str())

    #: Keep screen on
    keep_screen_on = d_(Bool())

    @observe("statusbar_color", "keep_screen_on")
    def _update_proxy(self, change):
        super()._update_proxy(change)
