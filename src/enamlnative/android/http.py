"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 18, 2017

@author: jrm
"""

import time
from atom.api import (Atom, Callable, Dict, List, ForwardInstance, Int,
                      Float, Bool, Unicode, Instance, set_default)
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback
from .app import AndroidApplication


class LoopjRequest(JavaBridgeObject):
    """ Since this is passed with every request, use this for listening for 
    events
    
    """
    __nativeclass__ = set_default('com.loopj.android.http.RequestParams')

    #: Java methods
    put = JavaMethod('java.lang.String', 'java.lang.String')


class LoopjAsyncHttpResponseHandler(JavaBridgeObject):
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedAsyncHttpResponseHandler')
    setAsyncHttpResponseListener = JavaMethod(
        'com.codelv.enamlnative.adapters.BridgedAsyncHttpResponseHandler'
        '$AsyncHttpResponseListener', 'boolean')

    # -------------------------------------------------------------------------
    # AsyncHttpResponseHandler API
    # -------------------------------------------------------------------------
    onStart = JavaCallback()
    onProgress = JavaCallback('int', 'int')
    onProgressData = JavaCallback('[B')
    onFinish = JavaCallback()
    onRetry = JavaCallback('int')
    onCancel = JavaCallback()
    onSuccess = JavaCallback('int', '[com.loopj.android.http.Header;', '[B')
    onFailure = JavaCallback('int', '[com.loopj.android.http.Header;', '[B',
                             'java.lang.Throwable')


class LoopjAsyncHttpClient(JavaBridgeObject):
    """ Uses https://loopj.com/android-async-http/

    Example
    -----------
    client = AsyncHttpClient()
    client.get(url,client.getId())

    """
    #: It's recommended to use this statically, so make a singleton
    _instance = None
    __nativeclass__ = set_default('com.loopj.android.http.AsyncHttpClient')

    @classmethod
    def instance(cls):
        return cls._instance

    def __init__(self, *args, **kwargs):
        """ Implement a singleton pattern """
        if LoopjAsyncHttpClient.instance() is not None:
            raise RuntimeError(
                "Only one instance of AsyncHttpClient should be used!")
        super(LoopjAsyncHttpClient, self).__init__(*args, **kwargs)
        LoopjAsyncHttpClient._instance = self

    get = JavaMethod('java.lang.String',
                     'com.loopj.android.http.RequestParams',
                     'com.loopj.android.http.ResponseHandlerInterface')
    post = JavaMethod('java.lang.String',
                      'com.loopj.android.http.RequestParams',
                      'com.loopj.android.http.ResponseHandlerInterface')

    #setCookieStore = JavaMethod('')


class HttpRequest(Atom):
    #: Request url
    url = Unicode()

    #: Request method
    method = Unicode()

    #: Request headers
    headers = List()

    #: Retry count
    retries = Int()

    #: Response created
    response = ForwardInstance(lambda:HttpResponse)

    #: Response handler
    handler = Instance(LoopjAsyncHttpResponseHandler)

    #: Called when complete
    callback = Callable()

    #: Streaming callback
    streaming_callback = Callable()

    #: Start time
    time = Float()

    def __init__(self, *args, **kwargs):
        super(HttpRequest, self).__init__(*args, **kwargs)
        self.time = time.time()
        self.response = HttpResponse(request=self)

    def _default_handler(self):
        handler = LoopjAsyncHttpResponseHandler()
        handler.setAsyncHttpResponseListener(
            handler.getId(),
            self.streaming_callback is not None)
        handler.onStart.connect(self.on_start)
        handler.onCancel.connect(self.on_cancel)
        handler.onFailure.connect(self.on_failure)
        handler.onFinish.connect(self.on_finish)
        handler.onProgress.connect(self.on_progress)
        handler.onProgressData.connect(self.on_progress_data)
        handler.onSuccess.connect(self.on_success)
        handler.onRetry(self.on_retry)

        return handler

    def on_start(self):
        pass

    def on_cancel(self):
        pass

    def on_retry(self, retry):
        self.retries = retry

    def on_success(self, status, headers, data):
        r = self.response
        r.status_code = status
        r.headers = headers.split("\n")
        if data:
            r.content = data
        r.ok = True

    def on_failure(self, status, headers, data, error):
        r = self.response
        r.status_code = status
        r.headers = headers.split("\n")
        r.reason = error
        if data:
            r.content = data
        r.ok = False

    def on_finish(self):
        r = self.response
        r.time = time.time()
        if self.callback:
            self.callback(r)

    def on_progress(self, written, total):
        r = self.response
        r.content_length = total
        r.progress = int(100*written/total)

    def on_progress_data(self, data):
        if self.streaming_callback:
            self.streaming_callback(data)


class HttpResponse(Atom):

    #: Request that created this response
    request = Instance(HttpRequest)

    #: Response headers
    headers = List()

    #: Result success
    ok = Bool()

    #: Response body
    #: if a streaming_callback is given to the request
    #: then this is NOT used
    content = Unicode()

    #: Size
    content_length = Int()

    #: Result
    status_code = Int()

    #: Error message
    reason = Unicode()

    #: Response headers
    headers = List()

    #: Progress
    progress = Int()

    #: Done time
    time = Float()


class AsyncHttpClient(Atom):
    """ This is the API you should actually use

    """
    #: App event loop
    app = Instance(AndroidApplication, factory=AndroidApplication.instance)

    #: Client config
    config = Dict()

    client = Instance(LoopjAsyncHttpClient)

    requests = List()

    def _default_client(self):
        #: Get existing or create a new client
        return LoopjAsyncHttpClient.instance() or LoopjAsyncHttpClient()

    def fetch(self, url, callback=None, raise_error=True, **kwargs):
        """  Fetch

        """
        future = self.app.create_future()

        #: Get the method to use
        method = getattr(self.client, kwargs.get('method', 'get').lower())

        #: Create the RequestParams
        params = LoopjRequest()
        request = HttpRequest(url=url, **kwargs)

        #: Set callback for when response is in
        if callback is not None:
            future.then(callback)

        def handle_response(response):
            """ Callback when the request is complete. """
            self.requests.remove(response.request)
            self.app.set_future_result(future, response)

        request.callback = handle_response

        #: This is a bit confusing
        #: pass the url, request params, and the id to use as a listener
        #: to the LoopjAsyncHttpClient get or post command.
        method(url, params, request.handler)

        #: Save a reference (is this needed?)
        self.requests.append(request)
        future.request = request
        return future

    def close(self):
        pass

