"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 25, 2017

@author: jrm
"""

from atom.api import Typed, Bool
from enamlnative.widgets.switch import ProxySwitch

from .bridge import ObjcMethod, ObjcProperty, ObjcCallback
from .uikit_control import UIControl, UiKitControl


class UISwitch(UIControl):
    """
    """
    #: Properties
    on = ObjcProperty('bool')
    onTintColor = ObjcProperty('UIColor')
    tintColor = ObjcProperty('UIColor')
    thumbTintColor = ObjcProperty('UIColor')
    onImage = ObjcProperty('UIImage')
    offImage = ObjcProperty('UIImage')

    #: Methods
    #: Works but then doesn't let you change it
    setOn = ObjcMethod('bool', dict(animated='bool'))

    #: Callbacks
    onValueChanged = ObjcCallback('bool')


class UiKitSwitch(UiKitControl, ProxySwitch):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UISwitch)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        """
        self.widget = UISwitch()

    def init_widget(self):
        """ Bind the on property to the checked state """
        super(UiKitSwitch, self).init_widget()

        d = self.declaration
        if d.checked:
            self.set_checked(d.checked)

        #: Watch the on property for change
        #: So apparently UISwitch is not KVO compliant...
        # self.widget.addObserver(
        #     self.get_app().view_controller,
        #     forKeyPath="on",
        #     options=UISwitch.NSKeyValueObservingOptionNew|UISwitch.NSKeyValueObservingOptionOld,
        #     context=self.widget
        #)

        #: A really ugly way to add the target
        #: would be nice if we could just pass the block pointer here :)
        self.get_app().bridge.addTarget(
            self.widget,
            forControlEvents=UISwitch.UIControlEventValueChanged,
            andCallback=self.widget.getId(),
            usingMethod="onValueChanged",
            withValues=["on"]#,"selected"]
        )

        self.widget.onValueChanged.connect(self.on_checked_changed)

    def on_checked_changed(self, on):
        """ See https://stackoverflow.com/questions/19628310/ """
        #: Since iOS decides to call this like 100 times for each defer it
        d = self.declaration
        with self.widget.setOn.suppressed():
            d.checked = on

    # -------------------------------------------------------------------------
    # ProxySwitch API
    # -------------------------------------------------------------------------
    def set_checked(self, checked):
        self.widget.setOn(checked, animated=True)

    def set_show_text(self, show):
        pass  #: Has no text

    def set_split_track(self, split):
        pass

    def set_text_off(self, text):
        pass

    def set_text_on(self, text):
        pass