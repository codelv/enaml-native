"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Int, Event, Bool, observe, set_default
)

from enaml.core.declarative import d_

from .view_group import ViewGroup, ProxyViewGroup


class ProxyWebView(ProxyViewGroup):
    """ The abstract definition of a proxy WebView object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: WebView)

    def set_url(self, url):
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
    """ A layout that places its children in a rectangular grid.

    """

    #: Page load error occurred
    error = d_(Bool(), writable=False)

    #: Page error code
    error_code = d_(Int(), writable=False)

    #: Error message
    error_message = d_(Unicode(), writable=False)

    #: Enable javascript
    javascript_enabled = d_(Bool(True))

    #: Read only title from the loaded page
    title = d_(Unicode(), writable=False)

    #: Read only loading progress
    progress = d_(Int(), writable=False)

    #: State
    loading = d_(Bool(), writable=False)

    #: Loads the given URL.
    url = d_(Unicode())

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
    @observe('javascript_enabled', 'url', 'reload',
             'go_forward', 'go_back', 'zoom_in', 'zoom_out')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        if change['type'] == 'event':
            name = 'do_'+change['name']
            if hasattr(self.proxy, name):
                handler = getattr(self.proxy, name)
                handler()
        else:
            super(WebView, self)._update_proxy(change)
