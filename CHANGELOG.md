# enaml-native 4.5.0

- Refactor ListView to use RecyclerAdapter and support container
operations (append, insert, remove, pop)
- Fix issue with builtin event loop with Python 3

# enaml-native 4.4.2

- Support screen orientation changes
- Set width and height of application in dp units

# enaml-native 4.4.1

- Speed up msgpack with use_list=False
- Compat changes to support python versions
- Use pipe to redirect library output to logcat

# enaml-native 4.4.0

- Add the `style` attribute for _all_ widgets that support it 
ex `style='@attr/borderlessButtonStyle'`
- Add the `background_style` attribute so you can make an clickable view have touch animations
by using `background_style='?attr/selectableItemBackground'`
(see [Ripple-Animation](https://guides.codepath.com/android/Ripple-Animation))
- Add "complex" style support when parsing android resources starting with `?`
- Update several examples
- Minor fixes to Spinner and RatingBar

# enaml-native 4.3

- Change minimumSdkLevel and APP_PLATFORM to 21

# enaml-native 4.2.4

- Simplify location by using a dict
- Support more notificaton features

# enaml-native 4.2.3

- Add notifications

# enaml-native 4.2.2

- Allow appending to a TextView directly
- Disable scrollbars on loading view
- Let loading view be overridden

# enaml-native 4.2.1

- Add missing click handlers in `ListView` and `ListItem`

# enaml-native 4.2.0

- [Glide](http://bumptech.github.io/glide/) is not added for loading images into ImageView's
by default.
- `JavaMethod` and `JavaStaticMethod` will now strip any trailing underscores from the name 
allowing you to define multiple method with different signatures with the same name by 
appending 1 or more '_'.  
- Add files for building the conda recipe here

# enaml-native 4.1.1

- Add support for html in `TextView` by setting `input_type = 'html'` using Android's Html.fromHtml.
See the [supported tags](https://stackoverflow.com/questions/9754076/which-html-tags-are-supported-by-android-textview#10262460)

# enaml-native 4.1.0

- Add `PopupWindow` that lets you build context menus or absolutely positioned views.

# enaml-native 4.0.3

- Add `popup` method to open dialogs from code

# enaml-native 4.0.2

- Fix padding and margin order

# enaml-native 4.0.1

- Add app bar layout

# enaml-native 4.0.0

- Python-for-android and kivy-ios have been completely dropped in favor of 
[conda-mobile](https://github.com/codelv/conda-mobile)

- Android updated to use api instead of compile
- Android starts python in a Thread instead of using AsyncTask


# enaml-native 3.1.0

Refactor Services to use a common API for retrieving instances.

# enaml-native 3.0.1

Make dev server not use autoreload.


# enaml-native 3.0.0

Introduces a major redesign in the core widget initialization

Changes

- Redesign widget initialization to only set attributes defined in the enaml
declaration of the widget.  This should improve speed and memory usage as it now will reduce
the number of checks required for initialization.

- Refactor event loops to add `then` and `catch` in a much more efficient way

- Refactor how events are batched together. It now will update as soon as control returns
to the eventloop or after 5ms occurs. 

- Fix a major layout issue where layout parameters were not properly applied based on the parent 
container. Now all `Flexbox` parameters (such as `align_self`, `min_width`, etc..) will work when
a view is nested in a `Flexbox` layout.

- Removed `AnalogClock`, `TabWidget` (not `TabLayout`), and `Spacer` widgets as they are rarely 
ever used.

- Scrollbars can now be hidden using `scrollbars = 'none'`

- ViewGroups (ie Flexbox, LinearLayout, ...) can now animate adding or removing children by setting
`transition = 'default'`



Migrating


- `layout_width`, `layout_height`, and `layout_gravity` have been changed 
to `width`, `height` and `gravity`. `width` and `height` are now coerced to an
int so `100`, `'100'`, `match_parent`, and `wrap_content` are valid values. 

- The `margins` attribute has been renamed to `margin` to match css
 
- The `layout` attribute has been removed and it's properties `align_self`, `min_width`, `max_width`, 
`min_height`, `max_height`, and `flex_basis` are all now added to all Views 


- ActivityIndicator `style` has been changed to `size`

- Button `style` has been removed and replaced with `flat=True` to indicate a borderless or "Flat" 
Button.

