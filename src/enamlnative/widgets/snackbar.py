"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Sept 20, 2017

@author: jrm
"""
from atom.api import Bool, Event, ForwardTyped, Int, Str, Typed, observe
from enaml.core.declarative import d_
from enaml.widgets.toolkit_object import ProxyToolkitObject, ToolkitObject


class ProxySnackbar(ProxyToolkitObject):
    """The abstract definition of a proxy Snackbar object."""

    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: Snackbar)

    def set_text(self, text):
        raise NotImplementedError

    def set_action_text(self, text):
        raise NotImplementedError

    def set_action_text_color(self, color):
        raise NotImplementedError

    def set_duration(self, duration):
        raise NotImplementedError

    def set_show(self, show):
        raise NotImplementedError


class Snackbar(ToolkitObject):
    """A toast is a view containing a quick little message for the user."""

    #: Text to display
    #: if this node has a child view this is ignored
    text = d_(Str())

    #: Text to display in the action button
    action_text = d_(Str())

    #: Color for the action text button
    action_text_color = d_(Str())

    #: Duration to display in ms or 0 for infinite
    duration = d_(Int(3000))

    #: Alias for the action is clicked
    clicked = d_(Event(), writable=False)

    #: When an action occurs such as swiped out, clicked, timed out, etc..
    action = d_(Event(str), writable=False)

    #: Show the snackbar for the given duration
    show = d_(Bool())

    #: A reference to the proxy object.
    proxy = Typed(ProxySnackbar)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("text", "duration", "action_text", "action_text_color", "show")
    def _update_proxy(self, change):

        super()._update_proxy(change)
