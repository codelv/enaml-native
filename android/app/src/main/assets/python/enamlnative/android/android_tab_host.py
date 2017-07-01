'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed, set_default

from enamlnative.widgets.tab_host import ProxyTabHost

from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .bridge import JavaMethod


class TabHost(FrameLayout):
    __javaclass__ = set_default('android.widget.TabHost')
    setCurrentTab = JavaMethod('int')

class AndroidTabHost(AndroidFrameLayout, ProxyTabHost):
    """ An Android implementation of an Enaml ProxyTabHost.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TabHost)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = TabHost(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidTabHost, self).init_widget()
        d = self.declaration
        self.set_current_tab(d.current_tab)

    # --------------------------------------------------------------------------
    # ProxyTabHost API
    # --------------------------------------------------------------------------
    def set_current_tab(self, index):
        self.widget.setCurrentTab(index)