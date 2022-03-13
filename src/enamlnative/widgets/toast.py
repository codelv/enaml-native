"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Sept 18, 2017
"""
from atom.api import Bool, Coerced, ForwardTyped, Int, Str, Typed
from enaml.core.declarative import d_, observe
from enaml.widgets.toolkit_object import ProxyToolkitObject, ToolkitObject
from .view import coerce_gravity


class ProxyToast(ProxyToolkitObject):
    """The abstract definition of a proxy toast object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Toast)

    def set_text(self, text):
        raise NotImplementedError

    def set_duration(self, duration):
        raise NotImplementedError

    def set_show(self, show):
        raise NotImplementedError


class Toast(ToolkitObject):
    """A toast is a view containing a quick little message for the user."""

    #: Text to display
    #: if this node has a child view this is ignored
    text = d_(Str())

    #: Duration to display in ms
    duration = d_(Int(1000))

    #: x position
    x = d_(Int())

    #: y position
    y = d_(Int())

    #: Position
    gravity = d_(Coerced(int, coercer=coerce_gravity))

    #: Show the notification for the given duration
    show = d_(Bool())

    #: A reference to the proxy object.
    proxy = Typed(ProxyToast)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("text", "duration", "show", "gravity", "x", "y")
    def _update_proxy(self, change):

        super()._update_proxy(change)
