"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, List, Int, observe, set_default
)

from enaml.core.declarative import d_

from .edit_text import EditText, ProxyEditText


class ProxyAutoCompleteTextView(ProxyEditText):
    """ The abstract definition of a proxy AutoCompleteTextView object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: AutoCompleteTextView)

    def set_choices(self, choices):
        raise NotImplementedError

    def set_drop_down_height(self, height):
        raise NotImplementedError

    def set_drop_down_width(self, width):
        raise NotImplementedError

    def set_list_selection(self, index):
        raise NotImplementedError

    def set_threshold(self, threshold):
        raise NotImplementedError


class AutoCompleteTextView(EditText):
    """ A simple control for displaying read-only text.

    """

    #: Auto complete choices
    choices = d_(List())

    #: Sets the current height for the auto-complete drop down list.
    drop_down_height = d_(Int())

    #: Sets the current width for the auto-complete drop down list.
    drop_down_width = d_(Int())

    #: Selected item within the list
    list_selection = d_(Int())

    #: Specifies the minimum number of characters the user has to type
    #: in the edit box before the drop down list is shown.
    threshold = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyAutoCompleteTextView)

    @observe('choices', 'drop_down_height', 'drop_down_width'
             'list_selection', 'threshold',)
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(AutoCompleteTextView, self)._update_proxy(change)
