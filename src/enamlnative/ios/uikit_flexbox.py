"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""

from atom.api import Typed, set_default
from enamlnative.widgets.flexbox import ProxyFlexbox

from .uikit_view import UIView, UiKitView
from .yoga import Yoga


class UIFlexbox(UIView):
    """ Adds yoga as a nested object
    """
    __nativeclass__ = set_default("UIView")


class UiKitFlexbox(UiKitView, ProxyFlexbox):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit layout created by the proxy.
    widget = Typed(UIFlexbox)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        self.widget = UIFlexbox()

    def init_layout(self):
        super(UiKitFlexbox, self).init_layout()

        if self.parent() is None:
            self.widget.yoga.applyLayoutPreservingOrigin(True)

    # -------------------------------------------------------------------------
    # ProxyFlexbox API
    # -------------------------------------------------------------------------
    def set_align_content(self, alignment):
        self.widget.yoga.alignContent = Yoga.ALIGN_CONTENT[alignment]

    def set_align_items(self, alignment):
        self.widget.yoga.alignItems = Yoga.ALIGN_ITEMS[alignment]

    def set_flex_direction(self, direction):
        self.widget.yoga.flexDirection = Yoga.FLEX_DIRECTION[direction]

    def set_flex_wrap(self, wrap):
        self.widget.flexWrap = Yoga.FLEX_WRAP[wrap]

    def set_justify_content(self, justify):
        self.widget.yoga.justifyContent = Yoga.JUSTIFY_CONTENT[justify]

