"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Aug 25, 2017
"""

from atom.api import Typed
from enamlnative.widgets.button import ProxyButton
from .bridge import ObjcMethod, ObjcProperty
from .uikit_control import UIControl, UiKitControl


class UIButton(UIControl):
    """ """

    __signature__ = [{"buttonWithType": "enum"}]
    #: Properties
    on = ObjcProperty("bool")
    onTintColor = ObjcProperty("UIColor")
    tintColor = ObjcProperty("UIColor")
    thumbTintColor = ObjcProperty("UIColor")
    onImage = ObjcProperty("UIImage")
    offImage = ObjcProperty("UIImage")

    #: Methods
    setTitle = ObjcMethod("NSString", {"forState": "enum"})

    #: Type Enum
    UIButtonTypeCustom = 0
    UIButtonTypeSystem = 1
    UIButtonTypeDetailDisclosure = 2
    UIButtonTypeInfoLight = 3
    UIButtonTypeInfoDark = 4
    UIButtonTypeContactAdd = 5
    UIButtonTypeRoundedRect = UIButtonTypeSystem


class UiKitButton(UiKitControl, ProxyButton):
    """An UiKit implementation of an Enaml ProxyToolkitObject."""

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UIButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the toolkit widget for the proxy object."""
        d = self.declaration
        button_type = (
            UIButton.UIButtonTypeSystem if d.flat else UIButton.UIButtonTypeRoundedRect
        )
        self.widget = UIButton(buttonWithType=button_type)

    def init_widget(self):
        super().init_widget()
        self.init_text()

    # -------------------------------------------------------------------------
    # ProxyButton API
    # -------------------------------------------------------------------------
    def set_text(self, text: str):
        w = self.widget
        assert w is not None
        w.setTitle(text, forState=UIButton.UIControlStateNormal)

    def set_style(self, style):
        pass  #: Cannot be changed once set!
