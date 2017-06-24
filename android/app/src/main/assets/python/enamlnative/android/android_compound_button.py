'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.compound_button import ProxyCompoundButton

from .android_button import AndroidButton, Button
from .bridge import JavaMethod, JavaCallback


class CompoundButton(Button):
    __javaclass__ = 'android.widget.CompoundButton'
    setChecked = JavaMethod('boolean')
    onCheckedChanged = JavaCallback('android.widget.CompoundButton','boolean')


class AndroidCompoundButton(AndroidButton, ProxyCompoundButton):
    """ An Android implementation of an Enaml ProxyCompoundButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(CompoundButton)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = CompoundButton(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidCompoundButton, self).init_widget()
        d = self.declaration
        self.set_checked(d.checked)
        self.widget.onCheckedChanged.connnect(self.on_checked)

    def on_checked(self, view, checked):
        d = self.declaration
        d.checked = checked

    #--------------------------------------------------------------------------
    # ProxyLabel API
    #--------------------------------------------------------------------------
    def set_checked(self, checked):
        self.widget.setChecked(checked)