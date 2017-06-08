'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 26, 2017

@author: jrm
'''
import jnius
from atom.api import Typed
from enamlnative.widgets.progress_bar import ProxyProgressBar

from .android_view import AndroidView, View

ProgressBar = jnius.autoclass('android.widget.ProgressBar')


class AndroidProgressBar(AndroidView, ProxyProgressBar):
    """ An Android implementation of an Enaml ProxyProgressBar.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ProgressBar)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = ProgressBar(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidProgressBar, self).init_widget()
        d = self.declaration
        self.set_progress(d.progress)
        self.set_indeterminate(d.indeterminate)
        if d.secondary_progress:
            self.set_secondary_progress(d.secondary_progress)
        if d.max:
            self.set_max(d.max)

    # --------------------------------------------------------------------------
    # ProxyProgressBar API
    # --------------------------------------------------------------------------
    def set_progress(self, progress):
        d = self.declaration
        self.widget.setProgress(progress,d.animated)

    def set_animated(self, animated):
        pass

    def set_indeterminate(self, indeterminate):
        self.widget.setIndeterminate(indeterminate)

    def set_secondary_progress(self, progress):
        self.widget.setSecondaryProgress(progress)

    def set_max(self, max):
        self.widget.setMax(max)