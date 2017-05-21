'''
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

ANDROID_FACTORIES = {
    'TextView': text_view_factory,
    'LinearLayout': linear_layout_factory,
    'RelativeLayout': relative_layout_factory,
    'FrameLayout': frame_layout_factory,
    'CalendarView': calendar_view_factory,
    'Button': button_factory,
    'CompoundButton': compound_button_factory,
    'CheckBox': checkbox_factory,
    'Chronometer': chronometer_factory,
}