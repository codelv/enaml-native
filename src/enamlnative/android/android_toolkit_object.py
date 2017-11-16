"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed
from enaml.widgets.toolkit_object import ProxyToolkitObject

from .bridge import JavaBridgeObject


class AndroidToolkitObject(ProxyToolkitObject):
    """ An Android implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(JavaBridgeObject)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'widget' attribute.

        """
        self.widget = JavaBridgeObject(self.get_context())

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

    def get_context(self):
        """ Get the context of the View.

        """
        from .app import AndroidApplication
        return AndroidApplication.instance()

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
            parent = self.parent_widget()
            if parent is not None:
                parent.removeView(widget)
            del self.widget
        super(AndroidToolkitObject, self).destroy()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------
    def parent_widget(self):
        """ Get the parent toolkit widget for this object.

        Returns
        -------
        result : JavaClass or None
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
        result : iterable of JavaClass
            The child widgets defined for this object.

        """
        for child in self.children():
            if child is not None: #: Not sure how this happens
                w = child.widget
                if w is not None:
                    yield w
