'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
'''

from atom.api import Typed, set_default
from enamlnative.widgets.text_view import ProxyTextView

from .bridge import ObjcMethod, ObjcProperty
from .uikit_view import UIView, UiKitView


class UILabel(UIView):
    """ From:
        https://developer.apple.com/documentation/uikit/uiview?language=objc
    """
    #: Properties
    text = ObjcProperty('NSString')
    textColor = ObjcProperty('UIColor')


class UiKitTextView(UiKitView, ProxyTextView):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UILabel)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        """
        self.widget = UILabel()#initWithFrame=(91,35,200,20))

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        super(UiKitTextView, self).init_widget()

        widget = self.widget
        d = self.declaration

        if d.text:
            self.set_text(d.text)
        if d.text_color:
            self.set_text_color(d.text_color)

    # --------------------------------------------------------------------------
    # ProxyTextView API
    # --------------------------------------------------------------------------
    def set_text(self, text):
        self.widget.text = text

    def set_text_color(self, color):
        self.widget.textColor = color