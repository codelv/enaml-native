"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Jan 29, 2018
"""
from atom.api import ForwardTyped, Typed
from .dialog import Dialog, ProxyDialog


class ProxyBottomSheetDialog(ProxyDialog):
    """The abstract definition of a proxy dialog object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: BottomSheetDialog)


class BottomSheetDialog(Dialog):
    """A dialog that slides up from the bottom of the screen."""

    #: A reference to the proxy object.
    proxy = Typed(ProxyBottomSheetDialog)
