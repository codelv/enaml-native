#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import (
    Typed, ForwardTyped, Event
)

from enaml.core.declarative import d_

from .linear_layout import LinearLayout, ProxyLinearLayout

class ProxyRadioGroup(ProxyLinearLayout):
    """ The abstract definition of a proxy Label object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: RadioGroup)


class RadioGroup(LinearLayout):
    """ A simple control for displaying read-only text.

    """

    #: Clear all checked
    clear = d_(Event(), writable=False)

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyRadioGroup)


