"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""

from atom.api import Typed, set_default
from enamlnative.widgets.progress_bar import ProxyProgressBar

from .bridge import ObjcMethod, ObjcProperty
from .uikit_view import UIView, UiKitView


class UIProgressView(UIView):
    """ From:
        https://developer.apple.com/documentation/uikit/uiview?language=objc
    """
    #: Properties
    progress = ObjcProperty('float')
    setProgress = ObjcMethod('float', dict(animated='bool'))


class UiKitProgressView(UiKitView, ProxyProgressBar):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UIProgressView)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        """
        self.widget = UIProgressView()

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        super(UiKitProgressView, self).init_widget()

        d = self.declaration
        if d.progress:
            self.set_progress(d.progress)

    # -------------------------------------------------------------------------
    # ProxyProgressBar API
    # -------------------------------------------------------------------------
    def set_progress(self, progress):
        self.widget.progress = progress/100.0