'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.text_view import ProxyTextView

from .android_view import AndroidView, Color

Typeface = jnius.autoclass('android.graphics.Typeface')
TextView = jnius.autoclass('android.widget.TextView')

class TextWatcher(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/text/TextWatcher']

    def __init__(self, handler):
        self.__handler__ = handler
        super(TextWatcher, self).__init__()

    @jnius.java_method('(Landroid/text/Editable;)V')
    def afterTextChanged(self,e):
        self.__handler__.after_text_changed(e)

    @jnius.java_method('(Ljava/lang/CharSequence;III)V')
    def beforeTextChanged(self, s, start, before, count):
        self.__handler__.before_text_changed(s, start, before, count)

    @jnius.java_method('(Ljava/lang/CharSequence;III)V')
    def onTextChanged(self, s, start, before, count):
        self.__handler__.on_text_changed(s, start, before, count)


class AndroidTextView(AndroidView, ProxyTextView):
    """ An Android implementation of an Enaml ProxyTextView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TextView)

    #: A reference to the text changed listener
    watcher = Typed(TextWatcher)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = TextView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidTextView, self).init_widget()
        d = self.declaration
        self.set_text(d.text)

        if d.all_caps:
            self.set_all_caps(d.all_caps)
        if d.auto_link_mask:
            self.set_auto_link_mask(d.auto_link_mask)
        if d.font_family or d.font_style:
            self.update_font()
        if d.text_size:
            self.set_text_size(d.text_size)
        if d.text_color:
            self.set_text_color(d.text_color)
        if d.link_color:
            self.set_link_color(d.link_color)
        if d.highlight_color:
            self.set_highlight_color(d.highlight_color)
        if d.lines:
            self.set_lines(d.lines)
        if d.max_lines:
            self.set_max_lines(d.max_lines)

    # --------------------------------------------------------------------------
    # ProxyTextView API
    # --------------------------------------------------------------------------
    def set_all_caps(self, enabled):
        self.widget.setAllCaps(enabled)

    def set_auto_link_mask(self, mask):
        self.widget.setAutoLinkMask(mask)

    def set_font_family(self, family):
        self.update_font()

    def set_font_style(self, style):
        self.update_font()

    def update_font(self):
        d = self.declaration
        style = getattr(Typeface, d.font_style.upper() or 'NORMAL')
        tf = Typeface.create(d.font_family or None, style)
        self.widget.setTypeface(tf)

    def set_text(self, text):
        """ Set the text in the widget.

        """
        self.widget.setText(text, 0, len(text))

    def set_text_color(self, color):
        self.widget.setTextColor(Color.parseColor(color))

    def set_highlight_color(self, color):
        self.widget.setHighlightColor(Color.parseColor(color))

    def set_link_color(self, color):
        self.widget.setLinkTextColor(Color.parseColor(color))

    def set_text_size(self, size):
        self.widget.setTextSize(size)

    def set_lines(self, lines):
        self.widget.setLines(lines)

    def set_max_lines(self, lines):
        self.widget.setMaxLines(lines)


