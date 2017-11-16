"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""

from atom.api import Typed, set_default
from enamlnative.widgets.text_view import ProxyTextView

from .bridge import ObjcMethod, ObjcProperty
from .uikit_view import NSObject, UIView, UiKitView

class UIFont(NSObject):
    __signature__ = set_default((dict(fontWithName="NSString",
                                      systemFontOfSize="NSInteger"),
                                 dict(size="NSInteger")))


class UITextView(UIView):
    """ Common text items """
    #: Properties
    text = ObjcProperty('NSString')
    textColor = ObjcProperty('UIColor')
    textAlignment = ObjcProperty('enum')# NSTextAlignment
    setFont = ObjcMethod('UIFont')

    NSTextAlignmentLeft = 0
    NSTextAlignmentCenter = 1
    NSTextAlignmentRight = 2
    NSTextAlignmentJustified = 3
    NSTextAlignmentNatural = 4

    TEXT_ALIGNMENT = {
        '': NSTextAlignmentNatural,
        'left': NSTextAlignmentLeft,
        'right': NSTextAlignmentRight,
        'center': NSTextAlignmentCenter,
        'justified': NSTextAlignmentJustified,
        'natural': NSTextAlignmentNatural,
    }


class UILabel(UITextView):
    numberOfLines = ObjcProperty('NSInteger')


class UiKitTextView(UiKitView, ProxyTextView):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UILabel)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.
        """
        self.widget = UILabel()

    def init_widget(self):
        """ Init the text view fields """
        super(UiKitTextView, self).init_widget()
        self.init_text()

    def init_text(self):
        """ Init text properties for this widget """
        d = self.declaration
        if d.text:
            self.set_text(d.text)
        if d.text_color:
            self.set_text_color(d.text_color)
        if d.text_alignment:
            self.set_text_alignment(d.text_alignment)
        if d.font_family or d.text_size:
            self.refresh_font()
        if hasattr(d, 'max_lines') and d.max_lines:
            self.set_max_lines(d.max_lines)

    # -------------------------------------------------------------------------
    # ProxyTextView API
    # -------------------------------------------------------------------------
    def refresh_font(self):
        d = self.declaration
        font_size = float(d.text_size or 17)  # Default is 17
        if d.font_family:
            self.widget.setFont((d.font_family, font_size))
            #UIFont(fontWithName=d.font_family, size=font_size)
        else:
            self.widget.setFont((font_size,))
            #UIFont(systemFontOfSize=font_size)

    def set_text(self, text):
        self.widget.text = text

    def set_text_color(self, color):
        self.widget.textColor = color

    def set_text_alignment(self, alignment):
        self.widget.textAlignment = UITextView.TEXT_ALIGNMENT[alignment]

    def set_text_size(self, size):
        self.refresh_font()

    def set_font_family(self, family):
        self.refresh_font()

    def set_max_lines(self, lines):
        self.widget.numberOfLines = lines