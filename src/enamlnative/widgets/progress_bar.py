"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 26, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Int, observe
)

from enaml.core.declarative import d_

from .view import View, ProxyView


class ProxyProgressBar(ProxyView):
    """ The abstract definition of a proxy ProgressBar object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ProgressBar)

    def set_progress(self, progress):
        raise NotImplementedError

    #def set_indeterminate(self, indeterminate):
    #    raise NotImplementedError

    def set_secondary_progress(self, progress):
        raise NotImplementedError

    def set_max(self, value):
        raise NotImplementedError

    def set_min(self, value):
        raise NotImplementedError


class ProgressBar(View):
    """ A simple control for displaying a ProgressBar.

    """
    #: Sets the current progress to the specified value.
    progress = d_(Int())

    #: Sets the current progress to the specified value.
    secondary_progress = d_(Int())

    #: Change the indeterminate mode for this progress bar.
    #: In indeterminate mode, the progress is ignored and the progress
    #: bar shows an infinite animation instead.

    #: Set the upper range of the progress bar max.
    max = d_(Int())

    #: Set the lower range of the progress bar
    min = d_(Int())

    #: A reference to the ProxyProgressBar object.
    proxy = Typed(ProxyProgressBar)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe('progress', 'secondary_progress', 'max', 'min')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(ProgressBar, self)._update_proxy(change)
