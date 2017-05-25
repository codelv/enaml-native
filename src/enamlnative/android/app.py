import jnius
from atom.api import Value, Dict, Long
from enaml.application import Application, ProxyResolver

from . import factories

Activity = jnius.autoclass('android.app.Activity')
View = jnius.autoclass('android.view.View')

class AndroidApplication(Application):
    """ An Android implementation of an Enaml application.

    A AndroidApplication uses the native Android widget toolkit to implement an Enaml UI that
    runs in the local process.

    """
    #: Android Activity
    activity = Value(Activity) # TODO...

    #: View to display within the activity
    view = Value(View)

    #: Callback cache
    _callback_cache = Dict()
    _callback_id = Long()



    def __init__(self, activity):
        """ Initialize a AndroidApplication

        """
        super(AndroidApplication, self).__init__()
        self.activity = activity
        self.resolver = ProxyResolver(factories=factories.ANDROID_FACTORIES)

    #--------------------------------------------------------------------------
    # Abstract API Implementation
    #--------------------------------------------------------------------------
    def start(self):
        """ Start the application's main event loop.

        """
        activity = self.activity
        view = self.get_view()
        assert view, "View does not exist!"
        activity.setView(view)

    def get_view(self):
        """ Prepare the view

        """
        view = self.view
        if not view.is_initialized:
            view.initialize()
        if not view.proxy_is_active:
            view.activate_proxy()
        return view.proxy.widget

    def stop(self):
        """ Stop the application's main event loop.

        """
        activity = self.activity
        activity.exit()

    def invoke_callback(self,callback_id):
        """ Invoke the call with the given id.

        Parameters
        ----------
        callback_id : long
            The id of a previously scheduled call.


        """
        if callback_id in self._callback_cache:
            callback,args,kwargs = self._callback_cache[callback_id]
            callback(*args,**kwargs)
            del self._callback_cache[callback_id]

    def deferred_call(self, callback, *args, **kwargs):
        """ Invoke a callable on the next cycle of the main event loop
        thread.

        Parameters
        ----------
        callback : callable
            The callable object to execute at some point in the future.

        *args, **kwargs
            Any additional positional and keyword arguments to pass to
            the callback.

        """
        self.timed_call(0,callback,*args,**kwargs)

    def timed_call(self, ms, callback, *args, **kwargs):
        """ Invoke a callable on the main event loop thread at a
        specified time in the future.

        Parameters
        ----------
        ms : int
            The time to delay, in milliseconds, before executing the
            callable.

        callback : callable
            The callable object to execute at some point in the future.

        *args, **kwargs
            Any additional positional and keyword arguments to pass to
            the callback.

        """
        self._callback_id += 1
        self._callback_cache[self._callback_id] = (callback,args,kwargs)
        activity = self.activity
        activity.scheduleCallback(self._callback_id,ms)

    def is_main_thread(self):
        """ Indicates whether the caller is on the main gui thread.

        Returns
        -------
        result : bool
            True if called from the main gui thread. False otherwise.

        """
        return True

    def create_mime_data(self):
        """ Create a new mime data object to be filled by the user.

        Returns
        -------
        result : MimeData
            A concrete implementation of the MimeData class.

        """
        return {}