"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped
)

from .compound_button import CompoundButton, ProxyCompoundButton


class ProxyRadioButton(ProxyCompoundButton):
    """ The abstract definition of a proxy RadioButton object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: RadioButton)


class RadioButton(CompoundButton):
    """ A simple control for displaying a RadioButton.

    """

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyRadioButton)


