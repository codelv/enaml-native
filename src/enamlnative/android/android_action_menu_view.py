"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 7, 2017
"""
from atom.api import Typed
from enaml.application import deferred_call
from enamlnative.widgets.action_menu_view import ProxyActionMenuView
from .android_linear_layout import AndroidLinearLayout, LinearLayout
from .android_image_view import Drawable
from .bridge import JavaBridgeObject, JavaCallback, JavaMethod


class Menu(JavaBridgeObject):
    __nativeclass__ = "android.view.Menu"

    def __init__(self):
        #: Menu is an Interface, we can't create it
        super().__init__()


class MenuItem(JavaBridgeObject):
    __nativeclass__ = "android.view.MenuItem"


class ActionMenuView(LinearLayout):
    package = "androidx.appcompat.widget"
    __nativeclass__ = f"{package}.ActionMenuView"
    getMenu = JavaMethod(returns=Menu)
    showOverflowMenu = JavaMethod()
    hideOverflowMenu = JavaMethod()
    setOverflowIcon = JavaMethod(Drawable)
    setOnMenuItemClickListener = JavaMethod(
        f"{package}.ActionMenuView$OnMenuItemClickListener"
    )
    onMenuItemClick = JavaCallback(MenuItem, returns=bool)


class AndroidActionMenuView(AndroidLinearLayout, ProxyActionMenuView):
    """An Android implementation of an Enaml ProxyActionMenuView."""

    #: A reference to the widget created by the proxy.
    widget = Typed(ActionMenuView)

    #: Menu created
    menu = Typed(Menu)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget."""
        self.widget = ActionMenuView(self.get_context())

    def init_widget(self):
        """Initialize the underlying widget."""
        super().init_widget()
        w = self.widget

        #: Kinda hackish, but when we get the menu back, load it
        deferred_call(self.init_menu)
        w.setOnMenuItemClickListener(w.getId())
        w.onMenuItemClick.connect(self.on_menu_item_click)

    async def init_menu(self):
        self.menu = await self.widget.getMenu()

    # -------------------------------------------------------------------------
    # OnMenuItemClickListener API
    # -------------------------------------------------------------------------
    def on_menu_item_click(self, item):
        return False

    # -------------------------------------------------------------------------
    # ProxyActionMenuView API
    # -------------------------------------------------------------------------
    def set_opened(self, opened: bool):
        w = self.widget
        assert w is not None
        if opened:
            w.showOverflowMenu()
        else:
            w.hideOverflowMenu()
