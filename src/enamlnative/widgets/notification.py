"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Sept 21, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode, Dict, Bool, Int, Event, Enum, observe,
    set_default
)

from enaml.core.declarative import d_
from enaml.widgets.toolkit_object import ToolkitObject, ProxyToolkitObject


class ProxyNotification(ProxyToolkitObject):
    """ The abstract definition of a proxy dialgo object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Notification)

    def set_channel_id(self, channel_id):
        raise NotImplementedError

    def set_color(self, color):
        raise NotImplementedError

    def set_priority(self, priority):
        raise NotImplementedError

    def set_title(self, title):
        raise NotImplementedError

    def set_text(self, text):
        raise NotImplementedError

    def set_sub_text(self, sub_text):
        raise NotImplementedError

    def set_info(self, info):
        raise NotImplementedError

    def set_show(self, show):
        raise NotImplementedError

    def set_show_progress(self, show):
        raise NotImplementedError

    def set_progress(self, progress):
        raise NotImplementedError

    def set_progress_indeterminate(self, indeterminate):
        raise NotImplementedError

    def set_style(self, style):
        raise NotImplementedError

    def set_settings(self, settings):
        raise NotImplementedError


class Notification(ToolkitObject):
    """ A notification that may contain a view.
    
    """
    #: Set the channel ID
    channel_id = d_(Unicode('default'))

    #: Set the title (first row) of the notification, in a standard
    #: notification.
    title = d_(Unicode())

    #: Set the text (second row) of the notification, in a standard
    #: notification.
    text = d_(Unicode())

    #: Set the large text at the right-hand side of the notification.
    info = d_(Unicode())

    #: Set the small icon to use in the notification layouts.
    icon = d_(Unicode())

    #: Sets color.
    color = d_(Unicode())

    #: Start the dialog and display it on screen (or hide if False)
    show = d_(Bool())

    #: Set the priority or importance
    priority = d_(Enum('normal', 'low', 'high'))

    #: Progress
    progress = d_(Int())

    #: Show an indeterminate progress bar
    progress_indeterminate = d_(Bool())

    #: Show a progress bar
    show_progress = d_(Bool())

    #: Notification style using the @style format
    #: (ex. @style/Theme_Light_NoTitleBar_Fullscreen
    style = d_(Unicode())

    #: Extra notification settings
    settings = d_(Dict())

    #: Clicked event
    clicked = d_(Event(), writable=False)

    #: A reference to the proxy object.
    proxy = Typed(ProxyNotification)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('channel_id', 'title', 'text', 'info', 'sub_text', 'color',
             'progress', 'show_progress', 'progress_indeterminate', 'priority',
             'show', 'style', 'settings')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(Notification, self)._update_proxy(change)

    def popup(self):
        """ Show the notification from code. This will initialize and activate
        if needed.
        
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




