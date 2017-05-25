'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''

def button_factory():
    from .android_button import AndroidButton
    return AndroidButton

def compound_button_factory():
    from .android_compound_button import AndroidCompoundButton
    return AndroidCompoundButton

def checkbox_factory():
    from .android_checkbox import AndroidCheckBox
    return AndroidCheckBox

def radio_button_factory():
    from .android_radio_button import AndroidRadioButton
    return AndroidRadioButton

def radio_group_factory():
    from .android_radio_group import AndroidRadioGroup
    return AndroidRadioGroup

def chronometer_factory():
    from .android_chronometer import AndroidChronometer
    return AndroidChronometer

def text_view_factory():
    from .android_text_view import AndroidTextView
    return AndroidTextView

def linear_layout_factory():
    from .android_linear_layout import AndroidLinearLayout
    return AndroidLinearLayout

def relative_layout_factory():
    from .android_relative_layout import AndroidRelativeLayout
    return AndroidRelativeLayout

def frame_layout_factory():
    from .android_frame_layout import AndroidFrameLayout
    return AndroidFrameLayout

def calendar_view_factory():
    from .android_calendar_view import AndroidCalendarView
    return AndroidCalendarView

def edit_text_factory():
    from .android_edit_text import AndroidEditText
    return AndroidEditText

def time_picker_factory():
    from .android_time_picker import AndroidTimePicker
    return AndroidTimePicker

def date_picker_factory():
    from .android_date_picker import AndroidDatePicker
    return AndroidDatePicker

def scroll_view_factory():
    from .android_scroll_view import AndroidScrollView
    return AndroidScrollView

def view_factory():
    from .android_view import AndroidView
    return AndroidView

def view_group_factory():
    from .android_view_group import AndroidViewGroup
    return AndroidViewGroup

def drawer_layout_factory():
    from .android_drawer_layout import AndroidDrawerLayout
    return AndroidDrawerLayout

ANDROID_FACTORIES = {
    'View': view_factory,
    'ViewGroup': view_group_factory,
    'TextView': text_view_factory,
    'LinearLayout': linear_layout_factory,
    'RelativeLayout': relative_layout_factory,
    'FrameLayout': frame_layout_factory,
    'DrawerLayout': drawer_layout_factory,
    'CalendarView': calendar_view_factory,
    'Button': button_factory,
    'CompoundButton': compound_button_factory,
    'CheckBox': checkbox_factory,
    'Chronometer': chronometer_factory,
    'RadioButton': radio_button_factory,
    'RadioGroup': radio_group_factory,
    'EditText': edit_text_factory,
    'TimePicker': time_picker_factory,
    'DatePicker': date_picker_factory,
    'ScrollView': scroll_view_factory,
}