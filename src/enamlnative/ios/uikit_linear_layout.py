"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""

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
    #setProgress = ObjcMethod('float', dict(animated='bool'))
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

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
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
        super(UiKitLinearLayout, self).init_widget()
        d = self.declaration
        if d.orientation != "horizontal":  #: Default is horizontal
            self.set_orientation(d.orientation)

    # -------------------------------------------------------------------------
    # ProxyLinearLayout API
    # -------------------------------------------------------------------------
    def set_orientation(self, orientation):
        if orientation == 'horizontal':
            self.layout.axis = UIStackView.UILayoutConstraintAxisHorizontal
        else:
            self.layout.axis = UIStackView.UILayoutConstraintAxisVertical
