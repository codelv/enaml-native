"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, set_default

from enamlnative.widgets.text_view import ProxyTextView

from .android_view import AndroidView, View
from .bridge import JavaMethod, JavaCallback


class Gravity:
    # Push object to the bottom of its container, not changing its size.
    bottom = 50

    # Place the object in the center of its container in both the
    # vertical and horizontal axis, not changing its size.
    center = 11

    # Place object in the horizontal center of its container,
    # not changing its size.
    center_horizontal = 1

    # Place object in the vertical center of its container,
    # not changing its size.
    center_vertical = 10

    # Additional option that can be set to have the left and/or right edges
    # of the child clipped to its container's bounds. The clip will be based
    # on the horizontal gravity: a left gravity will clip the right edge,
    # a right gravity will clip the left edge, and neither will clip
    # both edges.
    clip_horizontal = 8

    # Additional option that can be set to have the top and/or bottom edges
    # of the child clipped to its container's bounds. The clip will be based
    # on the vertical gravity: a top gravity will clip the bottom edge, a
    # bottom gravity will clip the top edge, and neither will clip both edges.
    clip_vertical = 80

    # Push object to the end of its container, not changing its size.
    end = 800005

    # Grow the horizontal and vertical size of the object
    # if needed so it completely fills its container.
    fill = 77

    # Grow the horizontal size of the object if needed so it completely
    # fills its container.
    fill_horizontal = 7

    # Grow the vertical size of the object if needed so it completely
    # fills its container.
    fill_vertical = 70

    # Push object to the left of its container, not changing its size.
    left = 3
    right = 5

    # Push object to the right of its container, not changing its size.
    start = 800003

    # Push object to the beginning of its container, not changing its size.
    top = 30

    @staticmethod
    def parse(gravity):
        g = 0
        for key in gravity.split("|"):
            g |= getattr(Gravity, key)
        return g


class TextView(View):
    __nativeclass__ = set_default('android.widget.TextView')
    setAllCaps = JavaMethod('boolean')
    setAutoLinkMask = JavaMethod('int')
    setText = JavaMethod('java.lang.CharSequence')
    setTextKeepState = JavaMethod('java.lang.CharSequence')
    setTextColor = JavaMethod('android.graphics.Color')
    setTextIsSelectable = JavaMethod('boolean')
    setHighlightColor = JavaMethod('android.graphics.Color')
    setLinkTextColor = JavaMethod('android.graphics.Color')
    setGravity = JavaMethod('int')
    setTextSize = JavaMethod('float')
    setTypeface = JavaMethod('android.graphics.Typeface', 'int')
    setLines = JavaMethod('int')
    setLineSpacing = JavaMethod('float', 'float')
    setLetterSpacing = JavaMethod('float')
    setMaxLines = JavaMethod('int')
    setOnEditorActionListener = JavaMethod(
        'android.widget.TextView$OnEditorActionListener')
    setInputType = JavaMethod('int')
    addTextChangedListener = JavaMethod('android.text.TextWatcher')
    removeTextChangedListener = JavaMethod('android.text.TextWatcher')

    #: TextWatcher API
    afterTextChanged = JavaCallback('android.text.Editable')
    beforeTextChanged = JavaCallback('java.lang.CharSequence', 'int', 'int',
                                     'int')
    onTextChanged = JavaCallback('java.lang.CharSequence', 'int', 'int', 'int')

    #: EditorAction API
    onEditorAction = JavaCallback('android.view.TextView', 'int',
                                  'android.view.KeyEvent', returns='boolean')

    FONT_STYLES = {
        'bold': 1,
        'bold_italic': 3,
        'normal': 0,
        'italic': 2
    }

    INPUT_TYPES = {
        '': 0,
        'date': 0x14,
        'datetime': 0x4,
        'number': 0x2,
        'number_decimal': 0x2002,
        'number_password': 0x12,
        'number_signed': 0x1002,
        'phone': 0x3,
        'text': 0x1,
        'text_auto_complete': 0x10001,
        'text_auto_correct': 0x8001,
        'text_cap_characters': 0x1001,
        'text_cap_sentences': 0x4001,
        'text_cap_words': 0x2001,
        'text_email_address': 0x21,
        'text_email_subject': 0x31,
        'text_filter': 0xb1,
        'text_ime_multi_line': 0x40001,
        'text_long_message': 0x51,
        'text_multi_line': 0x20001,
        'text_no_suggestions': 0x80001,
        'text_password': 0x81,
        'text_person_name': 0x61,
        'text_phonetic': 0xc1,
        'text_postal_address': 0x71,
        'text_short_message': 0x41,
        'text_uri': 0x11,
        'text_visible_password': 0x91,
        'text_web_edit_text': 0xa1,
        'text_web_email_address': 0xd1,
        'text_web_password': 0xe1,
        'time': 24,
    }

    TEXT_ALIGNMENT_INHERIT = 0
    TEXT_ALIGNMENT_CENTER = 4
    TEXT_ALIGNMENT_TEXT_END = 3
    TEXT_ALIGNMENT_TEXT_START = 2
    TEXT_ALIGNMENT_VIEW_START = 5

    TEXT_ALIGNMENT = {
        '': TEXT_ALIGNMENT_INHERIT,
        'left': TEXT_ALIGNMENT_TEXT_START,
        'right': TEXT_ALIGNMENT_TEXT_END,
        'center': TEXT_ALIGNMENT_CENTER,
        'justified': TEXT_ALIGNMENT_INHERIT,
        'natural': TEXT_ALIGNMENT_VIEW_START
    }


