'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.view_group import ProxyViewGroup

from .android_view import AndroidView, LayoutParams

Gravity = jnius.autoclass('android.view.Gravity')
ViewGroup = jnius.autoclass('android.view.ViewGroup')


class AndroidViewGroup(AndroidView, ProxyViewGroup):
    """ An Android implementation of an Enaml ProxyViewGroup.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ViewGroup)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = ViewGroup(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidViewGroup, self).init_widget()
        d = self.declaration
        if d.layout_width or d.layout_height or d.layout_gravity:
            self.update_layout_params()

    #--------------------------------------------------------------------------
    # ProxyViewGroup API
    #--------------------------------------------------------------------------
    def set_layout_width(self, width):
        self.update_layout_params()

    def set_layout_height(self, height):
        self.update_layout_params()

    def set_layout_gravity(self, gravity):
        return
        # params = self.get_layout_params()
        # params.gravity = getattr(Gravity,d.layout_gravity.upper())
        # self.update_layout_params()

    def update_layout_params(self):
        params = self.get_layout_params()
        # d = self.declaration
        # if d.layout_width:
        #     layout_width = getattr(LayoutParams,d.layout_width.upper())\
        #         if hasattr(LayoutParams,d.layout_width.upper()) else int(d.layout_width)
        # else:
        #     layout_width = LayoutParams.MATCH_PARENT
        # if d.layout_height:
        #     layout_height = getattr(LayoutParams,d.layout_height.upper())\
        #         if hasattr(LayoutParams,d.layout_height.upper()) else int(d.layout_height)
        # else:
        #     layout_height = LayoutParams.MATCH_PARENT
        #
        # #: Clone existing
        # params = self.layout_params(params)
        # self.widget.setLayoutParams(params)
