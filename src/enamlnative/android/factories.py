"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""


def activity_indicator_factory():
    from .android_activity_indicator import AndroidActivityIndicator
    return AndroidActivityIndicator


def analog_clock_factory():
    from .android_analog_clock import AndroidAnalogClock
    return AndroidAnalogClock


def auto_complete_text_view_factory():
    from .android_auto_complete_text_view import AndroidAutoCompleteTextView
    return AndroidAutoCompleteTextView


def button_factory():
    from .android_button import AndroidButton
    return AndroidButton


def calendar_view_factory():
    from .android_calendar_view import AndroidCalendarView
    return AndroidCalendarView


def card_view_factory():
    from .android_card_view import AndroidCardView
    return AndroidCardView


def checkbox_factory():
    from .android_checkbox import AndroidCheckBox
    return AndroidCheckBox


def chronometer_factory():
    from .android_chronometer import AndroidChronometer
    return AndroidChronometer


def coordinator_layout_factory():
    from .android_coordinator_layout import AndroidCoordinatorLayout
    return AndroidCoordinatorLayout


def compound_button_factory():
    from .android_compound_button import AndroidCompoundButton
    return AndroidCompoundButton


def date_picker_factory():
    from .android_date_picker import AndroidDatePicker
    return AndroidDatePicker


def dialog_factory():
    from .android_dialog import AndroidDialog
    return AndroidDialog


def drawer_layout_factory():
    from .android_drawer_layout import AndroidDrawerLayout
    return AndroidDrawerLayout


def edit_text_factory():
    from .android_edit_text import AndroidEditText
    return AndroidEditText


def flexbox_factory():
    from .android_flexbox import AndroidFlexbox
    return AndroidFlexbox


def fragment_factory():
    from .android_fragment import AndroidFragment
    return AndroidFragment


def frame_layout_factory():
    from .android_frame_layout import AndroidFrameLayout
    return AndroidFrameLayout


def grid_layout_factory():
    from .android_grid_layout import AndroidGridLayout
    return AndroidGridLayout


def icon_factory():
    from .android_iconify import AndroidIcon
    return AndroidIcon


def icon_button_factory():
    from .android_iconify import AndroidIconButton
    return AndroidIconButton


def icon_toggle_button_factory():
    from .android_iconify import AndroidIconToggleButton
    return AndroidIconToggleButton


def image_view_factory():
    from .android_image_view import AndroidImageView
    return AndroidImageView


def linear_layout_factory():
    from .android_linear_layout import AndroidLinearLayout
    return AndroidLinearLayout


def list_item_factory():
    from .android_list_view import AndroidListItem
    return AndroidListItem


def list_view_factory():
    from .android_list_view import AndroidListView
    return AndroidListView


def picker_factory():
    from .android_picker import AndroidPicker
    return AndroidPicker


def pager_title_strip_factory():
    from .android_view_pager import AndroidPagerTitleStrip
    return AndroidPagerTitleStrip


def pager_tab_strip_factory():
    from .android_view_pager import AndroidPagerTabStrip
    return AndroidPagerTabStrip


def pager_fragment_factory():
    from .android_fragment import AndroidPagerFragment
    return AndroidPagerFragment


def progress_bar_factory():
    from .android_progress_bar import AndroidProgressBar
    return AndroidProgressBar


def radio_button_factory():
    from .android_radio_button import AndroidRadioButton
    return AndroidRadioButton


def radio_group_factory():
    from .android_radio_group import AndroidRadioGroup
    return AndroidRadioGroup


def rating_bar_factory():
    from .android_rating_bar import AndroidRatingBar
    return AndroidRatingBar


def relative_layout_factory():
    from .android_relative_layout import AndroidRelativeLayout
    return AndroidRelativeLayout


def scroll_view_factory():
    from .android_scroll_view import AndroidScrollView
    return AndroidScrollView


def seek_bar_factory():
    from .android_seek_bar import AndroidSeekBar
    return AndroidSeekBar


def spacer_factory():
    from .android_spacer import AndroidSpacer
    return AndroidSpacer


def spinner_factory():
    from .android_spinner import AndroidSpinner
    return AndroidSpinner


def snackbar_factory():
    from .android_snackbar import AndroidSnackbar
    return AndroidSnackbar


def switch_factory():
    from .android_switch import AndroidSwitch
    return AndroidSwitch


def swipe_refresh_layout_factory():
    from .android_swipe_refresh_layout import AndroidSwipeRefreshLayout
    return AndroidSwipeRefreshLayout


def text_clock_factory():
    from .android_text_clock import AndroidTextClock
    return AndroidTextClock


def text_view_factory():
    from .android_text_view import AndroidTextView
    return AndroidTextView


def time_picker_factory():
    from .android_time_picker import AndroidTimePicker
    return AndroidTimePicker


def tab_layout_factory():
    from .android_tab_layout import AndroidTabLayout
    return AndroidTabLayout


def tab_fragment_factory():
    from .android_tab_layout import AndroidTabFragment
    return AndroidTabFragment


def toast_factory():
    from .android_toast import AndroidToast
    return AndroidToast


def toggle_button_factory():
    from .android_toggle_button import AndroidToggleButton
    return AndroidToggleButton


def toolbar_factory():
    from .android_toolbar import AndroidToolbar
    return AndroidToolbar


def view_factory():
    from .android_view import AndroidView
    return AndroidView


def view_pager_factory():
    from .android_view_pager import AndroidViewPager
    return AndroidViewPager


def web_view_factory():
    from .android_web_view import AndroidWebView
    return AndroidWebView


ANDROID_FACTORIES = {
    'ActivityIndicator': activity_indicator_factory,
    'AnalogClock': analog_clock_factory,
    'AutoCompleteTextView': auto_complete_text_view_factory,
    'Button': button_factory,
    'CalendarView': calendar_view_factory,
    'CardView': card_view_factory,
    'CheckBox': checkbox_factory,
    'Chronometer': chronometer_factory,
    'CoordinatorLayout': coordinator_layout_factory,
    'CompoundButton': compound_button_factory,
    'DatePicker': date_picker_factory,
    'Dialog': dialog_factory,
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
    'LinearLayout': linear_layout_factory,
    'ListItem': list_item_factory,
    'ListView': list_view_factory,
    'PagerTitleStrip': pager_title_strip_factory,
    'PagerTabStrip': pager_tab_strip_factory,
    'PagerFragment': pager_fragment_factory,
    'Picker': picker_factory,
    'ProgressBar': progress_bar_factory,
    'RadioButton': radio_button_factory,
    'RadioGroup': radio_group_factory,
    'RatingBar': rating_bar_factory,
    'RelativeLayout': relative_layout_factory,
    'ScrollView': scroll_view_factory,
    'SeekBar': seek_bar_factory,
    'Spacer': spacer_factory,
    'Spinner': spinner_factory,
    'Snackbar': snackbar_factory,
    'Switch': switch_factory,
    'SwipeRefreshLayout': swipe_refresh_layout_factory,
    'TabFragment': tab_fragment_factory,
    'TabLayout': tab_layout_factory,
    'TextClock': text_clock_factory,
    'TextView': text_view_factory,
    'TimePicker': time_picker_factory,
    'Toast': toast_factory,
    'ToggleButton': toggle_button_factory,
    'Toolbar': toolbar_factory,
    'View': view_factory,
    'ViewPager': view_pager_factory,
    'WebView': web_view_factory,
}