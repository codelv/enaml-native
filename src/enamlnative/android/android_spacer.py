"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 7, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.spacer import ProxySpacer

from .android_view import AndroidView, View


class Spacer(View):
    __nativeclass__ = set_default('android.widget.Space')


class AndroidSpacer(AndroidView, ProxySpacer):
    """ An Android implementation of an Enaml ProxySpacer.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Spacer)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = Spacer(self.get_context())



