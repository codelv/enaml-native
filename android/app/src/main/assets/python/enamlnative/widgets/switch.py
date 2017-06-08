'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on June 7, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Bool, observe
)

from enaml.core.declarative import d_

from .compound_button import CompoundButton, ProxyCompoundButton


class ProxySwitch(ProxyCompoundButton):
    """ The abstract definition of a proxy Switch object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Switch)


class Switch(CompoundButton):
    """ A simple control for displaying a Switch.

    """

    #: A reference to the ProxySwitch object.
    proxy = Typed(ProxySwitch)


