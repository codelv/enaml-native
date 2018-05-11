"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 9, 2018

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.video_view import ProxyVideoView

from .android_surface_view import AndroidSurfaceView, SurfaceView
from .android_utils import Uri
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class MediaPlayer(JavaBridgeObject):
    __nativeclass__ = set_default('android.media.MediaPlayer')
    onCompletion = JavaCallback('android.media.MediaPlayer')
    onError = JavaCallback('android.media.MediaPlayer', 'int', 'int',
                           returns='boolean')
    onInfo = JavaCallback('android.media.MediaPlayer', 'int', 'int',
                          returns='boolean')
    onPrepared = JavaCallback('android.media.MediaPlayer')

    MEDIA_ERROR_UNKNOWN = 1
    MEDIA_ERROR_SERVER_DIED = 100
    MEDIA_ERROR_NOT_VALID_FOR_PROGRESSIVE_PLAYBACK = 200
    MEDIA_ERROR_TIMED_OUT = -110
    MEDIA_ERROR_IO = -1004
    MEDIA_ERROR_UNSUPPORTED = -1010
    MEDIA_ERROR_MALFORMED = -1007

    ERROR = {
        MEDIA_ERROR_UNKNOWN: 'unknown',
        MEDIA_ERROR_SERVER_DIED: 'server died',
        MEDIA_ERROR_NOT_VALID_FOR_PROGRESSIVE_PLAYBACK: 'not valid for '
                                                        'progressive playback',
        MEDIA_ERROR_TIMED_OUT: 'timed out',
        MEDIA_ERROR_IO: 'connection error',
        MEDIA_ERROR_UNSUPPORTED: 'unsupported',
        MEDIA_ERROR_MALFORMED: 'malformed'
    }

    MEDIA_INFO_UNKNOWN = 1
    MEDIA_INFO_STARTED_AS_NEXT = 2
    MEDIA_INFO_VIDEO_RENDERING_START = 3
    MEDIA_INFO_VIDEO_TRACK_LAGGING = 700
    MEDIA_INFO_BUFFERING_START = 701
    MEDIA_INFO_BUFFERING_END = 702
    MEDIA_INFO_BAD_INTERLEAVING = 800
    MEDIA_INFO_NOT_SEEKABLE = 801
    MEDIA_INFO_METADATA_UPDATE = 802
    MEDIA_INFO_AUDIO_NOT_PLAYING = 804
    MEDIA_INFO_VIDEO_NOT_PLAYING = 805
    MEDIA_INFO_UNSUPPORTED_SUBTITLE = 901
    MEDIA_INFO_SUBTITLE_TIMED_OUT = 902

    INFO = {
        MEDIA_INFO_UNKNOWN: 'unknown',
        MEDIA_INFO_STARTED_AS_NEXT: 'started as next',
        MEDIA_INFO_VIDEO_RENDERING_START: 'video rendering start',
        MEDIA_INFO_VIDEO_TRACK_LAGGING: 'video track lagging',
        MEDIA_INFO_BUFFERING_START: 'buffering start',
        MEDIA_INFO_BUFFERING_END: 'buffering end',
        MEDIA_INFO_BAD_INTERLEAVING: 'bad interleaving',
        MEDIA_INFO_NOT_SEEKABLE: 'not seekable',
        MEDIA_INFO_METADATA_UPDATE: 'metadata update',
        MEDIA_INFO_AUDIO_NOT_PLAYING: 'audio not playing',
        MEDIA_INFO_VIDEO_NOT_PLAYING: 'video not playing',
        MEDIA_INFO_UNSUPPORTED_SUBTITLE: 'unsupported subtitle',
        MEDIA_INFO_SUBTITLE_TIMED_OUT: 'subtitle timed out'
    }


class VideoView(SurfaceView):
    __nativeclass__ = set_default('android.widget.VideoView')
    setVideoPath = JavaMethod('java.lang.String')
    setVideoURI = JavaMethod('android.net.Uri')
    start = JavaMethod()
    pause = JavaMethod()
    resume = JavaMethod()
    suspend = JavaMethod()
    stopPlayback = JavaMethod()
    seekTo = JavaMethod('int')
    setOnCompletionListener = JavaMethod(
        'android.media.MediaPlayer$OnCompletionListener')
    setOnErrorListener = JavaMethod(
        'android.media.MediaPlayer$OnErrorListener')
    setOnInfoListener = JavaMethod(
        'android.media.MediaPlayer$OnInfoListener')
    setOnPreparedListener = JavaMethod(
        'android.media.MediaPlayer$OnPreparedListener')


class AndroidVideoView(AndroidSurfaceView, ProxyVideoView):
    """ An Android implementation of an Enaml ProxySurfaceView

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(VideoView)

    #: The media player
    player = Typed(MediaPlayer)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        self.widget = VideoView(self.get_context())
    
    def init_widget(self):
        super(AndroidVideoView, self).init_widget()
        
        # Setup listeners
        w = self.widget
        player = self.player = MediaPlayer()
        id = player.getId()
        player.onCompletion.connect(self.on_complete)
        player.onError.connect(self.on_error)
        player.onPrepared.connect(self.on_prepared)
        player.onInfo.connect(self.on_info)

        w.setOnCompletionListener(id)
        w.setOnErrorListener(id)
        w.setOnPreparedListener(id)
        w.setOnInfoListener(id)
        
    def init_layout(self):
        super(AndroidVideoView, self).init_layout()
        d = self.declaration
        if d.state == 'play':
            self.set_state(d.state)
            
    # -------------------------------------------------------------------------
    # Listeners API
    # -------------------------------------------------------------------------
    def on_complete(self, player):
        d = self.declaration
        d.state = 'complete'
        
    def on_error(self, player, what, extra):
        d = self.declaration
        try:
            d.state = 'error'
            msg = MediaPlayer.ERROR.get(what, MediaPlayer.MEDIA_ERROR_UNKNOWN)
            d.error({'type': what, 'extra': extra, 'message': msg})
        finally:
            return True
        
    def on_prepared(self, player):
        d = self.declaration
        if d.control == 'play':
            d.state = 'playing'
    
    def on_info(self, player, what, extra):
        d = self.declaration
        try:
            msg = MediaPlayer.INFO.get(what, MediaPlayer.MEDIA_INFO_UNKNOWN)
            if extra:
                error = MediaPlayer.ERROR.get(extra)
                if error:
                    msg += " {}".format(error)
            d.info({'type': what, 'extra': extra,
                    'message': msg})
        finally:
            return True
    
    # -------------------------------------------------------------------------
    # ProxyVideoView API
    # -------------------------------------------------------------------------
    def set_src(self, src):
        self.widget.setVideoURI(Uri.parse(src))
        d = self.declaration
        d.state = 'loading'
        
    def set_control(self, control):
        d = self.declaration
        if control == 'play':
            self.widget.start()
            # d.state = 'loading'
        elif control == 'stop':
            self.widget.stopPlayback()
            d.state = 'stopped'
        elif control == 'pause':
            self.widget.pause()
            d.state = 'paused'
        
    def seek_to(self, pos):
        self.widget.seekTo(pos)
