"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 7, 2017

@author: jrm
"""
from atom.api import Atom, Typed, set_default

from enamlnative.widgets.action_menu_view import ProxyActionMenuView

from .android_linear_layout import AndroidLinearLayout, LinearLayout
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class ActionMenuView(LinearLayout):
    __nativeclass__ = set_default('android.support.v7.widget.ActionMenuView')
    getMenu = JavaMethod()
    showOverflowMenu = JavaMethod()
    hideOverflowMenu = JavaMethod()
    setOverflowIcon = JavaMethod('android.graphics.drawable')
    setOnMenuItemClickListener = JavaMethod(
        'android.support.v7.widget.ActionMenuView$OnMenuItemClickListener')

    onMenuItemClick = JavaCallback('android.view.MenuItem', returns='boolean')


class Menu(JavaBridgeObject):
    __nativeclass__ = set_default('android.view.Menu')

    def __init__(self):
        #: Menu is an Interface, we can't create it
        super(Atom, self).__init__()



class MenuItem(JavaBridgeObject):
    __nativeclass__ = set_default('android.view.MenuItem')


class AndroidActionMenuView(AndroidLinearLayout, ProxyActionMenuView):
    """ An Android implementation of an Enaml ProxyActionMenuView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ActionMenuView)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ActionMenuView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidActionMenuView, self).init_widget()
        d = self.declaration

        #: Kinda hackish, but when we get the menu back, load it
        self.widget.getMenu().then(self.on_menu)
        self.widget.setOnMenuItemClickListener(self.widget.getId())
        self.widget.onMenuItemClick.connect(self.on_menu_item_click)


    def on_menu(self, menu):
        """ """
        # This is just an id?
        Menu(menu)
        pass

    # -------------------------------------------------------------------------
    # OnMenuItemClickListener API
    # -------------------------------------------------------------------------
    def on_menu_item_click(self, item):

        return False

    # -------------------------------------------------------------------------
    # ProxyActionMenuView API
    # -------------------------------------------------------------------------
    def set_opened(self, opened):
        if opened:
           self.widget.showOverflowMenu()
        else:
            self.widget.hideOverflowMenu()