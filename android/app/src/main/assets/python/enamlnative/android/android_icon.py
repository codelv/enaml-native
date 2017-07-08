'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed, set_default

from enamlnative.widgets.icon import ProxyIcon

from .android_text_view import AndroidTextView, TextView


class Icon(TextView):
    __javaclass__ = set_default('com.joanzapata.iconify.widget.IconTextView')


class AndroidIcon(AndroidTextView, ProxyIcon):
    """ An Android implementation of an Enaml ProxyIcon.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Icon)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = Icon(self.get_context())
