"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""


def activity_indicator_factory():
    from .uikit_activity_indicator import UiKitActivityIndicator
    return UiKitActivityIndicator


def analog_clock_factory():
    from .uikit_analog_clock import UiKitAnalogClock
    return UiKitAnalogClock


def auto_complete_text_view_factory():
    from .uikit_auto_complete_text_view import UiKitAutoCompleteTextView
    return UiKitAutoCompleteTextView


def button_factory():
    # print "Import button"
    from .uikit_button import UiKitButton
    return UiKitButton


def calendar_view_factory():
    # print "Import calendar view"
    from .uikit_calendar_view import UiKitCalendarView
    return UiKitCalendarView


def card_view_factory():
    # print "Import card view"
    from .uikit_card_view import UiKitCardView
    return UiKitCardView


def checkbox_factory():
    # iOS doesn't have a checkbox
    #from .uikit_checkbox import UiKitCheckBox
    #return UiKitCheckBox
    from .uikit_switch import UiKitSwitch
    return UiKitSwitch


def chronometer_factory():
    # print "Import chronometer"
    from .uikit_chronometer import UiKitChronometer
    return UiKitChronometer


def compound_button_factory():
    # print "Import compound button"
    from .uikit_compound_button import UiKitCompoundButton
    return UiKitCompoundButton


def date_picker_factory():
    # print "Import date picker"
    from .uikit_date_picker import UiKitDatePicker
    return UiKitDatePicker


def drawer_layout_factory():
    # print "Import drawer layout"
    from .uikit_drawer_layout import UiKitDrawerLayout
    return UiKitDrawerLayout


def edit_text_factory():
    # print "Import edit text"
    from .uikit_edit_text import UiKitEditText
    return UiKitEditText


def flexbox_factory():
    from .uikit_flexbox import UiKitFlexbox
    return UiKitFlexbox

def fragment_factory():
    # print "Import frame layout"
    from .uikit_fragment import UiKitFragment
    return UiKitFragment


def frame_layout_factory():
    # print "Import frame layout"
    from .uikit_frame_layout import UiKitFrameLayout
    return UiKitFrameLayout


def grid_layout_factory():
    # print "Import grid layout"
    from .uikit_grid_layout import UiKitGridLayout
    return UiKitGridLayout


def icon_factory():
    from .uikit_iconify import UiKitIcon
    return UiKitIcon


def icon_button_factory():
    from .uikit_iconify import UiKitIconButton
    return UiKitIconButton


def icon_toggle_button_factory():
    from .uikit_iconify import UiKitIconToggleButton
    return UiKitIconToggleButton


def image_view_factory():
    from .uikit_image_view import UiKitImageView
    return UiKitImageView


def linear_layout_factory():
    # print "Import linear layout"
    from .uikit_linear_layout import UiKitLinearLayout
    return UiKitLinearLayout


def list_item_factory():
    # print "Import linear layout"
    from .uikit_list_view import UiKitListItem
    return UiKitListItem


def list_view_factory():
    # print "Import linear layout"
    from .uikit_list_view import UiKitListView
    return UiKitListView


def number_picker_factory():
    # print "Import view"
    from .uikit_number_picker import UiKitNumberPicker
    return UiKitNumberPicker


def pager_title_strip_factory():
    from .uikit_view_pager import UiKitPagerTitleStrip
    return UiKitPagerTitleStrip


def pager_tab_strip_factory():
    from .uikit_view_pager import UiKitPagerTabStrip
    return UiKitPagerTabStrip


def pager_fragment_factory():
    from .uikit_fragment import UiKitPagerFragment
    return UiKitPagerFragment


def progress_bar_factory():
    # print "Import progress bar"
    from .uikit_progress_view import UiKitProgressView
    return UiKitProgressView


def radio_button_factory():
    # print "Import radio button"
    from .uikit_radio_button import UiKitRadioButton
    return UiKitRadioButton


def radio_group_factory():
    # print "Import radio group"
    from .uikit_radio_group import UiKitRadioGroup
    return UiKitRadioGroup


def rating_bar_factory():
    # print "Import rating bar"
    from .uikit_rating_bar import UiKitRatingBar
    return UiKitRatingBar


