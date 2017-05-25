#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Typed, ForwardTyped, Tuple, observe
)

from enaml.core.declarative import d_

from .text_view import TextView, ProxyTextView


class ProxyEditText(ProxyTextView):
    """ The abstract definition of a proxy EditText object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: EditText)

    def set_selection(self, selection):
        raise NotImplementedError


class EditText(TextView):
    """ A simple control for displaying read-only text.

    """

    #: Text selection
    selection = d_(Tuple(int))

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyEditText)

    @observe('selection')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(EditText, self)._update_proxy(change)
