'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 25, 2017

@author: jrm
'''

from atom.api import Typed

from enamlnative.widgets.compound_button import ProxyCompoundButton

from .bridge import ObjcMethod, ObjcProperty
from .uikit_view import UIView, UiKitView


class UIControl(UIView):

    #: Properties
    enabled = ObjcProperty('boolean')
    selected = ObjcProperty('boolean')
    highlighted = ObjcProperty('boolean')
    contentVerticalAlignment = ObjcProperty('UIControlContentVerticalAlignment')
    contentHorizontalAlignment = ObjcProperty('UIControlContentHorizontalAlignment')

    #setProgress = ObjcMethod('float', dict(animated='boolean'))
    addTarget = ObjcMethod('id',
                           dict(action="SEL"),
                           dict(forControlEvents="UIControlEvents"))

    #: UIControlEvents enum
    UIControlEventTouchDown = 1 << 0
    UIControlEventTouchDownRepeat = 1 << 1
    UIControlEventTouchDragInside = 1 << 2
    UIControlEventTouchDragOutside = 1 << 3
    UIControlEventTouchDragEnter = 1 << 4
    UIControlEventTouchDragExit = 1 << 5
    UIControlEventTouchUpInside = 1 << 6
    UIControlEventTouchUpOutside = 1 << 7
    UIControlEventTouchCancel = 1 << 8
    UIControlEventValueChanged = 1 << 12
    UIControlEventPrimaryActionTriggered = 1 << 13
    UIControlEventEditingDidBegin = 1 << 16
    UIControlEventEditingChanged = 1 << 17
    UIControlEventEditingDidEnd = 1 << 18
    UIControlEventEditingDidEndOnExit = 1 << 19
    UIControlEventAllTouchEvents = 0x00000FFF
    UIControlEventAllEditingEvents = 0x000F0000
    UIControlEventApplicationReserved = 0x0F000000
    UIControlEventSystemReserved = 0xF0000000
    UIControlEventAllEvents = 0xFFFFFFFF


class UiKitControl(UiKitView, ProxyCompoundButton):
    """ A UiKitControl helper class.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UIControl)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        """
        self.widget = UIControl()

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        super(UiKitControl, self).init_widget()

        d = self.declaration
        if d.checked:
            self.set_checked(d.checked)