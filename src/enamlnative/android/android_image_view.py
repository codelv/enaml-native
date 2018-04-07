"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 6, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.image_view import ProxyImageView

from .android_view import AndroidView, View
from .bridge import (
    JavaBridgeObject, JavaMethod, JavaCallback, JavaStaticMethod
)


class ImageView(View):
    __nativeclass__ = set_default('android.widget.ImageView')
    setImageAlpha = JavaMethod('int')
    setColorFilter = JavaMethod('int')
    setCropToPadding = JavaMethod('boolean')
    setImageBitmap = JavaMethod('android.graphics.Bitmap')
    setImageIcon = JavaMethod('android.graphics.drawable.Icon')
    setImageLevel = JavaMethod('int')
    seImageMatrix = JavaMethod('android.graphics.Matrix')
    setImageResource = JavaMethod('android.R')
    setImageDrawable = JavaMethod('android.graphics.drawable.Drawable')
    setImageURI = JavaMethod('android.net.Uri')
    setMaxHeight = JavaMethod('int')
    setMaxWidth = JavaMethod('int')
    setScaleType = JavaMethod('android.view.ImageView.ScaleType')


class Drawable(JavaBridgeObject):
    __nativeclass__ = set_default('android.graphics.drawable.Drawable')
    onDrawableLoaded = JavaCallback('android.graphics.drawable.Drawable')


class Bitmap(JavaBridgeObject):
    __nativeclass__ = set_default('android.graphics.Bitmap')


class Icon(JavaBridgeObject):
    __nativeclass__ = set_default('android.graphics.drawable.Icon')
    createWithFilePath = JavaMethod('java.lang.String',
                                    returns='android.graphics.drawable.Icon')
    createWithContentUri = JavaMethod('java.lang.String',
                                      returns='android.graphics.drawable.Icon')


class Glide(JavaBridgeObject):
    __nativeclass__ = set_default('com.bumptech.glide.Glide')

    with_ = JavaStaticMethod('android.view.View',
                             returns='com.bumptech.glide.RequestManager')
    with__ = JavaStaticMethod('android.content.Context',
                              returns='com.bumptech.glide.RequestManager')


class RequestManager(JavaBridgeObject):
    __nativeclass__ = set_default('com.bumptech.glide.RequestManager')
    load = JavaMethod('java.lang.String',
                      returns='com.bumptech.glide.RequestBuilder')


class RequestBuilder(JavaBridgeObject):
    __nativeclass__ = set_default('com.bumptech.glide.RequestBuilder')
    asBitmap = JavaMethod(returns='android.graphics.Bitmap')
    into = JavaMethod('android.widget.ImageView')


class AndroidImageView(AndroidView, ProxyImageView):
    """ An Android implementation of an Enaml ProxyImageView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ImageView)

    #: A Glide request manager for loading images from urls or files
    manager = Typed(RequestManager)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ImageView(self.get_context())

    # -------------------------------------------------------------------------
    # OnDrawableLoaded API
    # -------------------------------------------------------------------------
    def on_drawable_loaded(self, d):
        self.widget.setImageDrawable(d)

    # -------------------------------------------------------------------------
    # ProxyImageView API
    # -------------------------------------------------------------------------
    def _default_manager(self):
        return RequestManager(__id__=Glide.with_(self.widget))

    def set_src(self, src):
        if src.startswith("@"):
            self.widget.setImageResource(src)
        elif src.startswith("{"):
            from .android_iconify import IconDrawable
            self.widget.setImageDrawable(
                IconDrawable(self.get_context(), src[1:-1]))
        else:
            RequestBuilder(__id__=self.manager.load(src)).into(self.widget)

    def set_max_height(self, height):
        self.widget.setMaxHeight(height)

    def set_max_width(self, width):
        self.widget.setMaxWidth(width)
