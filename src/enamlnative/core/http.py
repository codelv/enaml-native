"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

@author jrm

"""
import time
from httplib import responses
from atom.api import (Atom, List, Bool, Unicode, Dict, Int, ForwardInstance,
                      Instance, Float, Callable, Subclass)
from .app import BridgedApplication


class HttpError(Exception):
    def __init__(self, code, message=None, response=None):
        self.code = code
        self.message = message or responses.get(code, "Unknown")
        self.response = response

    def __str__(self):
        return "HTTP %d: %s" %(self.code, self.message)


class HttpRequest(Atom):
    """ The request object created for fetch calls. 
    It's based on the design of Tornado's HttpRequest.
    
    """
    #: Request url
    url = Unicode()

    #: Request method
    method = Unicode('get')

    #: Request headers
    headers = Dict()

    #: Retry count
    retries = Int()

    #: Request parameter data
    data = Dict()

    #: Content type
    content_type = Unicode("application/x-www-urlencoded")

    #: Raw request body
    body = Unicode()

    #: Response created
    response = ForwardInstance(lambda: HttpResponse)

    #: Called when complete
    callback = Callable()

    #: Streaming callback
    streaming_callback = Callable()

    #: Start time
    start_time = Float()

    def __init__(self, *args, **kwargs):
        """ Build the request as configured.
        
        """
        super(HttpRequest, self).__init__(*args, **kwargs)
        self.start_time = time.time()
        self.response = HttpResponse(request=self)
        self.init_request()

    def init_request(self):
        """ Initialize the request using whatever native means necessary 
        
        """
        raise NotImplementedError


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
    headers = Dict()

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

    #: Progress
    progress = Int()

    #: Done time
    request_time = Float()


class AbstractAsyncHttpClient(Atom):
    """ An AsyncHttpClient that lets you fetch using a format similar to 
    tornado's AsyncHTTPClient but using a native library. 
    
    This is done instead of using a python library so it handles all
    SSL stuff for us. Otherwise we have to compile and link all the SSL
    libraries with python which makes the app huge (at least 5Mb in ssl 
    libs alone) and the build process even more complicated.

    """

    #: Factory used to build the request
    request_factory = Subclass(HttpRequest)

    #: Pending requests
    requests = List(HttpRequest)

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
        app = BridgedApplication.instance()
        f = app.create_future()

        #: Set callback for when response is in
        if callback is not None:
            f.then(callback)

        def handle_response(response):
            """ Callback when the request is complete. """
            self.requests.remove(response.request)
            f.set_result(response)

        #: Create and dispatch the request object
        request = self.request_factory(url=url,
                                       callback=handle_response,
                                       **kwargs)

        #: Save a reference
        #: This gets removed in the handle response
        self.requests.append(request)

        #: Run the request
        self._fetch(request)

        #: Save it on the future so it can be accessed and observed
        #: from a view if needed
        f.request = request
        return f

    def _fetch(self, request):
        """ Actually do the request. Subclasses shall override this
        to implement it using the native API's.
        
        """
        raise NotImplementedError


class AbstractWebsocketClient(Atom):
    """ An AsyncWebsocketClient that lets you handle WSS using a 
    native library implementation. 
    
    This is done instead of using a python library so it handles all
    SSL stuff for us. Otherwise we have to compile and link all the SSL
    libraries with python which makes the app huge (at least 5Mb in ssl 
    libs alone) and the build process even more complicated.

    """

    @classmethod
    def connect(cls, url):
        """ Start a connection and return an instance 
        
        Parameters
        ----------
            url: string
                The url to connect to.
        
        Returns
        -------
            result: Future : AsyncWebsocketClient
                A future that resolves with the AsyncWebsocketClient connection 
                instance when the connection succeeds or fails.
        
        """
        raise NotImplementedError

    def write_message(self, message, binary=False):
        """ Sends a message to the WebSocket server. """
        raise NotImplementedError

    def close(self, code=None, reason=None):
        """ Close the websocket with the given code and reason """
        raise NotImplementedError

    def on_open(self):
        """ Called when a connection has opened """
        pass

    def on_message(self, message, is_binary):
        """ Called when a message is received """
        raise NotImplementedError

    def on_close(self, code=None, reason=None):
        """ Called when the connection is closed"""
        pass