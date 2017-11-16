"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""

from atom.api import Typed
from enamlnative.widgets.activity_indicator import ProxyActivityIndicator

from .bridge import ObjcMethod, ObjcProperty
from .uikit_view import UIView, UiKitView


class UIActivityIndicatorView(UIView):
    #: Properties
    color = ObjcProperty('UIColor')
    activityIndicatorViewStyle = ObjcProperty('UIActivityIndicatorViewStyle')
    startAnimating = ObjcMethod()
    stopAnimating = ObjcMethod()


class UiKitActivityIndicator(UiKitView, ProxyActivityIndicator):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UIActivityIndicatorView)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        """
        self.widget = UIActivityIndicatorView()

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        super(UiKitActivityIndicator, self).init_widget()

        d = self.declaration
        if d.style != 'normal':
            self.set_style(d.style)
        if d.color:
            self.set_color(d.color)

        #: Why would you want to stop an activity indicator?
        self.widget.startAnimating()

    # -------------------------------------------------------------------------
    # ProxyActivityIndicator API
    # -------------------------------------------------------------------------
    def set_style(self, style):
        pass
        #self.widget.activityIndicatorViewStyle = style

    def set_color(self, color):
        self.widget.color = color