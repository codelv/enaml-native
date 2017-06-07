'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''

def button_factory():
    print "Import button"
    from .android_button import AndroidButton
    return AndroidButton

def compound_button_factory():
    print "Import compound button"
    from .android_compound_button import AndroidCompoundButton
    return AndroidCompoundButton

def checkbox_factory():
    print "Import checkbox"
    from .android_checkbox import AndroidCheckBox
    return AndroidCheckBox

def radio_button_factory():
    print "Import radio button"
    from .android_radio_button import AndroidRadioButton
    return AndroidRadioButton

def radio_group_factory():
    print "Import radio group"
    from .android_radio_group import AndroidRadioGroup
    return AndroidRadioGroup

def chronometer_factory():
    print "Import chronometer"
    from .android_chronometer import AndroidChronometer
    return AndroidChronometer

def text_view_factory():
    print "Import text view"
    from .android_text_view import AndroidTextView
    return AndroidTextView

def linear_layout_factory():
    print "Import linear layout"
    from .android_linear_layout import AndroidLinearLayout
    return AndroidLinearLayout

def relative_layout_factory():
    print "Import relative layout"
    from .android_relative_layout import AndroidRelativeLayout
    return AndroidRelativeLayout

def frame_layout_factory():
    print "Import frame layout"
    from .android_frame_layout import AndroidFrameLayout
    return AndroidFrameLayout

def grid_layout_factory():
    print "Import grid layout"
    from .android_grid_layout import AndroidGridLayout
    return AndroidGridLayout

def calendar_view_factory():
    print "Import calendar view"
    from .android_calendar_view import AndroidCalendarView
    return AndroidCalendarView

def edit_text_factory():
    print "Import edit text"
    from .android_edit_text import AndroidEditText
    return AndroidEditText

def time_picker_factory():
    print "Import time picker"
    from .android_time_picker import AndroidTimePicker
    return AndroidTimePicker

def date_picker_factory():
    print "Import date picker"
    from .android_date_picker import AndroidDatePicker
    return AndroidDatePicker

def scroll_view_factory():
    print "Import scroll view"
    from .android_scroll_view import AndroidScrollView
    return AndroidScrollView

def spinner_factory():
    print "Import spinner"
    from .android_spinner import AndroidSpinner
    return AndroidSpinner

def view_factory():
    print "Import view"
    from .android_view import AndroidView
    return AndroidView

def view_group_factory():
    print "Import view group"
    from .android_view_group import AndroidViewGroup
    return AndroidViewGroup

def drawer_layout_factory():
    print "Import drawer layout"
    from .android_drawer_layout import AndroidDrawerLayout
    return AndroidDrawerLayout

def tab_widget_factory():
    print "Import widget factory"
    from .android_tab_widget import AndroidTabWidget
    return AndroidTabWidget

def tab_host_factory():
    print "Import tab host"
    from .android_tab_host import AndroidTabHost
    return AndroidTabHost

def progress_bar_factory():
    print "Import progress bar"
    from .android_progress_bar import AndroidProgressBar
    return AndroidProgressBar


ANDROID_FACTORIES = {
    'View': view_factory,
    'ViewGroup': view_group_factory,
    'TextView': text_view_factory,
    'LinearLayout': linear_layout_factory,
    'RelativeLayout': relative_layout_factory,
    'FrameLayout': frame_layout_factory,
    'GridLayout': grid_layout_factory,
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
    'Spinner': spinner_factory,
    'TabWidget': tab_widget_factory,
    'TabHost': tab_host_factory,
    'ProgressBar': progress_bar_factory,
}