"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Sept 20, 2017

@author: jrm
"""
from atom.api import Typed, Bool, set_default
from .bridge import JavaBridgeObject, JavaMethod, JavaStaticMethod, JavaCallback, JavaProxy
from enamlnative.widgets.snackbar import ProxySnackbar
from .android_toolkit_object import AndroidToolkitObject


class Snackbar(JavaBridgeObject):
    #: Show the view for the specified duration.
    __nativeclass__ = set_default('android.support.design.widget.Snackbar')
    __signature__ = set_default(('android.content.Context',))
    make = JavaStaticMethod('android.view.View','java.lang.CharSequence','int',
                           returns='android.support.design.widget.Snackbar')
    show = JavaMethod()
    dismiss = JavaMethod()
    setDuration = JavaMethod('int')
    setText = JavaMethod('java.lang.CharSequence')
    setAction = JavaMethod('java.lang.CharSequence',
                           'android.view.View$OnClickListener')
    setActionTextColor = JavaMethod('android.graphics.Color')
    addCallback = JavaMethod(
        'android.support.design.widget.BaseTransientBottomBar$BaseCallback')



    DISMISS_EVENT_SWIPE = 0
    DISMISS_EVENT_ACTION = 1
    DISMISS_EVENT_TIMEOUT = 2
    DISMISS_EVENT_MANUAL = 3
    DISMISS_EVENT_CONSECUTIVE = 4

    ACTIONS = {
        0: 'swipe',
        1: 'clicked',
        2: 'timeout',
        3: 'dismissed',
        4: 'replaced'
    }

    #: Snackbar.Callback API
    onClick = JavaCallback('android.view.View')

    onDismissed = JavaCallback('android.support.design.widget.Snackbar', 'int')
    onShown = JavaCallback('android.support.design.widget.Snackbar')


class BridgedSnackbarCallback(JavaBridgeObject):
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedSnackbarCallback')
    setListener = JavaMethod(
        'com.codelv.enamlnative.adapters.BridgedSnackbarCallback'
        '$SnackbarListener')


class AndroidSnackbar(AndroidToolkitObject, ProxySnackbar):
    """ An Android implementation of an Enaml ProxySnackbar.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Snackbar)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        A toast is not a subclass of view, hence we don't set name as widget
        or children will try to use it as their parent (which crashes).

        """
        d = self.declaration
        Snackbar.make(self.parent_widget(), d.text,
                      0 if d.duration else -2).then(self.on_widget_created)

    def init_widget(self):
        """ Our widget may not exist yet so we have to diverge from the normal 
        way of doing initialization. See `update_widget`
        
        """
        if not self.widget:
            return
        super(AndroidSnackbar, self).init_widget()

        d = self.declaration

        #: Bind events
        self.widget.onClick.connect(self.on_click)

        #: Use the custom callback to listen to events
        callback = BridgedSnackbarCallback()
        callback.setListener(self.widget.getId())
        self.widget.onDismissed.connect(self.on_dismissed)
        self.widget.onShown.connect(self.on_shown)
        self.widget.addCallback(callback)


        #: if d.text: #: Set during creation
        #: self.set_duration(d.duration) #: Set during creation
        if d.action_text:
            self.set_action_text(d.action_text)
        if d.action_text_color:
            self.set_action_text_color(d.action_text_color)
        if d.show:
            self.set_show(d.show)

    def on_widget_created(self, ref):
        """ Using Snackbar.make returns async so we have to 
        initialize it later. 
        
        """
        d = self.declaration
        self.widget = Snackbar(__id__=ref)
        self.init_widget()

    def on_shown(self, view):
        d = self.declaration
        with self.widget.show.suppressed():
            d.show = True

    def on_dismissed(self, view, action):
        d = self.declaration
        with self.widget.dismiss.suppressed():
            d.show = False
            d.action(Snackbar.ACTIONS[action])
            if action==Snackbar.DISMISS_EVENT_SWIPE:
                #: Swiping destroys the widget and prevents reopening
                #: so create it again
                self.create_widget()

    def on_click(self, view):
        d = self.declaration
        d.show = False
        d.clicked()

    def _refresh_show(self, dt):
        """ While the `show` is true, keep calling .show() until the 
        duration `dt` expires.

        Parameters
        ------------
        dt: int
            Time left to keep showing

        """
        d = self.declaration
        if dt<=0:
            #: Done, hide
            d.show = False
        elif d.show:
            #: If user didn't cancel it, keep it alive
            self.widget.show()

            t = min(1000,dt)
            app = self.get_context()
            app.timed_call(t, self._refresh_show, dt-t)

    # -------------------------------------------------------------------------
    # ProxySnackbar API
    # -------------------------------------------------------------------------
    def set_text(self, text):
        self.widget.setText(text)

    def set_action_text(self, text):
        #: Only possible if a custom view is not used
        self.widget.setAction(text, self.widget.getId())

    def set_action_text_color(self, color):
        self.widget.setActionTextColor(color)

    def set_duration(self, duration):
        """ Android for whatever stupid reason doesn't let you set the time
        it only allows 1-long or 0-short. So we have to repeatedly call show
        until the duration expires, hence this method does nothing see 
        `set_show`.
        
        """
        if duration == 0:
            self.widget.setDuration(-2) #: Infinite
        else:
            self.widget.setDuration(0) #: Long

    def set_show(self, show):
        if show:
            d = self.declaration
            self.widget.show()

            #: If an infinite duration was not set
            if d.duration:
                app = self.get_context()
                t = min(1000,d.duration)
                app.timed_call(t, self._refresh_show, d.duration-t)
        else:
            self.widget.dismiss()
