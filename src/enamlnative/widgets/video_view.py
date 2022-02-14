"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Bool, Enum, Event, ForwardTyped, Str, Typed, observe
from enaml.core.declarative import d_
from .surface_view import ProxySurfaceView, SurfaceView


class ProxyVideoView(ProxySurfaceView):
    """The abstract definition of a proxy video view object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: VideoView)

    def seek_to(self, t):
        raise NotImplementedError

    def set_control(self, control):
        raise NotImplementedError


class VideoView(SurfaceView):
    """VideoView displays a video file"""

    #: Source of the video file or URI
    src = d_(Str())

    #: Player actions
    control = d_(Enum("play", "stop", "pause"))

    #: State
    state = d_(
        Enum("idle", "stopped", "paused", "loading", "complete", "playing", "error"),
        writable=False,
    )

    #: Error event
    error = d_(Event(dict), writable=False)

    #: Info event, such as buffering
    info = d_(Event(dict), writable=False)

    #: A reference to the ProxyViewGroup object.
    proxy = Typed(ProxyVideoView)

    @observe("src", "src", "control")
    def _update_proxy(self, change):
        super()._update_proxy(change)

    def seek_to(self, ms):
        """Seek to the given time."""
        self.proxy.seek_to(ms)
