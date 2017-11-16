"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""

from atom.api import Instance, observe
from enamlnative.widgets.view_group import ProxyViewGroup

from .uikit_view import UIView, UiKitView


class UiKitViewGroup(UiKitView, ProxyViewGroup):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    layout = Instance(UIView)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'widget' attribute.

        """
        super(UiKitViewGroup, self).create_widget()
        self.create_layout()

    def create_layout(self):
        """ Create the layout widget for arranging child proxy objects.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'layout' attribute.

        """
        raise NotImplementedError

    def init_layout(self):
        """ Initialize the layout of the toolkit widget.

         This method is called during the bottom-up pass. This method
         should initialize the layout of the widget. The child widgets
         will be fully initialized and layed out when this is called.

         This

         """
        layout = self.layout
        #: Add the layout as a subview
        self.widget.addSubview(layout)

        #: Add all child widgets to the layout
        for child_widget in self.child_widgets():
            layout.addArrangedSubview(child_widget)
            #layout.addSubview(child_widget)
        #super(UiKitViewGroup, self).init_layout()

    # def update_frame(self):
    #     """ Use parent size by default"""
    #     super(UiKitViewGroup, self).update_frame()
    #     if not self.frame:
    #         d = self.declaration
    #         if d.parent and not (d.x or d.y or d.width or d.height):
    #             d.width, d.height = d.parent.width, d.parent.height
    #         self.frame = (d.x,d.y,d.width,d.height)

    def child_added(self, child):
        """ Handle the child added event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super(UiKitView, self).child_added(child)

        layout = self.layout
        for i, child_widget in enumerate(self.child_widgets()):
            if child_widget == child.widget:
                layout.insertArrangedSubview(child_widget, atIndex=i)
                layout.insertSubview(child_widget, atIndex=i)

    def child_removed(self, child):
        """ Handle the child removed event from the declaration.

        The child must be both removed from the arrangement and removed 
        normally.

        """
        layout = self.layout
        if child.widget is not None:
            layout.removeArrangedSubview(child.widget)
            layout.removeSubview(child.widget)
        #super(UiKitViewGroup, self).child_removed(child)

    def destroy(self):
        """ A reimplemented destructor that destroys the layout widget.

        """
        layout = self.layout
        if layout is not None:
            layout.removeFromSuperview()
            self.layout = None
        super(UiKitViewGroup, self).destroy()

    # -------------------------------------------------------------------------
    # ProxyViewGroup API
    # -------------------------------------------------------------------------
    @observe('frame')
    def set_frame(self, change):
        if self.frame:
           self.widget.frame = self.frame
           self.layout.frame = self.frame