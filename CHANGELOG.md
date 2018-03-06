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

