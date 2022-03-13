"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017
"""
import sys
from types import ModuleType

API = dict(
    ActivityIndicator=".activity_indicator.ActivityIndicator",
    AutoCompleteTextView=".auto_complete_text_view.AutoCompleteTextView",
    BottomSheetDialog=".bottom_sheet_dialog.BottomSheetDialog",
    Button=".button.Button",
    ImageButton=".button.ImageButton",
    FloatingActionButton=".button.FloatingActionButton",
    Dialog=".dialog.Dialog",
    DrawerLayout=".drawer_layout.DrawerLayout",
    CalendarView=".calendar_view.CalendarView",
    CardView=".card_view.CardView",
    CheckBox=".checkbox.CheckBox",
    Chronometer=".chronometer.Chronometer",
    CoordinatorLayout=".coordinator_layout.CoordinatorLayout",
    DatePicker=".date_picker.DatePicker",
    EditText=".edit_text.EditText",
    Flexbox=".flexbox.Flexbox",
    Fragment=".fragment.Fragment",
    FrameLayout=".frame_layout.FrameLayout",
    GridLayout=".grid_layout.GridLayout",
    Icon=".iconify.Icon",
    IconButton=".iconify.IconButton",
    IconToggleButton=".iconify.IconToggleButton",
    ImageView=".image_view.ImageView",
    LinearLayout=".linear_layout.LinearLayout",
    ListView=".list_view.ListView",
    ListItem=".list_view.ListItem",
    PagerTitleStrip=".view_pager.PagerTitleStrip",
    PagerTabStrip=".view_pager.PagerTabStrip",
    PagerFragment=".view_pager.PagerFragment",
    Picker=".picker.Picker",
    ProgressBar=".progress_bar.ProgressBar",
    RadioButton=".radio_button.RadioButton",
    RadioGroup=".radio_group.RadioGroup",
    RatingBar=".rating_bar.RatingBar",
    RelativeLayout=".relative_layout.RelativeLayout",
    ScrollView=".scroll_view.ScrollView",
    SeekBar=".seek_bar.SeekBar",
    Snackbar=".snackbar.Snackbar",
    SwipeRefreshLayout=".swipe_refresh_layout.SwipeRefreshLayout",
    Spinner=".spinner.Spinner",
    Switch=".switch.Switch",
    TabLayout=".tab_layout.TabLayout",
    TabFragment=".tab_layout.TabFragment",
    TextClock=".text_clock.TextClock",
    TextView=".text_view.TextView",
    TimePicker=".time_picker.TimePicker",
    Toast=".toast.Toast",
    ToggleButton=".toggle_button.ToggleButton",
    Toolbar=".toolbar.Toolbar",
    View=".view.View",
    ViewPager=".view_pager.ViewPager",
    WebView=".web_view.WebView",
)


class LazyImporter(ModuleType):
    """Lazily import only the modules actually needed.

    References
    ----------
    1. https://github.com/pallets/werkzeug/blob/master/werkzeug/__init__.py

    """

    def __getattr__(self, name):
        if name in API:
            # print("Loading {}".format(name))
            path = API[name]
            if path.startswith("."):
                path = "enamlnative.widgets" + path
            parts = path.split(".")
            mod, widget = ".".join(parts[:-1]), parts[-1]
            module = __import__(mod, fromlist=[""])
            return getattr(module, widget)
        return super(LazyImporter, self).__getattr__(name)


old_module = sys.modules[__name__]  # So it's not garbage collected
new_module = sys.modules[__name__] = LazyImporter(__name__)
new_module.__dict__.update(
    {
        "__file__": __file__,
        "__doc__": __doc__,
        "__all__": API.keys(),
    }
)
