"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 25, 2017

@author: jrm
"""

from atom.api import Typed
from enamlnative.widgets.edit_text import ProxyEditText

from .bridge import ObjcMethod, ObjcProperty, ObjcCallback, NestedBridgeObject
from .uikit_control import UIControl, UiKitControl


class UIKeyboard(NestedBridgeObject):

    UIKeyboardTypeDefault = 0
    UIKeyboardTypeASCIICapable = 1
    UIKeyboardTypeNumbersAndPunctuation = 2
    UIKeyboardTypeURL = 3
    UIKeyboardTypeNumberPad = 4
    UIKeyboardTypePhonePad = 5
    UIKeyboardTypeNamePhonePad = 6
    UIKeyboardTypeEmailAddress = 7
    UIKeyboardTypeDecimalPad = 8
    UIKeyboardTypeTwitter = 9
    UIKeyboardTypeWebSearch = 10
    UIKeyboardTypeASCIICapableNumberPad = 11
    UIKeyboardTypeAlphabet = UIKeyboardTypeASCIICapable



class UITextField(UIControl):
    """
    """
    #: Properties
    placeholder = ObjcProperty('NSString')

    #:
    borderStyle = ObjcProperty('enum')  # UITextBorderStyle

    #: Callback
    onValueChanged = ObjcCallback('NSString')

    UITextBorderStyleNone = 0
    UITextBorderStyleLine = 1
    UITextBorderStyleBezel = 2
    UITextBorderStyleRoundedRect = 3

    STYLES = {
        '': UITextBorderStyleNone,
        'line': UITextBorderStyleLine,
        'bezel': UITextBorderStyleBezel,
        'rounded_rect': UITextBorderStyleRoundedRect
    }


class UiKitEditText(UiKitControl, ProxyEditText):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UITextField)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        """
        self.widget = UITextField()

    def init_widget(self):
        """ Bind the on property to the checked state """
        super(UiKitEditText, self).init_widget()

        #: Init font properties etc...
        self.init_text()

        d = self.declaration
        if d.placeholder:
            self.set_placeholder(d.placeholder)
        if d.input_type != 'text':
            self.set_input_type(d.input_type)
        if d.style:
            self.set_style(d.style)

        #: A really ugly way to add the target
        #: would be nice if we could just pass the block pointer here :)
        self.get_app().bridge.addTarget(
            self.widget,
            forControlEvents=UITextField.UIControlEventEditingChanged,
            andCallback=self.widget.getId(),
            usingMethod="onValueChanged",
            withValues=["text"]#,"selected"]
        )

        self.widget.onValueChanged.connect(self.on_value_changed)

    def on_value_changed(self, text):
        """ Update text field """
        d = self.declaration
        with self.widget.get_member('text').suppressed(self.widget):
            d.text = text

    # -------------------------------------------------------------------------
    # ProxyEditText API
    # -------------------------------------------------------------------------
    def set_selection(self, selection):
        pass

    def set_input_type(self, input_type):
        """ Set keyboard type """
        #: TODO...
        pass

    def set_style(self, style):
        self.widget.borderStyle = UITextField.STYLES[style]

    def set_placeholder(self, placeholder):
        self.widget.placeholder = placeholder