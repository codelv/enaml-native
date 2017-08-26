'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
'''

from atom.api import Typed, set_default
from enamlnative.widgets.linear_layout import ProxyLinearLayout

from .bridge import ObjcMethod, ObjcProperty
from .uikit_view_group import UIView, UiKitViewGroup


class UIStackView(UIView):
    """ From:
        https://developer.apple.com/documentation/uikit/uistackview?language=objc
    """
    #: Properties
    axis = ObjcProperty('UILayoutConstraintAxis')
    #setProgress = ObjcMethod('float', dict(animated='boolean'))
    addArrangedSubview = ObjcMethod('UIView')
    insertArrangedSubview = ObjcMethod('UIView', dict(atIndex='NSInteger'))
    removeArrangedSubview = ObjcMethod('UIView')

    UILayoutConstraintAxisHorizontal = 0
    UILayoutConstraintAxisVertical = 1


class UiKitLinearLayout(UiKitViewGroup, ProxyLinearLayout):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit layout created by the proxy.
    layout = Typed(UIStackView)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_layout(self):
        """ Create the layout widget for arranging child proxy objects.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'layout' attribute.

        """
        self.layout = UIStackView()

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        widget = self.widget
        d = self.declaration
        super(UiKitLinearLayout, self).init_widget()
        if d.orientation != "horizontal":  #: Default is horizontal
            self.set_orientation(d.orientation)

    # def init_layout(self):
    #     """ Initialize the layout of the toolkit widget.
    #
    #      This method is called during the bottom-up pass. This method
    #      should initialize the layout of the widget. The child widgets
    #      will be fully initialized and layed out when this is called.
    #
    #      """
    #     widget = self.widget
    #     for child_widget in self.child_widgets():
    #         widget.addArrangedSubview(child_widget)
    #     super(UiKitLinearLayout, self).init_layout()
    #
    # def update_frame(self):
    #     """ Use parent size by default"""
    #     super(UiKitLinearLayout, self).update_frame()
    #     if not self.frame:
    #         self.frame = self.parent().frame

    # def child_added(self, child):
    #     """ Handle the child added event from the declaration.
    #
    #     This handler will unparent the child toolkit widget. Subclasses
    #     which need more control should reimplement this method.
    #
    #     """
    #     super(UiKitView, self).child_added(child)
    #     widget = self.widget
    #     #: TODO: Should index be cached?
    #     for i, child_widget in enumerate(self.child_widgets()):
    #         if child_widget == child.widget:
    #             widget.insertArrangedSubview(child_widget, atIndex=i)
    #
    # def child_removed(self, child):
    #     """ Handle the child removed event from the declaration.
    #
    #     The child must be both removed from the arrangement and removed normally.
    #
    #     """
    #     if child.widget is not None:
    #         self.widget.removeArrangedSubview(child.widget)
    #     super(UiKitLinearLayout, self).child_removed(child)

    # --------------------------------------------------------------------------
    # ProxyLinearLayout API
    # --------------------------------------------------------------------------
    def set_orientation(self, orientation):
        if orientation == 'horizontal':
            self.layout.axis = UIStackView.UILayoutConstraintAxisHorizontal
        else:
            self.layout.axis = UIStackView.UILayoutConstraintAxisVertical
