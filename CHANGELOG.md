
# enaml-native 3.0.0

Introduces a major redesign in the core widget initialization

Changes

- Redesign widget initialization to only set attributes defined in the enaml
declaration of the widget.  This should improve speed and memory usage as it now will reduce
the number of checks required for initialization.

- Fix a major layout issue where layout parameters were not properly applied based on the parent 
container. Now all `Flexbox` parameters (such as `align_self`, `min_width`, etc..) will work when
a view is nested in a `Flexbox` layout.

- Removed `AnalogClock`, `TabWidget` (not `TabLayout`), and `Spacer` widgets as they are rarely 
ever used.



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

