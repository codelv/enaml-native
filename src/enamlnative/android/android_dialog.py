"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Sept 21, 2017

@author: jrm
"""
from atom.api import Typed, set_default
from enamlnative.android.bridge import JavaBridgeObject, JavaMethod, JavaCallback
from enamlnative.android.android_toolkit_object import AndroidToolkitObject
from enamlnative.widgets.dialog import ProxyDialog


class Dialog(JavaBridgeObject):
    #: Show the view for the specified duration.
    __nativeclass__ = set_default('android.app.Dialog')
    __signature__ = set_default(('android.content.Context', 'android.R'))
    show = JavaMethod()
    dismiss = JavaMethod()
    setCancelable = JavaMethod('boolean')
    setCanceledOnTouchOutside = JavaMethod('boolean')
    setContentView = JavaMethod('android.view.View')
    setTitle = JavaMethod('java.lang.CharSequence')

    setOnDismissListener = JavaMethod(
        'android.content.DialogInterface$OnDismissListener')
    onDismiss = JavaCallback('android.app.Dialog')

    setOnCancelListener = JavaMethod(
        'android.content.DialogInterface$OnCancelListener')
    onCancel = JavaCallback('android.app.Dialog')

    setOnKeyListener = JavaMethod(
        'android.content.DialogInterface$OnKeyListener')
    onKey = JavaCallback('android.app.Dialog', 'int', 'android.view.KeyEvent')


class AndroidDialog(AndroidToolkitObject, ProxyDialog):
    """ An Android implementation of an Enaml ProxyDialog.

    """

    #: A reference to the widget created by the proxy.
    dialog = Typed(Dialog)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        A dialog is not a subclass of view, hence we don't set name as widget
        or children will try to use it as their parent.

        """
        d = self.declaration
        self.dialog = Dialog(self.get_context(), d.style)

    def init_widget(self):
        """
        """
        super(AndroidDialog, self).init_widget()

        #: Bind our listener

        d = self.declaration
        if d.title:
            self.set_title(d.title)
        if not d.cancel_on_back:
            self.set_cancel_on_back(d.cancel_on_back)
        if not d.cancel_on_touch_outside:
            self.set_cancel_on_touch_outside(d.cancel_on_touch_outside)
        if d.key_events:
            self.set_key_events(d.key_events)

        #: Listen for events
        self.dialog.setOnDismissListener(self.dialog.getId())
        self.dialog.onDismiss.connect(self.on_dismiss)

        self.dialog.setOnCancelListener(self.dialog.getId())
        self.dialog.onCancel.connect(self.on_cancel)

    def init_layout(self):
        """ If a view is given show it 
        
        """
        super(AndroidDialog, self).init_layout()

        #: Set the content
        for view in self.child_widgets():
            self.dialog.setContentView(view)
            break

        #: Show it if needed
        d = self.declaration
        if d.show:
            self.set_show(d.show)

    def child_added(self, child):
        """ Overwrite the content view """
        view = child.widget
        if view is not None:
            self.dialog.setContentView(view)
            
    def destroy(self):
        """ A reimplemented destructor that cancels 
        the dialog before destroying. 
        
        """
        dialog = self.dialog
        if dialog:
            #: Clear the dismiss listener
            #: (or we get an error during the callback)
            dialog.setOnDismissListener(None)
            dialog.dismiss()
            del self.dialog
        super(AndroidDialog, self).destroy()

    # -------------------------------------------------------------------------
    # Dialog API
    # -------------------------------------------------------------------------
    def on_cancel(self, dialog):
        d = self.declaration
        with self.dialog.show.suppressed():
            d.show = False

    def on_dismiss(self, dialog):
        d = self.declaration
        with self.dialog.show.suppressed():
            d.show = False

    # -------------------------------------------------------------------------
    # OnKeyListener API
    # -------------------------------------------------------------------------
    def on_key(self, dialog, key, event):
        """ Trigger the key event

        Parameters
        ----------
        view: int
            The ID of the view that sent this event
        key: int
            The code of the key that was pressed
        data: bytes
            The msgpack encoded key event

        """
        d = self.declaration
        r = {'key': key, 'result': False}
        d.key_event(r)
        return r['result']

    # -------------------------------------------------------------------------
    # ProxyDialog API
    # -------------------------------------------------------------------------
    def set_title(self, title):
        self.dialog.setTitle(title)

    def set_cancel_on_back(self, cancels):
        self.dialog.setCancelable(cancels)

    def set_cancel_on_touch_outside(self, cancels):
        self.dialog.setCanceledOnTouchOutside(cancels)

    def set_key_events(self, enabled):
        self.dialog.setOnKeyListener(self.dialog.getId() if enabled else None)
        if enabled:
            self.dialog.onKey.connect(self.on_key)

    def set_show(self, show):
        if show:
            d = self.declaration
            self.dialog.show()
        else:
            self.dialog.dismiss()

    def set_style(self, style):
        d = self.declaration
        if d.show:
            self.dialog.dismiss()

        #: Recreate dialog with new style
        self.create_widget()
        self.init_widget()
        self.init_layout()