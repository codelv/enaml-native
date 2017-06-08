'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 7, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.switch import ProxySwitch

from .android_compound_button import AndroidCompoundButton

Switch = jnius.autoclass('android.widget.Switch')


class AndroidSwitch(AndroidCompoundButton, ProxySwitch):
    """ An Android implementation of an Enaml ProxySwitch.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Switch)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying Android widget.

        """
        self.widget = Switch(self.get_context())