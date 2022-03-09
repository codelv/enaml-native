"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on June 7, 2017

 
"""
from atom.api import Bool, ForwardTyped, Int, Typed
from enaml.core.declarative import d_, observe
from .progress_bar import ProgressBar, ProxyProgressBar


class ProxySeekBar(ProxyProgressBar):
    """The abstract definition of a proxy SeekBar object."""

    #: A reference to the SeekBar declaration.
    declaration = ForwardTyped(lambda: SeekBar)

    def set_key_progress_increment(self, value: int):
        raise NotImplementedError

    def set_split_track(self, split: bool):
        raise NotImplementedError


class SeekBar(ProgressBar):
    """A simple control for displaying read-only text."""

    #: Sets the amount of progress changed via the arrow keys.
    key_progress_increment = d_(Int())

    #: Specifies whether the track should be split by the thumb.
    split_track = d_(Bool())

    #: A reference to the SeekBar object.
    proxy = Typed(ProxySeekBar)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe("key_progress_increment", "split_track")
    def _update_proxy(self, change):

        super()._update_proxy(change)
