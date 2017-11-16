"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""

from atom.api import Typed
from enamlnative.widgets.scroll_view import ProxyScrollView

from .bridge import ObjcMethod, ObjcProperty
from .uikit_view import UIView, UiKitView


class UIScrollView(UIView):
    #: Properties
    contentSize = ObjcProperty('CGSize')

    #: Added by UIScrollView+AutoResize
    fitToContents = ObjcMethod()
    # axis = ObjcProperty('UILayoutConstraintAxis')
    # #setProgress = ObjcMethod('float', dict(animated='bool'))
    # addArrangedSubview = ObjcMethod('UIView')
    # insertArrangedSubview = ObjcMethod('UIView', dict(atIndex='NSInteger'))
    # removeArrangedSubview = ObjcMethod('UIView')
    #
    # UILayoutConstraintAxisHorizontal = 0
    # UILayoutConstraintAxisVertical = 1


class UiKitScrollView(UiKitView, ProxyScrollView):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit layout created by the proxy.
    widget = Typed(UIScrollView)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the widget

        """
        self.widget = UIScrollView()

    # def update_frame(self):
    #     """ """
    #     super
    #     # d = self.declaration
    #     # if not (d.x or d.y or d.width or d.height):
    #     #     d.width, d.height = d.parent.width, d.parent.height
    #     # self.frame = (d.x,d.y,d.width,d.height)

    def init_layout(self):
        super(UiKitScrollView, self).init_layout()
        for c in self.children():
            if c.frame:
                self.widget.contentSize = c.frame[-2:]
                return

        self.widget.fitToContents()

    # -------------------------------------------------------------------------
    # ProxyScrollView API
    # -------------------------------------------------------------------------
    # def set_frame(self, change):
    #     super(UiKitScrollView, self).set_frame(change)
    #     d = self.declaration
    #     self.widget.contentSize = (d.width, d.height)

    def set_orientation(self, orientation):
        #: TODO: Cannot enforce direction that I'm aware of
        #: (but can lock direction)
        pass

    def set_scroll_by(self, delta):
        raise NotImplementedError

    def set_scroll_to(self, point):
        raise NotImplementedError