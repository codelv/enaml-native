'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 25, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.tab_widget import ProxyTabWidget

from .android_linear_layout import AndroidLinearLayout

TabWidget = jnius.autoclass('android.widget.TabWidget')

class AndroidTabWidget(AndroidLinearLayout, ProxyTabWidget):
    """ An Android implementation of an Enaml ProxyFrameLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TabWidget)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = TabWidget(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidTabWidget, self).init_widget()
        d = self.declaration
        self.set_current_tab(d.current_tab)
        self.set_enabled(d.enabled)
        self.set_strip_enabled(d.strip_enabled)


    #--------------------------------------------------------------------------
    # ProxyTabWidget API
    #--------------------------------------------------------------------------
    def set_strip_enabled(self, enabled):
        self.widget.setStripEnabled(enabled)

    def set_current_tab(self, index):
        self.widget.setCurrentTab(index)

    def set_enabled(self, enabled):
        self.widget.setEnabled(enabled)
