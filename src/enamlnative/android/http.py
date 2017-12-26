"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 18, 2017

@author: jrm
"""

import time
from atom.api import (Atom, Callable, Dict, List, ForwardInstance, Int,
                      Float, Bool, Unicode, Instance, set_default)
from .bridge import (JavaBridgeObject, JavaMethod, JavaCallback,
                     JavaStaticMethod)
from ..core.http import (HttpRequest, HttpError, AbstractAsyncHttpClient,
                         AbstractWebsocketClient)


class BridgedAsyncHttpCallback(JavaBridgeObject):
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedAsyncHttpCallback')
    setAsyncHttpResponseListener = JavaMethod(
        'com.codelv.enamlnative.adapters.BridgedAsyncHttpCallback'
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
    onSuccess = JavaCallback('int', 'java.lang.String', '[B')
    onFailure = JavaCallback('int', 'java.lang.String', '[B',
                             'java.lang.Throwable')


class Call(JavaBridgeObject):
    __nativeclass__ = set_default('okhttp3.Call')
    cancel = JavaMethod()
    clone = JavaMethod()
    enqueue = JavaMethod('okhttp3.Callback')
    execute = JavaMethod(returns='okhttp3.Response')
    request = JavaMethod('okhttp3.Request')


class Interceptor(JavaBridgeObject):
    __nativeclass__ = set_default('okhttp3.Interceptor')


class OkHttpClient(JavaBridgeObject):
    """ OkHttp performs best when you create a single OkHttpClient instance 
    and reuse it for all of your HTTP calls. This is because each client holds 
    its own connection pool and thread pools. Reusing connections and threads 
    reduces latency and saves memory. Conversely, creating a client for each 
    request wastes resources on idle pools.
    """
    #: Shared instance
    _instance = None

    __nativeclass__ = set_default('okhttp3.OkHttpClient')

    newCall = JavaMethod('okhttp3.Request', returns='okhttp3.Call')
    newWebSocket = JavaMethod('okhttp3.Request', 'okhttp3.WebSocketListener',
                              returns='okhttp3.WebSocket')

    class Builder(JavaBridgeObject):
        __nativeclass__ = set_default('okhttp3.OkHttpClient$Builder')
        addNetworkInterceptor = JavaMethod('okhttp3.Interceptor')
        build = JavaMethod(returns='okhttp3.OkHttpClient')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            OkHttpClient()
        return cls._instance

    def __init__(self, *args, **kwargs):
        """ Implement a singleton pattern """
        if OkHttpClient._instance is not None:
            raise RuntimeError(
                "Only one instance of OkHttpClient should be used!")
        super(OkHttpClient, self).__init__(*args, **kwargs)
        OkHttpClient._instance = self


class MediaType(JavaBridgeObject):
    __nativeclass__ = set_default('okhttp3.MediaType')
    parse = JavaStaticMethod('java.lang.String', returns='okhttp3.MediaType')


class RequestBody(JavaBridgeObject):
    __nativeclass__ = set_default('okhttp3.RequestBody')
    create = JavaStaticMethod('okhttp3.MediaType', 'java.lang.String',
                              # TODO: Should support '[B',
                              returns='okhttp3.RequestBody')


class Request(JavaBridgeObject):
    __nativeclass__ = set_default('okhttp3.Request')

    class Builder(JavaBridgeObject):
        __nativeclass__ = set_default('okhttp3.Request$Builder')
        url = JavaMethod('java.lang.String')
        addHeader = JavaMethod('java.lang.String', 'java.lang.String')
        method = JavaMethod('java.lang.String', 'okhttp3.RequestBody')
        get = JavaMethod()
        put = JavaMethod()
        delete = JavaMethod()
        build = JavaMethod(returns='okhttp3.Request')


class WebSocketListener(JavaBridgeObject):
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedWebsocketListener')

    onClosed = JavaCallback('WebSocket webSocket', 'int code', 'String reason')
    onClosing = JavaCallback('WebSocket webSocket, int code, String reason')
    onFailure = JavaCallback('WebSocket webSocket, Throwable t, Response response')
    onMessage = JavaCallback('WebSocket webSocket', 'bytes or string')
    onOpen = JavaCallback('WebSocket webSocket', 'Response response')


class AndroidHttpRequest(HttpRequest):

    #: okhttp3.Call that can be used to cancel the request
    call = Instance(Call)

    #: okhttp3.Request
    request = Instance(Request)

    #: Handles the async callbacks
    handler = Instance(BridgedAsyncHttpCallback)

    def init_request(self):
        """ Init the native request using the okhttp3.Request.Builder """

        #: Build the request
        builder = Request.Builder()
        builder.url(self.url)

        #: Set any headers
        for k, v in self.headers.items():
            builder.addHeader(k, v)

        #: Get the body or generate from the data given
        body = self.body

        if body:
            #: Create the request body
            media_type = MediaType(
                __id__=MediaType.parse(self.content_type))
            request_body = RequestBody(
                __id__=RequestBody.create(media_type, body))
            #: Set the request method
            builder.method(self.method, request_body)
        elif self.method in ['get', 'delete', 'head']:
            #: Set the method
            getattr(builder, self.method)()
        else:
            raise ValueError("Cannot do a '{}' request "
                             "without a body".format(self.method))

        #: Save the okhttp request
        self.request = Request(__id__=builder.build())

    def _default_handler(self):
        handler = BridgedAsyncHttpCallback()
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

    def _default_body(self):
        """ If the body is not passed in by the user try to create one
        using the given data parameters. 
        """
        if not self.data:
            return ""
        if self.content_type == 'application/json':
            import json
            return json.dumps(self.data)
        elif self.content_type == 'application/x-www-form-urlencoded':
            import urllib
            return urllib.urlencode(self.data)
        else:
            raise NotImplementedError(
                "You must manually encode the request "
                "body for '{}'".format(self.content_type)
            )

    def on_start(self):
        pass

    def on_cancel(self):
        pass

    def on_retry(self, retry):
        self.retries = retry

    def on_success(self, status, headers, data):
        r = self.response
        r.code = status
        if headers:
            r.headers = headers
        if data:
            r.body = data
        r.progress = 100
        r.ok = True

    def on_failure(self, status, headers, data, error):
        r = self.response
        r.code = status
        if headers:
            r.headers = headers
        if error:
            r.reason = error
        r.error = HttpError(status, error, r)
        if data:
            r.body = data
        r.ok = False

    def on_finish(self):
        """ Called regardless of success or failure """
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


class AsyncHttpClient(AbstractAsyncHttpClient):
    """ An AsyncHttpClient that lets you fetch using a format similar to 
    tornado's AsyncHTTPClient but using the Android native Loopj library. 
    
    This is done instead of using a python library so it handles all
    SSL stuff for us. Otherwise we have to compile and link all the SSL
    libraries with python which makes the app huge (at least 5Mb in ssl 
    libs alone) and the build process even more complicated.

    """

    #: The client that actually does the request
    client = Instance(OkHttpClient)

    #: Set this as the request factory
    request_factory = set_default(AndroidHttpRequest)

    def _default_client(self):
        #: Get existing or create a new client
        return OkHttpClient.instance()

    def _fetch(self, request):
        """ Fetch using the OkHttpClient """
        client = self.client

        #: Dispatch the async call
        call = Call(__id__=client.newCall(request.request))
        call.enqueue(request.handler)

        #: Save the call reference
        request.call = call
