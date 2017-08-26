'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 25, 2017

@author: jrm
'''

from atom.api import Typed, set_default
from enamlnative.widgets.button import ProxyButton

from .bridge import ObjcMethod, ObjcProperty
from .uikit_control import UIControl, UiKitControl


class UIButton(UIControl):
    """
    """
    __signature__ = set_default(dict(buttonWithType="UIButtonType"))
    #: Properties
    on = ObjcProperty('boolean')
    onTintColor = ObjcProperty('UIColor')
    tintColor = ObjcProperty('UIColor')
    thumbTintColor = ObjcProperty('UIColor')
    onImage = ObjcProperty('UIImage')
    offImage = ObjcProperty('UIImage')

    #: Methods
    setTitle = ObjcMethod('NSString', dict(forState='UIControlState'))

    UIButtonTypeCustom = 0
    UIButtonTypeSystem = 1
    UIButtonTypeDetailDisclosure = 2
    UIButtonTypeInfoLight = 3
    UIButtonTypeInfoDark = 4
    UIButtonTypeContactAdd = 5
    UIButtonTypeRoundedRect = UIButtonTypeSystem

    UIControlStateNormal = 0
    UIControlStateHighlighted = 1 << 0
    UIControlStateDisabled = 1 << 1
    UIControlStateSelected = 1 << 2
    UIControlStateFocused = 1 << 3
    UIControlStateApplication = 0x00FF0000
    UIControlStateReserved = 0xFF000000


class UiKitButton(UiKitControl, ProxyButton):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UIButton)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        """
        d = self.declaration
        button_type = {
            '': UIButton.UIButtonTypeRoundedRect,
            'borderless': UIButton.UIButtonTypeSystem,
            'inset': UIButton.UIButtonTypeSystem,
            'small': UIButton.UIButtonTypeSystem
        }[d.styles]
        self.widget = UIButton(buttonWithType=button_type)

    # --------------------------------------------------------------------------
    # ProxyButton API
    # --------------------------------------------------------------------------
    def set_style(self, style):
        pass #: Cannot be changed once set!