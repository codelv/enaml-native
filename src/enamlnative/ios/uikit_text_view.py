'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
'''

from atom.api import Typed, Tuple, observe, set_default
from enamlnative.widgets.text_view import ProxyTextView

from .bridge import ObjcMethod, ObjcProperty
from .uikit_view import NSObject, UIView, UiKitView

class UIFont(NSObject):
    __signature__ = set_default((dict(fontWithName="NSString",
                                      systemFontOfSize="NSInteger"), dict(size="NSInteger")))

class UILabel(UIView):
    """ From:
        https://developer.apple.com/documentation/uikit/uiview?language=objc
    """
    #: Properties
    text = ObjcProperty('NSString')
    textColor = ObjcProperty('UIColor')
    numberOfLines = ObjcProperty('NSInteger')
    textAlignment = ObjcProperty('NSTextAlignment')

    setFont = ObjcMethod('UIFont')


class UiKitTextView(UiKitView, ProxyTextView):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UILabel)

    #: Font to use
    font = Tuple()#Instance(UIFont)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        """
        self.widget = UILabel()

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        super(UiKitTextView, self).init_widget()

        d = self.declaration
        if d.text:
            self.set_text(d.text)
        if d.text_color:
            self.set_text_color(d.text_color)
        if d.font_family or d.text_size:
            self.refresh_font()
        if d.max_lines:
            self.set_max_lines(d.max_lines)

    # --------------------------------------------------------------------------
    # ProxyTextView API
    # --------------------------------------------------------------------------
    @observe('font')
    def update_font(self, change):
        self.widget.setFont(self.font)

    def refresh_font(self):
        d = self.declaration
        font_size = float(d.text_size or 17) # Default is 17
        if d.font_family:
            self.font = (d.font_family, font_size)#UIFont(fontWithName=d.font_family, size=font_size)
        else:
            self.font = (font_size,)#UIFont(systemFontOfSize=font_size)

    def set_text(self, text):
        self.widget.text = text

    def set_text_color(self, color):
        self.widget.textColor = color

    def set_text_size(self, size):
        self.update_font()

    def set_font_family(self, family):
        self.update_font()

    def set_max_lines(self, lines):
        self.widget.numberOfLines = lines