"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 25, 2017

@author: jrm
"""

from atom.api import Typed

from enamlnative.widgets.compound_button import ProxyCompoundButton

from .bridge import ObjcMethod, ObjcProperty, ObjcCallback
from .uikit_text_view import UITextView, UiKitTextView


class UIControl(UITextView):

    #: Properties
    enabled = ObjcProperty('bool')
    selected = ObjcProperty('bool')
    highlighted = ObjcProperty('bool')
    contentVerticalAlignment = ObjcProperty(
        'UIControlContentVerticalAlignment')
    contentHorizontalAlignment = ObjcProperty(
        'UIControlContentHorizontalAlignment')

    #setProgress = ObjcMethod('float', dict(animated='bool'))
    addTarget = ObjcMethod('id',
                           dict(action="SEL"),
                           dict(forControlEvents="enum"))#""UIControlEvents"))

    onClicked = ObjcCallback()

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

    UIControlStateNormal = 0
    UIControlStateHighlighted = 1 << 0
    UIControlStateDisabled = 1 << 1
    UIControlStateSelected = 1 << 2
    UIControlStateFocused = 1 << 3
    UIControlStateApplication = 0x00FF0000
    UIControlStateReserved = 0xFF000000


class UiKitControl(UiKitTextView, ProxyCompoundButton):
    """ A UiKitControl helper class.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UIControl)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        
        """
        self.widget = UIControl()

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        Note: This does NOT initialize text properties by default!

        """
        super(UiKitControl, self).init_widget()

        d = self.declaration
        if d.clickable:
            #: A really ugly way to add the target
            #: would be nice if we could just pass the block pointer here :)
            self.get_app().bridge.addTarget(
                self.widget,
                forControlEvents=UIControl.UIControlEventTouchUpInside,
                andCallback=self.widget.getId(),
                usingMethod="onClicked",
                withValues=[]
            )

            self.widget.onClicked.connect(self.on_clicked)

    # -------------------------------------------------------------------------
    # Clicked API
    # -------------------------------------------------------------------------
    def on_clicked(self):
        d = self.declaration
        d.clicked()