class AndroidTextView(AndroidView, ProxyTextView):
    """ An Android implementation of an Enaml ProxyTextView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TextView)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = TextView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidTextView, self).init_widget()
        d = self.declaration

        if d.text:
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
        if d.text_alignment:
            self.set_text_alignment(d.text_alignment)
        if d.text_selectable:
            self.set_text_selectable(d.text_selectable)
        if d.link_color:
            self.set_link_color(d.link_color)
        if d.highlight_color:
            self.set_highlight_color(d.highlight_color)
        if d.lines:
            self.set_lines(d.lines)
        if d.line_spacing:
            self.set_line_spacing(d.line_spacing)
        if d.letter_spacing:
            self.set_letter_spacing(d.letter_spacing)
        if d.max_lines:
            self.set_max_lines(d.max_lines)
        if d.input_type:
            self.set_input_type(d.input_type)
            self.widget.addTextChangedListener(self.widget.getId())
            self.widget.onTextChanged.connect(self.on_text_changed)
        if d.editor_actions:
            self.widget.setOnEditorActionListener(self.widget.getId())
            self.widget.onEditorAction.connect(self.on_editor_action)

    # -------------------------------------------------------------------------
    # TextWatcher API
    # -------------------------------------------------------------------------
    def on_text_changed(self, text, start, before, count):
        d = self.declaration
        with self.widget.setTextKeepState.suppressed():
            d.text = text

    # -------------------------------------------------------------------------
    # OnEditorAction API
    # -------------------------------------------------------------------------
    def on_editor_action(self, view, key, key_event):
        d = self.declaration
        r = {'key': key, 'result': False}
        d.editor_action(r)
        return not not r['result']  # Apparently not not is faster than bool

    # -------------------------------------------------------------------------
    # ProxyTextView API
    # -------------------------------------------------------------------------
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
        font_style = TextView.FONT_STYLES[d.font_style or 'normal']
        #style = getattr(Typeface, d.font_style.upper() or 'NORMAL')
        #tf = Typeface.create(d.font_family or None, style)
        self.widget.setTypeface(d.font_family, font_style)  #, d.font_style)

    def set_input_type(self, input_type):
        it = TextView.INPUT_TYPES[input_type]
        self.widget.setInputType(it)

    def set_text(self, text):
        """ Set the text in the widget.

        """
        self.widget.setTextKeepState(text)  #, 0, len(text))

    def set_text_alignment(self, alignment):
        self.widget.setGravity(TextView.TEXT_ALIGNMENT[alignment])

    def set_text_selectable(self, selectable):
        self.widget.setTextIsSelectable(selectable)

    def set_text_color(self, color):
        self.widget.setTextColor(color)

    def set_highlight_color(self, color):
        self.widget.setHighlightColor(color)

    def set_link_color(self, color):
        self.widget.setLinkTextColor(color)

    def set_text_size(self, size):
        self.widget.setTextSize(size)

    def set_lines(self, lines):
        self.widget.setLines(lines)

    def set_line_spacing(self, spacing):
        self.widget.setLineSpacing(*spacing)

    def set_letter_spacing(self, spacing):
        self.widget.setLetterSpacing(spacing)

    def set_max_lines(self, lines):
        self.widget.setMaxLines(lines)


