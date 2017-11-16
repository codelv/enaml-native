"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 6, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.image_view import ProxyImageView

from .android_view import AndroidView, View
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


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
    setImageUri = JavaMethod('android.net.Uri')
    setMaxHeight = JavaMethod('int')
    setMaxWidth = JavaMethod('int')
    setScaleType = JavaMethod('android.view.ImageView.ScaleType')


class Drawable(JavaBridgeObject):
    __nativeclass__ = set_default('android.graphics.drawable.Drawable')
    onDrawableLoaded = JavaCallback('android.graphics.drawable.Drawable')


class Icon(JavaBridgeObject):
    __nativeclass__ = set_default('android.graphics.drawable.Icon')
    createWithFilePath = JavaMethod('java.lang.String',
                                    returns='android.graphics.drawable.Icon')
    createWithContentUri = JavaMethod('java.lang.String',
                                      returns='android.graphics.drawable.Icon')


class AndroidImageView(AndroidView, ProxyImageView):
    """ An Android implementation of an Enaml ProxyImageView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ImageView)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ImageView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidImageView, self).init_widget()
        d = self.declaration
        if d.alpha:
            self.set_alpha(d.alpha)
        if d.max_height:
            self.set_max_height(d.max_height)
        if d.max_width:
            self.set_max_width(d.max_width)
        self.set_src(d.src)

    # -------------------------------------------------------------------------
    # OnDrawableLoaded API
    # -------------------------------------------------------------------------
    def on_drawable_loaded(self, d):
        self.widget.setImageDrawable(d)

    # -------------------------------------------------------------------------
    # ProxyImageView API
    # -------------------------------------------------------------------------
    def set_src(self, src):
        if src.startswith("@"):
            self.widget.setImageResource(src)
        else:
            self.widget.setImageUri(src)

    def set_max_height(self, height):
        self.widget.setMaxHeight(height)

    def set_max_width(self, width):
        self.widget.setMaxWidth(width)
