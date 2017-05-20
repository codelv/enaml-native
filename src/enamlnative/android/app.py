import jnius
from atom.api import Value
from enaml.application import Application, ProxyResolver

from . import factories

Activity = jnius.autoclass('android.app.Activity')
View = jnius.autoclass('android.view.View')

from enaml.widgets.main_window import MainWindow

class AndroidApplication(Application):
    """ An Android implementation of an Enaml application.

    A AndroidApplication uses the native Android widget toolkit to implement an Enaml UI that
    runs in the local process.

    """
    activity = Value(Activity) # TODO...
    content_view = Value(View)

    def __init__(self):
        """ Initialize a AndroidApplication

        """
        super(AndroidApplication, self).__init__()
        PythonActivity = jnius.autoclass('org.kivy.android.PythonActivity')
        self.activity = PythonActivity.mActivity
        self.resolver = ProxyResolver(factories=factories.ANDROID_FACTORIES)

    #--------------------------------------------------------------------------
    # Abstract API Implementation
    #--------------------------------------------------------------------------
    def start(self):
        """ Start the application's main event loop.

        """
        activity = self.activity
        if not getattr(activity, '_in_event_loop', False):
            activity._in_event_loop = True
            activity.setContentView(self.get_view())

    def get_view(self):
        """ Prepare the view

        """
        view = self.content_view
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
        activity._in_event_loop = False

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
        deferredCall(callback, *args, **kwargs)

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
        timedCall(ms, callback, *args, **kwargs)

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