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
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback, encode
from .app import AndroidApplication
from httplib import responses


class LoopjHeader(JavaBridgeObject):
    __nativeclass__ = set_default(
        'cz.msebera.android.httpclient.message.BasicHeader')
    __signature__ = set_default(('java.lang.String', 'java.lang.String'))


class LoopjRequestParams(JavaBridgeObject):
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

    setBasicAuth = JavaMethod('java.lang.String', 'java.lang.String')
    setTimeout = JavaMethod('int')
    setConnectTimeout = JavaMethod('int')
    setUserAgent = JavaMethod('java.lang.String')

    get = JavaMethod('android.content.Context', 'java.lang.String',
                     '[Lcz.msebera.android.httpclient.Header;',
                     'com.loopj.android.http.RequestParams',
                     'com.loopj.android.http.ResponseHandlerInterface')
    post = JavaMethod('android.content.Context', 'java.lang.String',
                      '[Lcz.msebera.android.httpclient.Header;',
                      'com.loopj.android.http.RequestParams',
                      'com.loopj.android.http.ResponseHandlerInterface')
    put = JavaMethod('android.content.Context', 'java.lang.String',
                     '[Lcz.msebera.android.httpclient.Header;',
                     'com.loopj.android.http.RequestParams',
                     'com.loopj.android.http.ResponseHandlerInterface')
    delete = JavaMethod('android.content.Context', 'java.lang.String',
                        '[Lcz.msebera.android.httpclient.Header;',
                        'com.loopj.android.http.RequestParams',
                        'com.loopj.android.http.ResponseHandlerInterface')
    head = JavaMethod('android.content.Context', 'java.lang.String',
                      '[Lcz.msebera.android.httpclient.Header;',
                      'com.loopj.android.http.RequestParams',
                      'com.loopj.android.http.ResponseHandlerInterface')



class HttpError(Exception):
    def __init__(self, code, message=None, response=None):
        self.code = code
        self.message = message or responses.get(code, "Unknown")
        self.response = response

    def __str__(self):
        return "HTTP %d: %s" %(self.code, self.message)


class HttpRequest(Atom):
    #: Request url
    url = Unicode()

    #: Request method
    method = Unicode()

    #: Request headers
    headers = Dict()

    #: Retry count
    retries = Int()

    #: Request parameter data
    data = Dict()

    #: Response created
    response = ForwardInstance(lambda: HttpResponse)

    #: The actual LoopjRequest object
    params = Instance(LoopjRequestParams)

    #: Response handler
    handler = Instance(LoopjAsyncHttpResponseHandler)

    #: Called when complete
    callback = Callable()

    #: Streaming callback
    streaming_callback = Callable()

    #: Start time
    start_time = Float()

    def __init__(self, *args, **kwargs):
        super(HttpRequest, self).__init__(*args, **kwargs)
        self.start_time = time.time()
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

    def _default_params(self):
        """ RequestParams to send with the request.
        """
        #: Create the RequestParams
        params = LoopjRequestParams()

        #: Update body
        for k, v in self.data.items():
            params.put(k, v)

        return params

    def on_start(self):
        pass

    def on_cancel(self):
        pass

    def on_retry(self, retry):
        self.retries = retry

    def on_success(self, status, headers, data):
        r = self.response
        r.code = status
        r.headers = headers.split("\n")
        if data:
            r.body = data
        r.progress = 100
        r.ok = True

    def on_failure(self, status, headers, data, error):
        r = self.response
        r.code = status
        r.headers = headers.split("\n")
        if error:
            r.reason = error
        r.error = HttpError(status, error, r)
        if data:
            r.body = data
        r.ok = False

    def on_finish(self):
        r = self.response
        r.request_time = time.time() - self.start_time
        if self.callback:
            self.callback(r)

    def on_progress(self, written, total):
        r = self.response
        r.content_length = total
        if total:
            r.progress = int(100*written/total)

    def on_progress_data(self, data):
        if self.streaming_callback:
            self.streaming_callback(data)


class HttpResponse(Atom):
    """ The response object returned to an AsyncHttpClient fetch callback.
    It is based on the the tornado HttpResponse object.
    
    """

    #: Request that created this response
    request = Instance(HttpRequest)

    #: Numeric HTTP status code
    code = Int()

    #: Reason phrase for the status code
    reason = Unicode()

    #: Response headers list of strings
    headers = List()

    #: Result success
    ok = Bool()

    #: Response body
    #: Note: if a streaming_callback is given to the request
    #: then this is NOT used and will be empty
    body = Unicode()

    #: Size
    content_length = Int()

    #: Error message
    error = Instance(HttpError)

    #: Response headers
    headers = List()

    #: Progress
    progress = Int()

    #: Done time
    request_time = Float()


class AsyncHttpClient(Atom):
    """ An AsyncHttpClient that lets you fetch using a format similar to 
    tornado's AsyncHTTPClient but using the Android native Loopj library. 
    
    This is done instead of using a python library so it handles all
    SSL stuff for us. Otherwise we have to compile and link all the SSL
    libraries with python which makes the app huge (at least 5Mb in ssl 
    libs alone) and the build process even more complicated.

    """
    #: Client config
    config = Dict()

    #: The client that actually does the request
    client = Instance(LoopjAsyncHttpClient)

    #: Pending requests
    #: these must be held so the bridge doesn't destroy them later
    requests = List()

    def _default_client(self):
        #: Get existing or create a new client
        return LoopjAsyncHttpClient.instance() or LoopjAsyncHttpClient()

    def fetch(self, url, callback=None, raise_error=True, **kwargs):
        """  Fetch the given url and fire the callback when ready. Optionally
        pass a `streaming_callback` to handle data from large requests.
        
        Parameters
        ----------
            url: string
                The url to access.
            callback: callable
                The callback to invoke when the request completes. You can
                also use the return value.
            kwargs: 
                The arguments to pass to the `HttpRequest` object. See it
                for which values are valid.
        
        Returns
        --------
            result: Future
                A future that resolves with the `HttpResponse` object when
                the request is complete.

        """
        app = AndroidApplication.instance()
        f = app.create_future()

        #: Get the method to use
        method = getattr(self.client, kwargs.get('method', 'get').lower())

        #: Create the request object
        request = HttpRequest(url=url, **kwargs)

        #: Set callback for when response is in
        if callback is not None:
            f.then(callback)

        def handle_response(response):
            """ Callback when the request is complete. """
            self.requests.remove(response.request)
            f.set_result(response)

        request.callback = handle_response

        #: Create a header object and hold onto it until the request fires
        headers = [LoopjHeader(k, v) for k, v in request.headers.items()]

        #: Send the request
        method(app, request.url, [encode(h) for h in headers],
               request.params, request.handler)

        #: Save a reference
        self.requests.append(request)

        #: Save it on the future so it can be accessed and observed
        #: from a view if needed
        f.request = request
        return f

    def close(self):
        pass

