#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Typed, ForwardTyped, Bool, observe
)

from enaml.core.declarative import d_

from .compound_button import CompoundButton, ProxyCompoundButton


class ProxyCheckBox(ProxyCompoundButton):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: CheckBox)


class CheckBox(CompoundButton):
    """ A simple control for displaying read-only text.

    """

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyCheckBox)


