"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
from atom.api import Bool, Enum, Event, Float, ForwardTyped, Int, Str, Tuple, Typed
from enaml.core.declarative import d_, observe
from .view import ProxyView, View


class ProxyTextView(ProxyView):
    """The abstract definition of a proxy Label object."""

    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: TextView)

    def set_all_caps(self, enabled: bool):
        raise NotImplementedError

    def set_auto_link_mask(self, mask: int):
        raise NotImplementedError

    def set_input_type(self, input_type: str):
        raise NotImplementedError

    def set_font_family(self, family: str):
        raise NotImplementedError

    def set_font_style(self, style: str):
        raise NotImplementedError

    def set_text(self, text: str):
        raise NotImplementedError

    def set_text_color(self, color: str):
        raise NotImplementedError

    def set_text_alignment(self, alignment: str):
        raise NotImplementedError

    def set_highlight_color(self, color: str):
        raise NotImplementedError

    def set_link_color(self, color: str):
        raise NotImplementedError

    def set_text_size(self, size: float):
        raise NotImplementedError

    def set_lines(self, lines: int):
        raise NotImplementedError

    def set_line_spacing(self, spacing: tuple[float, ...]):
        raise NotImplementedError

    def set_letter_spacing(self, spacing: float):
        raise NotImplementedError

    def set_max_lines(self, lines: int):
        raise NotImplementedError

    def set_text_selectable(self, selectable: bool):
        raise NotImplementedError

    def append_text(self, text: str):
        raise NotImplementedError


class TextView(View):
    """A simple control for displaying read-only text."""

    #: Sets the properties of this field to transform input to
    #: ALL CAPS display.
    all_caps = d_(Bool())

    #: Sets the autolink mask of the text.
    auto_link_mask = d_(Int(0))

    #: Listen for edit actions
    editor_actions = d_(Bool())

    #: Listen for editor actions
    editor_action = d_(Event(dict), writable=False)

    #: Input type or types separated by "|"
    #: See https://developer.android.com/reference/android/widget/TextView.html
    #: attr_android:inputType
    input_type = d_(Str())

    INPUT_TYPES = (
        "date",
        "datetime",
        "number",
        "number_decimal",
        "number_password",
        "number_signed",
        "phone",
        "text",
        "text_auto_complete",
        "text_auto_correct",
        "text_cap_characters",
        "text_cap_sentences",
        "text_cap_words",
        "text_email_address",
        "text_email_subject",
        "text_filter",
        "text_ime_multi_line",
        "text_long_message",
        "text_multi_line",
        "text_no_suggestions",
        "text_password",
        "text_person_name",
        "text_phonetic",
        "text_postal_address",
        "text_short_message",
        "text_uri",
        "text_visible_password",
        "text_web_edit_text",
        "text_web_email_address",
        "text_web_password",
        "time",
    )

    #: Font family
    font_family = d_(Str())

    #: Font style
    font_style = d_(Enum("normal", "bold", "italic", "bold_italic"))

    #: Sets the color used to display the selection highlight.
    highlight_color = d_(Str())

    #: Sets the color of links in the text.
    link_color = d_(Str())

    #: The unicode text for the label.
    text = d_(Str())

    #: Text alignment
    text_alignment = d_(Enum("", "left", "right", "center", "justified", "natural"))

    #: Sets the text color for all the states (normal, selected, focused)
    #: to be this color.
    text_color = d_(Str())

    #: Set the default text size to the given value, interpreted as
    #: "scaled pixel" units.
    text_size = d_(Float(strict=False))

    #: Set text s
    text_selectable = d_(Bool())

    #: Sets the height of the TextView to be exactly lines tall.
    lines = d_(Int())

    #: Sets the line spacing
    line_spacing = d_(Tuple((int, float)))

    #: Sets the line spacing
    letter_spacing = d_(Float(strict=False))

    #: Sets the height of the TextView to be at most maxLines tall.
    max_lines = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyTextView)

    # -------------------------------------------------------------------------
    # Observers
    # -------------------------------------------------------------------------
    @observe(
        "all_caps",
        "auto_link_mask",
        "input_type",
        "font_family",
        "font_style",
        "text_selectable",
        "text",
        "text_color",
        "text_size",
        "text_alignment",
        "link_color",
        "highlight_color",
        "lines",
        "max_lines",
        "line_spacing",
        "letter_spacing",
    )
    def _update_proxy(self, change):

        super()._update_proxy(change)

    # -------------------------------------------------------------------------
    # TextView API
    # -------------------------------------------------------------------------
    def append_text(self, text):
        """Add text to the existing text"""
        self.proxy.append_text(text)
