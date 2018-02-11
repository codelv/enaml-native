"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.button import (
    ProxyButton, ProxyImageButton, ProxyFloatingActionButton
)

from .bridge import JavaMethod

from .android_text_view import AndroidTextView, TextView
from .android_image_view import AndroidImageView, ImageView


class Button(TextView):
    __nativeclass__ = set_default('android.widget.Button')
    __signature__ = set_default(('android.content.Context',
                                 'android.util.AttributeSet', 'int'))
    STYLE_NORMAL = 0x01010048
    STYLE_FLAT = 0x0101032b
    STYLES = {
        '': STYLE_NORMAL,
        'borderless': STYLE_FLAT,
        'inset': 0x0101004a,
        'small': 0x01010049,
    }


class ImageButton(ImageView):
    __nativeclass__ = set_default('android.widget.ImageButton')


class FloatingActionButton(ImageButton):
    __nativeclass__ = set_default(
        'android.support.design.widget.FloatingActionButton')

    SIZE_NORMAL = 0
    SIZE_MINI = 1
    SIZE_AUTO = -1

    SIZES = {
        'normal': SIZE_NORMAL,
        'mini': SIZE_MINI,
        'auto': SIZE_AUTO
    }

    setSize = JavaMethod('int')
    setRippleColor = JavaMethod('android.graphics.Color')
    setCompatElevation = JavaMethod('float')
    show = JavaMethod()
    hide = JavaMethod()


class AndroidButton(AndroidTextView, ProxyButton):
    """ An Android implementation of an Enaml ProxyButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Button)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        d = self.declaration
        style = Button.STYLE_FLAT if d.flat else Button.STYLE_NORMAL
        self.widget = Button(self.get_context(), None, style)

    def init_widget(self):
        super(AndroidButton, self).init_widget()

        w = self.widget
        w.setOnClickListener(w.getId())
        w.onClick.connect(self.on_click)

    # -------------------------------------------------------------------------
    # ProxyButton API
    # -------------------------------------------------------------------------
    def set_flat(self, flat):
        pass


class AndroidImageButton(AndroidImageView, ProxyImageButton):
    """ An Android implementation of an Enaml ProxyImageButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ImageButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ImageButton(self.get_context())

    def init_widget(self):
        super(AndroidImageButton, self).init_widget()

        w = self.widget
        w.setOnClickListener(w.getId())
        w.onClick.connect(self.on_click)


class AndroidFloatingActionButton(AndroidImageButton,
                                  ProxyFloatingActionButton):
    """ An Android implementation of an Enaml ProxyImageButton.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(FloatingActionButton)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = FloatingActionButton(self.get_context())

    # -------------------------------------------------------------------------
    # ProxyFloatingActionButton API
    # -------------------------------------------------------------------------
    def set_size(self, size):
        self.widget.setSize(FloatingActionButton.SIZES[size])

    def set_elevation(self, elevation):
        self.widget.setCompatElevation(elevation)

    def set_ripple_color(self, color):
        self.widget.setRippleColor(color)

    def set_show(self, show):
        if show:
            self.widget.show()
        else:
            self.widget.hide()

