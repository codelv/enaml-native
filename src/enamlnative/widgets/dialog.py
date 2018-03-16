"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Sept 21, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Bool, Event, observe, set_default
)

from enaml.core.declarative import d_
from enaml.widgets.toolkit_object import ToolkitObject, ProxyToolkitObject


class ProxyDialog(ProxyToolkitObject):
    """ The abstract definition of a proxy dialgo object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Dialog)

    def set_title(self, title):
        raise NotImplementedError

    def set_cancel_on_back(self, cancels):
        raise NotImplementedError

    def set_cancel_on_touch_outside(self, cancels):
        raise NotImplementedError

    def set_key_events(self, enabled):
        raise NotImplementedError

    def set_show(self, show):
        raise NotImplementedError

    def set_style(self, style):
        raise NotImplementedError


class Dialog(ToolkitObject):
    """ A popup dialog that may contain a view.
    
    """

    #: Sets whether this dialog is cancelable with the BACK key.
    cancel_on_back = d_(Bool(True))

    #: Sets whether this dialog is canceled when touched outside
    #: the window's bounds.
    cancel_on_touch_outside = d_(Bool(True))

    #: Listen for key events
    key_events = d_(Bool())

    #: Key event
    key_pressed = d_(Event(dict), writable=False)

    #: Set the title text for this dialog's window.
    title = d_(Unicode())

    #: Start the dialog and display it on screen (or hide if False)
    show = d_(Bool())

    #: Dialog style using the @style format
    #: (ex. @style/Theme_Light_NoTitleBar_Fullscreen
    style = d_(Unicode())

    #: A reference to the proxy object.
    proxy = Typed(ProxyDialog)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('cancel_on_back', 'cancel_on_touch_outside', 'key_events',
             'title', 'show', 'style')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(Dialog, self)._update_proxy(change)

    def popup(self):
        """ Show the dialog from code. This will initialize and activate
        if needed.
        
        Examples
        --------
        
        >>> enamldef AlertDialog(Dialog): dialog:
              attr result: lambda text: None
              TextView:
                text = "Are you sure you want to delete?"
              Button:
                text = "Yes"
                clicked ::
                  dialog.show = False
                  dialog.result(self.text)
              Button:
                text = "No"
                clicked ::
                  dialog.show = False
                  dialog.result(self.text)
            def on_result(value):
              print("User clicked: {}".format(value))
            AlertDialog(result=on_result).popup()
        
        Notes
        ------
        This does NOT block. Callbacks should be used to handle click events
        or the `show` state should be observed to know when it is closed.
         
        """
        if not self.is_initialized:
            self.initialize()
        if not self.proxy_is_active:
            self.activate_proxy()
        self.show = True




