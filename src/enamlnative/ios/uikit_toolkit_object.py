"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed
from enaml.widgets.toolkit_object import ProxyToolkitObject

from .bridge import ObjcBridgeObject


class UiKitToolkitObject(ProxyToolkitObject):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(ObjcBridgeObject)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'widget' attribute.

        """
        self.widget = ObjcBridgeObject()

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        widget = self.widget

    def init_layout(self):
        """ Initialize the layout of the toolkit widget.

        This method is called during the bottom-up pass. This method
        should initialize the layout of the widget. The child widgets
        will be fully initialized and layed out when this is called.

        """
        pass

    def get_app(self):
        """ Get the app of the View.

        """
        from .app import IPhoneApplication
        return IPhoneApplication.instance()

    # -------------------------------------------------------------------------
    # ProxyToolkitObject API
    # -------------------------------------------------------------------------
    def activate_top_down(self):
        """ Activate the proxy for the top-down pass.

        """
        self.create_widget()
        self.init_widget()

    def activate_bottom_up(self):
        """ Activate the proxy tree for the bottom-up pass.

        """
        self.init_layout()

    def destroy(self):
        """ A reimplemented destructor.

        This destructor will clear the reference to the toolkit widget
        and set its parent to None.

        """
        widget = self.widget
        if widget is not None:
            del self.widget
        super(UiKitToolkitObject, self).destroy()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------
    def parent_widget(self):
        """ Get the parent toolkit widget for this object.

        Returns
        -------
        result : ObjcBridgeObject or None
            The toolkit widget declared on the declaration parent, or
            None if there is no such parent.

        """
        parent = self.parent()
        if parent is not None:
            return parent.widget

    def child_widgets(self):
        """ Get the child toolkit widgets for this object.

        Returns
        -------
        result : iterable of ObjcBridgeObjects
            The child widgets defined for this object.

        """
        for child in self.children():
            if child is not None:  #: Not sure how this happens
                w = child.widget
                if w is not None:
                    yield w
