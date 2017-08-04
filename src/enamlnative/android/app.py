'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

@author jrm

'''
import jnius
import unicodedata #: Required by tornado for encodings
from atom.api import Float, Value, Int, Unicode, Typed
from enaml.application import ProxyResolver
from . import factories
from .android_activity import Activity
from ..core.app import BridgedApplication


class AppEventListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['com/enaml/MainActivity$AppEventListener']
    __javacontext__ = 'app'

    def __init__(self, handler):
        self.__handler__ = handler
        super(AppEventListener, self).__init__()

    @jnius.java_method('([B)V')
    def onEvents(self, data):
        self.__handler__.on_events(bytearray(data))

    @jnius.java_method('()V')
    def onResume(self):
        self.__handler__.on_resume()

    @jnius.java_method('()V')
    def onPause(self):
        self.__handler__.on_pause()

    @jnius.java_method('()V')
    def onStop(self):
        self.__handler__.on_stop()

    @jnius.java_method('()V')
    def onDestroy(self):
        self.__handler__.on_destroy()


class AndroidApplication(BridgedApplication):
    """ An Android implementation of an Enaml Native BridgedApplication.

    A AndroidApplication uses the native Android widget toolkit to implement an Enaml UI that
    runs in the local process.

    """

    #: Attributes so it can be seralized over the bridge as a reference
    __nativeclass__ = Unicode('android.content.Context')

    #: Bridge widget
    widget = Typed(Activity)

    #: Android Activity
    activity = Value()

    #: Pixel density of the device
    #: Loaded immediately as this is used often.
    dp = Float()

    #: Save reference to the event listener
    listener = Typed(AppEventListener)

    # --------------------------------------------------------------------------
    # Defaults
    # --------------------------------------------------------------------------
    def _default_widget(self):
        """ Return a bridge object reference to the MainActivity """
        return Activity(__id__=-1)

    def _default_dp(self):
        return self.activity.getResources().getDisplayMetrics().density

    # --------------------------------------------------------------------------
    # AndroidApplication Constructor
    # --------------------------------------------------------------------------
    def __init__(self, activity):
        """ Initialize a AndroidApplication. Uses jnius to retrieve
            an instance of the activity.
        """
        super(AndroidApplication, self).__init__()
        self.activity = jnius.autoclass(activity).mActivity
        self.resolver = ProxyResolver(factories=factories.ANDROID_FACTORIES)

    # --------------------------------------------------------------------------
    # Abstract API Implementation
    # --------------------------------------------------------------------------
    def start(self):
        """ Start the application's main event loop. Bind the Android app event
            listener using jnius.
        """
        activity = self.activity

        #: Hook for JNI using jnius
        self.listener = AppEventListener(self)
        activity.setAppEventListener(self.listener)

        super(AndroidApplication, self).start()

    # --------------------------------------------------------------------------
    # Bridge API Implementation
    # --------------------------------------------------------------------------
    def show_view(self):
        """ Show the current `app.view`. This will fade out the previous
            with the new view.
        """
        self.widget.setView(self.get_view())

    def dispatch_events(self, data):
        """ Send the data to the Native application for processing """
        self.activity.processEvents(data)

    # --------------------------------------------------------------------------
    # Android utilities API Implementation
    # --------------------------------------------------------------------------
    def _observe_keep_screen_on(self, change):
        """ Sets or clears the flag to keep the screen on. """
        def set_screen_on(window):
            from .android_window import Window
            window = Window(__id__=window)
            if self.keep_screen_on:
                window.addFlags(Window.FLAG_KEEP_SCREEN_ON)
            else:
                window.clearFlags(Window.FLAG_KEEP_SCREEN_ON)

        self.widget.getWindow().then(set_screen_on)
