"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Bool, Event, ForwardTyped, Int, Str, Typed
from enaml.core.declarative import d_, observe
from .view_group import ProxyViewGroup, ViewGroup


class ProxyWebView(ProxyViewGroup):
    """The abstract definition of a proxy WebView object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: WebView)

    def set_url(self, url: str):
        raise NotImplementedError

    def set_source(self, source: str):
        raise NotImplementedError

    def do_reload(self):
        raise NotImplementedError

    def do_go_back(self):
        raise NotImplementedError

    def do_go_forward(self):
        raise NotImplementedError

    def do_zoom_in(self):
        raise NotImplementedError

    def do_zoom_out(self):
        raise NotImplementedError


class WebView(ViewGroup):
    """A layout that places its children in a rectangular grid."""

    #: Page load error occurred
    error = d_(Bool(), writable=False)

    #: Page error code
    error_code = d_(Int(), writable=False)

    #: Error message
    error_message = d_(Str(), writable=False)

    #: Enable javascript
    javascript_enabled = d_(Bool(True))

    #: Read only title from the loaded page
    title = d_(Str(), writable=False)

    #: Read only loading progress
    progress = d_(Int(), writable=False)

    #: State
    loading = d_(Bool(), writable=False)

    #: Loads the URL (if given)
    url = d_(Str())

    #: Loads the source (if given)
    source = d_(Str())

    #: Reloads the current URL.
    reload = d_(Event())

    #: Go back in history
    go_back = d_(Event())

    #: Go forward in history
    go_forward = d_(Event())

    #: Zoom in
    zoom_in = d_(Event())

    #: Zoom out
    zoom_out = d_(Event())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyWebView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe(
        "javascript_enabled",
        "url",
        "reload",
        "source",
        "go_forward",
        "go_back",
        "zoom_in",
        "zoom_out",
    )
    def _update_proxy(self, change):
        if change["type"] == "event":
            if handler := getattr(self.proxy, f"do_{change['name']}", None):
                handler()
        else:
            super()._update_proxy(change)