def relative_layout_factory():
    # print "Import relative layout"
    from .uikit_relative_layout import UiKitRelativeLayout
    return UiKitRelativeLayout


def scroll_view_factory():
    # print "Import scroll view"
    from .uikit_scroll_view import UiKitScrollView
    return UiKitScrollView


def seek_bar_factory():
    from .uikit_slider import UiKitSlider
    return UiKitSlider


def spacer_factory():
    # print "Import switch"
    from .uikit_spacer import UiKitSpacer
    return UiKitSpacer


def spinner_factory():
    # print "Import spinner"
    from .uikit_spinner import UiKitSpinner
    return UiKitSpinner


def switch_factory():
    # print "Import switch"
    from .uikit_switch import UiKitSwitch
    return UiKitSwitch


def text_clock_factory():
    from .uikit_text_clock import UiKitTextClock
    return UiKitTextClock


def text_view_factory():
    # print "Import text view"
    from .uikit_text_view import UiKitTextView
    return UiKitTextView


def time_picker_factory():
    # print "Import time picker"
    from .uikit_time_picker import UiKitTimePicker
    return UiKitTimePicker


def tab_layout_factory():
    # print "Import tab host"
    from .uikit_tab_layout import UiKitTabLayout
    return UiKitTabLayout


def tab_fragment_factory():
    # print "Import tab host"
    from .uikit_tab_layout import UiKitTabFragment
    return UiKitTabFragment


def toggle_button_factory():
    # print "Import toggle button"
    from .uikit_toggle_button import UiKitToggleButton
    return UiKitToggleButton


def toolbar_factory():
    from .uikit_toolbar import UiKitToolbar
    return UiKitToolbar


def view_factory():
    # print "Import view"
    from .uikit_view import UiKitView
    return UiKitView


def view_pager_factory():
    # print "Import view pager"
    from .uikit_view_pager import UiKitViewPager
    return UiKitViewPager


def web_view_factory():
    from .uikit_web_view import UiKitWebView
    return UiKitWebView


IOS_FACTORIES = {
    'ActivityIndicator': activity_indicator_factory,
    'AnalogClock': analog_clock_factory,
    'AutoCompleteTextView': auto_complete_text_view_factory,
    'Button': button_factory,
    'CalendarView': calendar_view_factory,
    'CardView': card_view_factory,
    'CheckBox': checkbox_factory,
    'Chronometer': chronometer_factory,
    'CompoundButton': compound_button_factory,
    'DatePicker': date_picker_factory,
    'DrawerLayout': drawer_layout_factory,
    'EditText': edit_text_factory,
    'Flexbox': flexbox_factory,
    'Fragment': fragment_factory,
    'FrameLayout': frame_layout_factory,
    'GridLayout': grid_layout_factory,
    'Icon': icon_factory,
    'IconButton': icon_button_factory,
    'IconToggleButton': icon_toggle_button_factory,
    'ImageView': image_view_factory,
    'Label': text_view_factory,
    'LinearLayout': linear_layout_factory,
    'ListItem': list_item_factory,
    'ListView': list_view_factory,
    'NumberPicker': number_picker_factory,
    'PagerTitleStrip': pager_title_strip_factory,
    'PagerTabStrip': pager_tab_strip_factory,
    'PagerFragment': pager_fragment_factory,
    'ProgressBar': progress_bar_factory,
    'RadioButton': radio_button_factory,
    'RadioGroup': radio_group_factory,
    'RatingBar': rating_bar_factory,
    'RelativeLayout': relative_layout_factory,
    'ScrollView': scroll_view_factory,
    'SeekBar': seek_bar_factory,
    'Slider': seek_bar_factory, # Alias
    'Spacer': spacer_factory,
    'Spinner': spinner_factory,
    'Switch': switch_factory,
    'TabFragment': tab_fragment_factory,
    'TabLayout': tab_layout_factory,
    'TextClock': text_clock_factory,
    'TextView': text_view_factory,
    'TimePicker': time_picker_factory,
    'ToggleButton': toggle_button_factory,
    'Toolbar': toolbar_factory,
    'View': view_factory,
    'ViewPager': view_pager_factory,
    'WebView': web_view_factory,
}