"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.
"""
from atom.api import ForwardTyped, Typed
from .view_animator import ProxyViewAnimator, ViewAnimator


class ProxyViewSwitcher(ProxyViewAnimator):
    """The abstract definition of a proxy ViewSwitcher object."""

    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: ViewSwitcher)


class ViewSwitcher(ViewAnimator):
    """A simple control for a ViewSwitcher."""

    #: A reference to the ProxyViewSwitcher object.
    proxy = Typed(ProxyViewSwitcher)
