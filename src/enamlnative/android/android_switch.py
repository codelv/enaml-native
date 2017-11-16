"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 7, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.switch import ProxySwitch

from .android_compound_button import AndroidCompoundButton, CompoundButton
from .bridge import JavaMethod


class Switch(CompoundButton):
    __nativeclass__ = set_default('android.widget.Switch')
    setShowText = JavaMethod('boolean')
    setSplitTrack = JavaMethod('boolean')
    setTextOff = JavaMethod('java.lang.CharSequence')
    setTextOn = JavaMethod('java.lang.CharSequence')


class AndroidSwitch(AndroidCompoundButton, ProxySwitch):
    """ An Android implementation of an Enaml ProxySwitch.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Switch)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = Switch(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidSwitch, self).init_widget()
        d = self.declaration
        self.set_show_text(d.show_text)
        if d.split_track:
            self.set_split_track(d.split_track)
        if d.text_off:
            self.set_text_off(d.text_off)
        if d.text_on:
            self.set_text_on(d.text_on)

    # -------------------------------------------------------------------------
    # ProxySwitch API
    # -------------------------------------------------------------------------
    def set_show_text(self, show):
        api = self.get_context().api_level
        if api >= 21:
            self.widget.setShowText(show)

    def set_split_track(self, split):
        self.widget.setSplitTrack(split)

    def set_text_off(self, text):
        self.widget.setTextOff(text)

    def set_text_on(self, text):
        self.widget.setTextOn(text)
