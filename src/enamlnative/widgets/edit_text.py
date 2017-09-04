'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Tuple, Unicode, observe, set_default
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

    def set_placeholder(self, placeholder):
        raise NotImplementedError


class EditText(TextView):
    """ A simple control for displaying read-only text.

    """

    #: Text selection
    selection = d_(Tuple(int))

    #: Make editable by default
    input_type = set_default('text')

    #: Placeholder text
    placeholder = d_(Unicode())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyEditText)

    @observe('selection', 'placeholder')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(EditText, self)._update_proxy(change)
