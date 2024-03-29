"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Aug 22, 2017
"""
from atom.api import ForwardTyped, set_default
from enamlnative.widgets.activity_indicator import (
    ActivityIndicator,
    ProxyActivityIndicator,
)
from .android_progress_bar import AndroidProgressBar


class AndroidActivityIndicator(AndroidProgressBar, ProxyActivityIndicator):
    """An Android implementation of an Enaml ProxyActivityIndicator."""

    #: A reference to the declaration. Why does this need set explicitly here?
    declaration = ForwardTyped(lambda: ActivityIndicator)

    #: Set it to be an indeterminate progress bar
    indeterminate = set_default(True)  # type: ignore
