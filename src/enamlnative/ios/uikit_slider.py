"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 25, 2017

@author: jrm
"""

from atom.api import Typed, Bool
from enamlnative.widgets.seek_bar import ProxySeekBar

from .bridge import ObjcMethod, ObjcProperty, ObjcCallback
from .uikit_control import UIControl, UiKitControl


class UISlider(UIControl):
    """
    """
    #: Properties
    minimumValue = ObjcProperty('float')
    maximumValue = ObjcProperty('float')
    continuous = ObjcProperty('bool')
    value = ObjcProperty('float')
    onTintColor = ObjcProperty('UIColor')
    tintColor = ObjcProperty('UIColor')
    thumbTintColor = ObjcProperty('UIColor')
    onImage = ObjcProperty('UIImage')
    offImage = ObjcProperty('UIImage')

    #: Methods
    #: Works but then doesn't let you change it
    setValue = ObjcMethod('float', dict(animated='bool'))

    #: Callbacks
    onValueChanged = ObjcCallback('float')


class UiKitSlider(UiKitControl, ProxySeekBar):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UISlider)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        
        """
        self.widget = UISlider()

    def init_widget(self):
        """ Bind the on property to the checked state """
        super(UiKitSlider, self).init_widget()

        d = self.declaration
        if d.min:
            self.set_min(d.min)
        if d.max:
            self.set_max(d.max)
        if d.progress:
            self.set_progress(d.progress)

        #: A really ugly way to add the target
        #: would be nice if we could just pass the block pointer here :)
        self.get_app().bridge.addTarget(
            self.widget,
            forControlEvents=UISlider.UIControlEventValueChanged,
            andCallback=self.widget.getId(),
            usingMethod="onValueChanged",
            withValues=["value"]#,"selected"]
        )

        self.widget.onValueChanged.connect(self.on_checked_changed)

    def init_text(self):
        """ A slider has no text!"""
        pass

    def on_checked_changed(self, value):
        """ See https://stackoverflow.com/questions/19628310/ """
        #: Since iOS decides to call this like 100 times for each defer it
        d = self.declaration
        with self.widget.setValue.suppressed():
            d.progress = int(value)

    # -------------------------------------------------------------------------
    # ProxySlider API
    # -------------------------------------------------------------------------
    def set_progress(self, progress):
        self.widget.setValue(float(progress), animated=True)

    def set_secondary_progress(self, progress):
        raise NotImplementedError

    def set_max(self, value):
        self.widget.maximumValue = float(value)

    def set_min(self, value):
        self.widget.minimumValue = float(value)

    def set_key_progress_increment(self, value):
        raise NotImplementedError

    def set_split_track(self, split):
        raise NotImplementedError