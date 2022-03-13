"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 7, 2017
"""
from atom.api import Typed
from enamlnative.widgets.web_view import ProxyWebView
from .android_view_group import AndroidViewGroup, ViewGroup
from .android_image_view import Bitmap
from .bridge import JavaBridgeObject, JavaCallback, JavaMethod


class WebView(ViewGroup):
    __nativeclass__ = "android.webkit.WebView"
    loadUrl = JavaMethod(str)
    loadData = JavaMethod(str, str, str)
    loadDataWithBaseURL = JavaMethod(
        str,
        str,
        str,
        str,
        str,
    )
    setWebViewClient = JavaMethod("android.webkit.WebViewClient")
    reload = JavaMethod()
    goBack = JavaMethod()
    goForward = JavaMethod()
    zoomIn = JavaMethod()
    zoomOut = JavaMethod()


class BridgedWebViewClient(JavaBridgeObject):
    __nativeclass__ = "com.codelv.enamlnative.adapters.BridgedWebViewClient"
    setWebView = JavaMethod(
        WebView,
        "com.codelv.enamlnative.adapters.BridgedWebViewClient$WebViewListener",
    )
    setJavaScriptEnabled = JavaMethod(bool)
    onLoadResource = JavaCallback(WebView, str)
    onPageStarted = JavaCallback(WebView, str, Bitmap)
    onPageFinished = JavaCallback(WebView, str)
    onScaleChanged = JavaCallback(WebView, float, float)
    onReceivedError = JavaCallback(WebView, int, str, str)
    onProgressChanged = JavaCallback(WebView, int)
    onReceivedTitle = JavaCallback(WebView, str)


class AndroidWebView(AndroidViewGroup, ProxyWebView):
    """An Android implementation of an Enaml ProxyWebView."""

    #: A reference to the widget created by the proxy.
    widget = Typed(WebView)

    #: A client for listening to web view events
    client = Typed(BridgedWebViewClient)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        d = self.declaration
        self.widget = WebView(self.get_context(), None, d.style)

    def init_widget(self):
        """Initialize the underlying widget."""
        # Create and init the client
        c = self.client = BridgedWebViewClient()
        c.setWebView(self.widget, c.getId())
        c.onLoadResource.connect(self.on_load_resource)
        c.onPageFinished.connect(self.on_page_finished)
        c.onPageStarted.connect(self.on_page_started)
        c.onReceivedError.connect(self.on_received_error)
        c.onScaleChanged.connect(self.on_scale_changed)
        c.onProgressChanged.connect(self.on_progress_changed)
        c.onReceivedTitle.connect(self.on_page_title_changed)

        super().init_widget()

    def destroy(self):
        """Destroy the client"""
        if self.client:
            #: Stop listening
            self.client.setWebView(self.widget, None)
            del self.client
        super().destroy()

    # -------------------------------------------------------------------------
    # WebViewClient API
    # -------------------------------------------------------------------------
    def on_load_resource(self, view, url):
        pass

    def on_page_started(self, view, url):
        d = self.declaration
        d.loading = True
        with self.widget.loadUrl.suppressed():
            d.url = url

    def on_page_title_changed(self, view, title):
        d = self.declaration
        d.title = title

    def on_progress_changed(self, view, progress):
        d = self.declaration
        d.progress = progress

    def on_page_finished(self, view, url):
        d = self.declaration
        d.loading = False
        d.error = False

    def on_received_error(self, view, code, message, url):
        d = self.declaration
        d.error_code = code
        d.error_message = message
        d.error = True

    def on_scale_changed(self, view, old, new):
        pass

    # -------------------------------------------------------------------------
    # ProxyWebView API
    # -------------------------------------------------------------------------
    def set_url(self, url):
        self.widget.loadUrl(url)

    def set_source(self, source):
        """Set the raw HTML of this page to load. For loading from
        a file or http resource use the `url` instead.

        """
        self.widget.loadDataWithBaseURL(None, source, "text/html", "utf-8", None)

    def set_javascript_enabled(self, enabled):
        self.client.setJavaScriptEnabled(enabled)

    def do_reload(self):
        self.widget.reload()

    def do_go_back(self):
        self.widget.goBack()

    def do_go_forward(self):
        self.widget.goForward()

    def do_zoom_in(self):
        self.widget.zoomIn()

    def do_zoom_out(self):
        self.widget.zoomOut()
