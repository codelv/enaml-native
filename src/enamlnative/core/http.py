"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Dec 9, 2017

@author jrm

"""
from httplib import responses
from atom.api import (Atom, List, Bool, Unicode, Dict, Int, ForwardInstance,
                      Instance, Float, Callable)


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
    method = Unicode()

    #: Request headers
    headers = Dict()

    #: Retry count
    retries = Int()

    #: Request parameter data
    data = Dict()

    #: Response created
    response = ForwardInstance(lambda: HttpResponse)

    #: Called when complete
    callback = Callable()

    #: Streaming callback
    streaming_callback = Callable()

    #: Start time
    start_time = Float()


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


class AbstractAsyncHttpClient(Atom):
    """ An AsyncHttpClient that lets you fetch using a format similar to 
    tornado's AsyncHTTPClient but using a native library. 
    
    This is done instead of using a python library so it handles all
    SSL stuff for us. Otherwise we have to compile and link all the SSL
    libraries with python which makes the app huge (at least 5Mb in ssl 
    libs alone) and the build process even more complicated.

    """

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
        raise NotImplementedError


class AbstractWebsocketClient(Atom):
    """ An AsyncWebsocketClient that lets you handle WSS using a 
    native library implementation. 
    
    This is done instead of using a python library so it handles all
    SSL stuff for us. Otherwise we have to compile and link all the SSL
    libraries with python which makes the app huge (at least 5Mb in ssl 
    libs alone) and the build process even more complicated.

    """

    def write_message(self, message, binary=False):
        """ Sends a message to the WebSocket server. """

    def on_message(self, message, is_binary):
        """ """
