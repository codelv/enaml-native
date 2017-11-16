"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Sept 18, 2017

@author: jrm
"""
from atom.api import Typed, Bool, set_default
from .bridge import JavaBridgeObject, JavaMethod, JavaStaticMethod
from enamlnative.widgets.toast import ProxyToast
from .android_toolkit_object import AndroidToolkitObject
from .android_text_view import Gravity


class Toast(JavaBridgeObject):
    #: Show the view for the specified duration.
    __nativeclass__ = set_default('android.widget.Toast')
    __signature__ = set_default(('android.content.Context',))
    makeText = JavaStaticMethod('android.content.Context',
                                'java.lang.CharSequence', 'int',
                                returns='android.widget.Toast')
    show = JavaMethod()
    cancel = JavaMethod()
    setDuration = JavaMethod('int')
    setGravity = JavaMethod('int', 'int', 'int')
    setText = JavaMethod('java.lang.CharSequence')
    setView = JavaMethod('android.view.View')


class AndroidToast(AndroidToolkitObject, ProxyToast):
    """ An Android implementation of an Enaml ProxyToast.

    """
    #: A reference to the widget created by the proxy.
    toast = Typed(Toast)

    #: Made toast
    #: Android doesn't let us simply update the text of an existing toast
    #: unless it was created with "makeToast"
    made_toast = Bool()

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        A toast is not a subclass of view, hence we don't set name as widget
        or children will try to use it as their parent (which crashes).

        """
        d = self.declaration
        if d.text:
            Toast.makeText(self.get_context(),
                           d.text, 1).then(self.on_make_toast)
            self.made_toast = True
        else:
            self.toast = Toast(self.get_context())

    def init_widget(self):
        """ Our widget may not exist yet so we have to diverge from the normal 
        way of doing initialization. See `update_widget`
        
        """
        super(AndroidToast, self).init_widget()
        if not self.toast:
            return

        d = self.declaration
        if not self.made_toast:
            #: Set it to LONG
            self.toast.setDuration(1)
        #if d.position:
        #    self.set_position(d.position)
        if d.show:
            self.set_show(d.show)

    def init_layout(self):
        """ If a view is given show it """
        super(AndroidToast, self).init_layout()
        if not self.made_toast:
            for view in self.child_widgets():
                self.toast.setView(view)
                break

    def child_added(self, child):
        """ Overwrite the view """
        view = child.widget
        if view is not None:
            self.toast.setView(view)

    def on_make_toast(self, ref):
        """ Using Toast.makeToast returns async so we have to initialize it 
        later. 
        
        """
        d = self.declaration
        self.toast = Toast(__id__=ref)
        self.init_widget()

    def _refresh_show(self, dt):
        """ While the toast.show is true, keep calling .show() until the 
        duration `dt` expires.

        Parameters
        ------------
        dt: int
            Time left to keep showing

        """
        d = self.declaration
        if dt <= 0:
            #: Done, hide
            d.show = False
        elif d.show:
            #: If user didn't cancel it, keep it alive
            self.toast.show()

            t = min(1000, dt)
            app = self.get_context()
            app.timed_call(t, self._refresh_show, dt-t)

    # -------------------------------------------------------------------------
    # ProxyToast API
    # -------------------------------------------------------------------------
    def set_text(self, text):
        #: Only possible if a custom view is not used
        if self.made_toast:
            self.toast.setText(text)

    def set_duration(self, duration):
        """ Android for whatever stupid reason doesn't let you set the time
        it only allows 1-long or 0-short. So we have to repeatedly call show
        until the duration expires, hence this method does nothing see 
        `set_show`.
        
        """
        pass

    def set_show(self, show):
        if show:
            d = self.declaration
            self.toast.show()

            #: Get app
            app = self.get_context()
            t = min(1000, d.duration)
            app.timed_call(t, self._refresh_show, d.duration-t)
        else:
            self.toast.cancel()

    def set_position(self, position):
        #: TODO: Handle x,y offsets
        self.toast.setGravity(Gravity.parse(position), 0, 0)