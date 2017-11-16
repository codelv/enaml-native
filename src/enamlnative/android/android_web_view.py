"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.
    
Created on July 7, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.web_view import ProxyWebView

from .android_view_group import AndroidViewGroup, ViewGroup, MarginLayoutParams
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class WebView(ViewGroup):
    __nativeclass__ = set_default('android.webkit.WebView')
    loadUrl = JavaMethod('java.lang.String')
    setWebViewClient = JavaMethod('android.webkit.WebViewClient')
    reload = JavaMethod()
    goBack = JavaMethod()
    goForward = JavaMethod()
    zoomIn = JavaMethod()
    zoomOut = JavaMethod()


class BridgedWebViewClient(JavaBridgeObject):
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedWebViewClient')
    setWebView = JavaMethod(
        'android.webkit.WebView',
        'com.codelv.enamlnative.adapters.BridgedWebViewClient$WebViewListener')
    setJavaScriptEnabled = JavaMethod('boolean')
    onLoadResource = JavaCallback('android.webkit.WebView', 'java.lang.String')
    onPageStarted = JavaCallback('android.webkit.WebView', 'java.lang.String',
                                 'android.graphics.Bitmap')
    onPageFinished = JavaCallback('android.webkit.WebView', 'java.lang.String')
    onScaleChanged = JavaCallback('android.webkit.WebView', 'float', 'float')
    onReceivedError = JavaCallback('android.webkit.WebView', 'int',
                                   'java.lang.String', 'java.lang.String')

    onProgressChanged = JavaCallback('android.webkit.WebView', 'int')
    onReceivedTitle = JavaCallback('android.webkit.WebView',
                                   'java.lang.String')


class AndroidWebView(AndroidViewGroup, ProxyWebView):
    """ An Android implementation of an Enaml ProxyWebView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(WebView)

    #: A client for listening to web view events
    client = Typed(BridgedWebViewClient)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = WebView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidWebView, self).init_widget()
        d = self.declaration

        self.client = BridgedWebViewClient()
        #self.client.setWebViewListener(self.client.getId())
        self.client.setWebView(self.widget, self.client.getId())
        self.client.onLoadResource.connect(self.on_load_resource)
        self.client.onPageFinished.connect(self.on_page_finished)
        self.client.onPageStarted.connect(self.on_page_started)
        self.client.onReceivedError.connect(self.on_received_error)
        self.client.onScaleChanged.connect(self.on_scale_changed)
        self.client.onProgressChanged.connect(self.on_progress_changed)
        self.client.onReceivedTitle.connect(self.on_page_title_changed)

        #: Done by setWebView
        #self.widget.setWebViewClient(self.client)
        if d.javascript_enabled:
            self.set_javascript_enabled(d.javascript_enabled)

        if d.url:
            self.set_url(d.url)

    def destroy(self):
        """ Destroy the client

        """
        if self.client:
            #: Stop listening
            self.client.setWebView(self.widget, None)
            del self.client
        super(AndroidWebView, self).destroy()

    # -------------------------------------------------------------------------
    # WebViewClient API
    # -------------------------------------------------------------------------
    def on_load_resource(self, view, url):
        pass

    def on_page_started(self, view, url):
        d = self.declaration
        d.loading = True
        d = self.declaration
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
