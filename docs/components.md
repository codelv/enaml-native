### Components

Usage examples of every component should go here.  At some point editable examples should be added. 

### ActivityIndicator

Displays a circular loading indicator.


    :::python

    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
      #: Normal size
      ActivityIndicator:
        pass

      #: Small
      ActivityIndicator:
        style = "small"

      #: Large
      ActivityIndicator:
        style = "large"
  

### AnalogClock

An analog clock. 
 
    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
      #: Normal size
      AnalogClock:
        pass

> Note: This widget is depreciated on Android


### AutoCompleteTextView

A text field with autocomplete items.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        flex_direction = "column"

        TextView:
            text = "Pet type"

        AutoCompleteTextView: tv:
            #: Autocomplete items 
            choices = ['Cat','Dog', 'Duck','Bird','Elephant', "Fish"]

            #: Min letters before autocomplete
            threshold = 1

            #: Placeholder
            placeholder = "Type an animal name"

        TextView:
            text << "Selection: {}".format(tv.text)

### Button

A clickable button with different styles.
    
    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        flex_direction = "column"

        TextView: tv:
            pass    

        Looper:
            iterable = list(Button.style.items)
            Button:
                text = loop_item or "default"

                #: Button style
                style = loop_item

                #: Listen to click events 
                clicked :: tv.text = "Style {}".format(loop_item)


        Button:
            text = "default"
            text_color = "#f00"
            font_family = "sans-serif-light"
            text_size = 32
            style = "borderless"

        Button:
            text = "borderless"
            style = "borderless"
            text_color = "#c1a"
        

You can also set any `TextView` attributes such as `background_color`, `text_color`, `text_size` and `font_family`.

### CalendarView

A calendar widget that lets you set and choose a date within a range.
    
    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        flex_direction = "column"

        CalendarView: cv:
            pass

        TextView:
            text << "Date: {}".format(cv.date)

### CardView

A material design "card" or bordered view with a shadow.
    
    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        flex_direction = "column"
        background_color = "#eee"
        padding = (10,10,10,0)

        CardView:
            #: Padding inside card
            content_padding = (20, 20, 20, 20)

            #: Border radius
            radius = 30

            #: Elevation or "shadow"
            card_elevation = 10

            #: Content is usually a layout container (ie flexbox)
            Flexbox:
                TextView:
                    text = "This is a card!"
                    text_size = 32

### CheckBox

A checkbox widget with a "checked" property.
    
    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        flex_direction = "column"

        CheckBox: cb:
            text = "CheckBox"
            checked = True

        CheckBox:
            text = "Bound checkbox"
            checked := cb.checked
            
### Chronometer

A timer widget that increments every second. You can observe the `ticks` attribute and start/stop with the `running` attribute.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        flex_direction = "column"

        Chronometer: cm:
            text_size = 32
            running = True

        TextView:
            text << "Elapsed: {} seconds".format(cm.ticks)
            
### CompoundButton

This is an abstract component and should not be used directly.

### DatePicker

A widget for picking dates including years. Observe the `date` attribute for changes.
    
    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        flex_direction = "column"
        align_items = "center"
        DatePicker: dp:
            pass

        TextView:
            text << "Date: {} ".format(dp.date)
            
### Dialog

A popup dialog that displays a view as it's content. Show it by setting `show=True` and hide by setting it to `False`.
 
 [![Dialogs in enaml-native](https://img.youtube.com/vi/dxW2KCy67vU/0.jpg)](https://youtu.be/dxW2KCy67vU)

Disable cancellation by setting `cancel_on_back` and/or `cancel_on_touch_outside` to `False`.

The `style` can also be set to make it fullscreen using the `@style/<resource>` syntax.

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
        Button:
            text = "Open dialog"
            clicked :: dialog.show = True
        #: Prevent cancelling without pressing a button
        CheckBox:
            text = "Cancel on touch outside"
            checked := dialog.cancel_on_touch_outside
        CheckBox:
            text = "Cancel on back"
            checked := dialog.cancel_on_back
        TextView:
            text << "Show: {}".format(dialog.show)
        Dialog: dialog:
            Flexbox:
                flex_direction = "column"
                justify_content = "space_between"
                Flexbox:
                    flex_direction = "column"
                    padding = (20, 20, 20, 50)
                    TextView:
                        text = "Are you sure you want to delete?"
                        font_family = "sans-serif-medium"
                    TextView:
                        text = "This operation cannot be undone."
                Flexbox:
                    justify_content = "space_between"
                    Button:
                        style = "borderless"
                        text = "Ok"
                        clicked :: 
                            print("ok!")
                            dialog.show = False
                    Button:
                        style = "borderless"
                        text = "Cancel"
                        clicked :: dialog.show = False


> Note: This allows you to use custom views. There are also other native dialogs (alerts, pickers, etc.. ) that may better suite your needs.

### DrawerLayout

A layout component that allows you to create a left and/or right drawer. The first child is the "content" and subsequent children will be drawers if they have a `layout_gravity` and `layout_width` attributes assigned. Use the `opened` attribute to open and close the drawers from code.

    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *

    enamldef Drawer(ScrollView): view:
        #: Must have layout_gravity AND layout_width
        layout_gravity = 'left'
        layout_width = '200'
        background_color = "#fff"
        Flexbox:
            flex_direction = "column"
            Looper:
                iterable = range(20)
                Button:
                    style = "borderless"
                    text = "{} {}".format(view.layout_gravity, loop_index)

    enamldef ContentView(DrawerLayout): drawer:
        background_color = "#eee"
        Flexbox:
            flex_direction = "column"
            Toolbar:
                title = "Drawers"
                subtitle = "Swipe to open drawers"
                background_color = "#abc"
            Button:
                text = "Open left"
                #: Set the `opened` attribute to the list of drawers
                clicked :: drawer.opened = [left_drawer]
            Button:
                text = "Open right"
                clicked :: drawer.opened = [right_drawer]
            Button:
                text = "Close all"
                #: Set the `opened` attribute to an empty list to close all
                clicked :: drawer.opened = []

        Drawer: left_drawer:
            layout_gravity = "left"
        Drawer: right_drawer:
            layout_gravity = "right"

### EditText

A text input field that can be set to accept differnt types (password, phone, etc..). Observe the `text` attribute to respond to changes.  

    :::python
    from enamlnative.widgets.api import *

    enamldef Text(TextView):
        #: Add Spacing
        padding = (0, 20, 0, 0)

    enamldef ContentView(Flexbox):
        flex_direction = "column"

        Text:
            text = "Observe the text attribute for responding to changes"
        EditText: et:
            text = ""
        EditText: 
            text := et.text

        Text:
            text = "Set placholder text"
        EditText:
            placeholder = "Placeholder here"

        Text:
            text = "Set input types to change keyboard and display"
        EditText:
            placeholder = "Input type password"
            input_type = "text_password"
        EditText:
            placeholder = "Input type phone"
            input_type = "phone"

        Text:
            text = "Respond to keyboard actions"
        EditText: editor:
            attr action = None
            placeholder = "Press the keyboard send button"
            editor_actions = True
            editor_action :: self.action = change
        Text:
            text << "{}".format(editor.action)

You can to respond to keyboard "actions" (ie the send button pressed) by setting `editor_actions=True` and observing `editor_action` events.  This event passes a dictionary as it's value with two important entries `result` and `key`. 

If you set the `result` of event value dictionary to True via `change['value']['result'] = True` it will tell the widget that the action was handled and the keyboard should NOT close  (it closes by default).  

The `key` of the event value dictionary is a code that represent the key pressed. See the android [EditorInfo](https://developer.android.com/reference/android/view/inputmethod/EditorInfo.html) docs for the keycodes.

### Flexbox

For flexbox usage see the layouts section in [learning the basics](https://www.codelv.com/projects/enaml-native/docs/learn-the-basics#layouts)

### Fragment

Fragment is a special component that subclasses the `Conditional` block and is meant for providing pages to a [ViewPager](#viewpager). It's preferred to use the [PagerFragement](#pagerfragment) instead of using this directly however they both will work as childen of a pager. See the [ViewPager](#viewpager) component docs for more info.

### FrameLayout

A wrapper for android's [FrameLayout](https://developer.android.com/reference/android/widget/FrameLayout.html). It's preferred to use Flexbox for layouts however some custom native components may subclass this.


### GridLayout

A wrapper for android's [GridLayout](https://developer.android.com/reference/android/widget/GridLayout.html). It's preferred to use Flexbox for layouts.

### Icon

A component for displaying icons. It extends the `TextView` component and uses [android-iconify](https://github.com/JoanZapata/android-iconify) behind the scenes. All icon packs are included by default.

> Note: Icons now require the [enaml-native-icons](https://github.com/codelv/enaml-native-icons) package

[![Icons in enaml-native](https://img.youtube.com/vi/K0hiyV6SBms/0.jpg)](https://youtu.be/K0hiyV6SBms)

Icon packs

1. [fontawesome // (v4.5)](http://fontawesome.io/icons/)
2. [entypo  // (v3,2015)](http://entypo.com/)
3. [typicons // (v2.0.7)](http://www.typicons.com/)
4. [material // (v2.0.0)](https://material.io/icons/)
5. [material-community // (v1.4.57)](https://materialdesignicons.com/)
6. [meteocons // (latest)](http://www.alessioatzeni.com/meteocons/)
7. [weathericons // (v2.0)](https://erikflowers.github.io/weather-icons/)
8. [simplelineicons // (v1.0.0)](http://simplelineicons.com/)
9. [ionicons // (v2.0.1)](https://ionicframework.com/docs/ionicons/)

To use them simply add `{<icon_name>}` in the Icon's text attribute. You can set the text_color, text_size, font_familiy, as well or optionally can use the inline [icon options](https://github.com/JoanZapata/android-iconify#icon-options).

Try the simple icon finder example.

    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *

    enamldef Text(TextView):
        #: Add Spacing
        padding = (0, 20, 0, 0)

    enamldef ContentView(ScrollView): finder:
        attr icons << getattr(Icon,"PACK_%s"%icon_pack.items[icon_pack.selected].replace(" ","_").upper())
        padding = (10, 10, 10, 10)
        Flexbox:
            flex_direction = "column"
            CardView:
                Flexbox:
                    flex_direction = "column"
                    layout_height = "wrap_content"
                    Text:
                        text = "Icons"
                        text_size = 32
                    Text:
                        text = "Use {icon-name} within the text. Uses android-iconify. Browse an icon pack below" \
                             "or pick an icon from the pack here"
                    Text:
                      text = "Icon packs"
                    Spinner: icon_pack:
                      items = ['Entypo','Font awesome','Ionicons', 'Material community', 'Material',
                                'Meteocons', "Weather"]

                    Text:
                      text = "Icon"
                    AutoCompleteTextView: search:
                        choices << list(finder.icons)
                        text << finder.icons[0]

                    Flexbox: display:
                        padding = (0, 20, 0, 20)
                        attr text << u"{%s}"%(search.text) if search.text in finder.icons else "" 
                        Looper:
                            iterable = [72, 64, 48, 32, 24, 18]
                            Icon:
                                text_size = loop_item
                                padding = (8, 0, 8, 0)
                                text << display.text

                    Text:
                        text = "Manual"
                    EditText: manual:
                        editor_actions = True
                        placeholder = "Put your icon code here"
                        editor_action :: 
                            if change['value']['key'] == 6:
                                display.text = self.text
                                #: Keep keyboard open
                                change['value']['result'] = True
                    Text:
                        text = "Warning: it's easy to blow up with a typo here!"
                        text_color = "#f00"


                    #: Use one because it's way f,aster than a looper
                    Text:
                      text = "Icons"
                    Icon:
                      text_size = 32
                      text << u" ".join([u"{%s}"%n for n in finder.icons])



### IconButton

It's a button that allows Icons in the text. See the [Icon](#icon) and [Button](#button) components.


### IconToggleButton

It's a toggle button that allows Icons in the text. See the [Icon](#icon) and [ToggleButton](#togglebutton) components.

### MapView

A `GoogleMap` component. All of the `Map<Item>` components can be added as children. 

> Note: This has moved to the [enaml-native-maps](https://github.com/codelv/enaml-native-maps) package

Map click events can be handled with the `clicked` event which passes a `change['value']` dict containing the `position` and `click` type. 

The camera position, zoom, tilt and bearing can be set or observed. See [Android camera position](https://developers.google.com/maps/documentation/android-api/views#the_camera_position) 
for mored etails.

    :::python
    import random
    from enamlnative.android.app import AndroidApplication
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *
    from enamlnative.android.api import LocationManager
    
    enamldef ContentView(DrawerLayout): view:
        attr num_markers = 10
        attr markers_draggable = True
        attr marker_rotation = 0
        attr marker_alpha = 1
        attr markers_flat = True
        attr center = (39.95090, -86.26190)
        attr points << [(center[0]+random.randint(0,100)/1000.0*i,
                                center[1]+random.randint(0,100)/1000.0*i) for i in range(view.num_markers)]
        MapView: mapview:
            rotate_gestures = False
            show_toolbar = False
            camera_position << view.center
            camera_zoom = 10
            clicked::
                if change['value']['click']=='long':
                    pts = view.points[:]
                    pts.append(change['value']['position'])
                    view.points = pts
            Looper:
                iterable << view.points
                MapMarker:
                    attr angle << view.marker_rotation
                    position = loop_item
                    position ::
                        toast.text = "Marker {} moved {}".format(loop_index,self.position)
                        toast.show = True
                    dragging::
                        if not change['value']:
                            #: Dragging stopped
                            #: Update point
                            pts = view.points[:]
                            pts[loop_index] = self.position
                            view.points = pts
                        
                    title = "Marker {}".format(loop_index)
                    snippit = "Caption {}".format(loop_index)
                    draggable << view.markers_draggable
                    rotation << view.marker_rotation
                    flat << view.markers_flat
                    alpha << view.marker_alpha
                    clicked :: 
                        #: Set the odd markers as "handled"
                        change['value']['handled'] = False
                        toast.text = "Clicked {}".format(loop_index)
                        toast.show = True
                    info_clicked :: 
                        #: Set the odd markers as "handled"
                        toast.text = "Info window {} {} clicked".format(loop_index,change['value']['click'])
                        toast.show = True
                    custom_info_window_mode = 'content'
                    Conditional:
                        condition = bool(loop_index & 1)
                        Flexbox:
                            align_items = 'center'
                            Icon:
                                text = "{fa-cog}"
                                padding = (0,10,10,10)
                            TextView:
                                text = "Item: {}".format(loop_index)
            MapPolyline:
                points << view.points
                color = "#90F0"
                clickable = True
                clicked :: 
                    toast.text = "Polyline clicked"
                    toast.show = True
            MapPolygon:
                points << view.points[:3]
                fill_color = "#300F"
                stroke_color = "#900F"
                clickable = True
                clicked :: 
                    toast.text = "Polygon clicked"
                    toast.show = True
            MapCircle:
                position << view.center
                radius = 3000
                fill_color = "#30FF"
                stroke_color = "#90FF"
                clickable = True
                clicked ::
                    toast.text = "Circle clicked"
                    toast.show = True
            Toast: toast:
                text = "Marker"
                duration = 300
        ScrollView:
            layout_gravity = "left"
            layout_width = "200"
            background_color = "#fff"
            Flexbox:
                padding = (10,10,10,10)
                flex_direction = "column"
                TextView:
                    text = "Camera"
                    text_size = 18
                TextView:
                    text << "Zoom {}".format(mapview.camera_zoom)
                SeekBar:
                    max = 20
                    progress << int(mapview.camera_zoom)
                    progress :: mapview.camera_zoom = float(change['value'])
                TextView:
                    text << "Position {}".format(mapview.camera_position)
                Button:
                    text = "Recenter"
                    clicked :: mapview.camera_position = view.center
                TextView:
                    text = "Markers"
                    text_size = 18
                Switch:
                    text = "Draggable"
                    checked := view.markers_draggable
                Switch:
                    text = "Flat"
                    checked := view.markers_flat
                TextView:
                    text << "Rotation ({})".format(view.marker_rotation)
                SeekBar:
                    max = 360
                    progress := view.marker_rotation
                TextView:
                    text << "Alpha ({})".format(view.marker_alpha)
                SeekBar:
                    max = 100
                    progress << int(view.marker_alpha*100)
                    progress :: view.marker_alpha = change['value']/100.0
                Button:
                    text = "Add marker"
                    style = "borderless"
                    clicked :: view.num_markers +=1
                Button:
                    text = "Remove marker"
                    style = "borderless"
                    clicked :: view.num_markers = max(1,view.num_markers-1)
                TextView:
                    text = "Selection"
                Spinner:
                    items << ["Marker {}".format(i) for i in range(view.num_markers)]
                    selected :: 
                        w = mapview.children[change['value']]
                        w.show_info = True
                            
                TextView:
                    text = "Maps"
                    text_size = 18
                Switch:
                    text = "Show buildings"
                    checked := mapview.show_buildings
                Switch:
                    text = "Show location"
                    checked := mapview.show_location
                Button:
                    text = "Request permission"
                    style = "borderless"
                    clicked :: LocationManager.request_permission()
                Switch:
                    text = "Show traffic"
                    checked := mapview.show_traffic
                TextView:
                    text = "Layers"
                    text_size = 18
                Spinner:
                    items = list(MapView.map_type.items)
                    selected << self.items.index(mapview.map_type)
                    selected :: mapview.map_type = self.items[change['value']]

### MapMarker

A marker that can be added to a map at a given `position` (tuple of `(lat,lng)`). Set the `title` and `snippit` text for the info window. 

The `dragging` attribute can be observed to tell if it started or stopped dragging. Set `draggable=True` to enable dragging.
 
 A child view can be used to populate the info window. Info windows can be `long` or `short` clicked and handeld with `info_clicked` events.

See the [MapView](#mapview) example for usage.

### MapCircle

A circle that can be added to a map. Set the `position` and `radius` to define the size and location. Styles can be set via `fill_color` and `stroke_color`.

It can be made clickable by setting `clickable=True` and handling `clicked` events. 

See the [MapView](#mapview) example for usage.

### MapPolyline

A polyline that can be added to a map. Set the `points` to a list of `(lat,lng)` coordinates. Styles can be set via `color` and `width`.

It can be made clickable by setting `clickable=True` and handling `clicked` events. 

See the [MapView](#mapview) example for usage.

### MapPolygon

A polygon that can be added to a map. Set the `points` to a list of `(lat,lng)` coordinates. Styles can be set via `fill_color`, `stroke_color`, and `stroke_width`.

It can be made clickable by setting `clickable=True` and handling `clicked` events. 

See the [MapView](#mapview) example for usage.


### PagerFragment

Adds a page to [ViewPager](#viewpager).

### PagerTabStrip

Adds a "tab strip" to a [ViewPager](#viewpager). It's similar to tabs but only displays the current, next, and previous tab. Can set the different text and indicator colors. Items are automatically added when a `PagerFragment` is added to the `ViewPager`.

Set the `title` of the `PagerFragment` to define the text of the tab.
 
[![Pager title strip in enaml-native](https://img.youtube.com/vi/UdAaUNUD3eY/0.jpg)](https://youtu.be/UdAaUNUD3eY)


    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
    
        ViewPager:
            PagerTabStrip: pager_tab_strip:
                text_color = '#eee'
                inactive_alpha = 0.7
                text_size = 16
                tab_indicator_color = '#97c024'
                background_color = '#3574a3'
            Looper:
                iterable << ['First', 'Second', 'Third']
                PagerFragment:
                  title = loop_item
                  Flexbox:
                    background_color = '#fff'
                    flex_direction = 'column'
                    padding = (10,10,10,10)
                    Spinner:
                      items = ['top', 'bottom']
                      selected << 0 if pager_tab_strip.layout_gravity == 'top' else 1
                      selected :: pager_tab_strip.layout_gravity = self.items[self.selected]


### PagerTitleStrip

See the [PagerTabStrip](#pagertabstrip).


### Picker

A value picker from a "slot machine" style spinning list. Use the `items` property to set the text values. And use `value` to read the selected value (or item index).
 
 [![Pickers enaml-native](https://img.youtube.com/vi/yGHEvlg5uRo/0.jpg)](https://youtu.be/yGHEvlg5uRo)

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
    
        #: Numeric by default (on android)
        Picker: pk1:
          min_value = 0
          max_value = 100
          value = 20
        TextView:
          text << "Selected: {}".format(pk1.value)
    
        #: Use items for strings
        Picker: pk2:
          items = ["blue",'red','green','orange','yellow','white','black']
        TextView:
          text << "Selected: {}".format(pk2.items[pk2.value])

### ProgressBar

Simply set the `progress` attribute.

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
    
        ProgressBar: pb:
            progress = 50
    
        SeekBar:
            progress := pb.progress


### RadioButton

A `RadioButton` should be a child of a `ReadioGroup`. See [RadioGroup](#radiogroup) for usage. You can set the `text` and `checked` attributes but generally `checked` is should be used by the group.

### RadioGroup

A container for a set of radio buttons. Only only one may be selected at a time. The selected button (if one is selected) will be set as the `checked` attribute.

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
    
        RadioGroup: rg:
            # Or set it
            RadioButton:
                text = "A"
            RadioButton:
                text = "B"
            RadioButton:
                text = "C"
                checked = True
        TextView:
            text << "Selected: {}".format(rg.checked.text if rg.checked else "None")
    
        RadioGroup: rg2:
            # Or set it
            checked = rg2.children[0]
            RadioButton:
                text = "A"
            RadioButton:
                text = "B"
            RadioButton:
                text = "C"
        TextView:
            text << "Selected: {}".format(rg2.checked.text if rg2.checked else "None")


### RatingBar

A "star" rating that can be adjusted like a slider or seekbar. Set or observe the `rating` as needed. Use `is_indicator=True` to make it read only.
 
 > Note: A RatingBar on Android should be a child of a LinearLayout to display properly.

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
        LinearLayout:
            RatingBar: rbar1:
                num_stars = 3
                rating = 1
                #: Prevents moving
                is_indicator = True
        TextView:
            text << "Fixed Rating {}".format(rbar1.rating)
        LinearLayout:
            RatingBar: rbar2:
                rating = 5
        TextView:
             text << "Rating {}".format(rbar2.rating)


### Seekbar

A seekbar is like a slider or controllable progress bar that lets you select a from a continuous range of values.

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
        SeekBar: seekbar:
          progress = 12
          max = 20
        TextView:
          text << "Value {}".format(seekbar.progress)

> Note: The `min` attribute only is supported for Android api 26 and above. Simply add the min to progress value as needed.


### Snackbar

A Snackbar displays a message at the bottom of the screen with an action button. Set the `action_text` to enable actions.

[![Toast and Snackbar in enaml-native](https://img.youtube.com/vi/4zRgHin2d9s/0.jpg)](https://youtu.be/4zRgHin2d9s)

> Note: A Snackbar MUST be a child of either a `FrameLayout` (or subclass) or a `CoordinatorLayout`. Using a `CoordinatorLayout` enables support for swiping to dismiss. 


    :::python
    from enamlnative.widgets.api import *
    from enamlnative.android.app import AndroidApplication
    
    enamldef ContentView(CoordinatorLayout):
        Flexbox:
            flex_direction = "column"
            Button: 
                text = "Show snackbar"
                clicked :: 
                    sb.show = True
            TextView:
                text << "Snackbar state: {}".format("active" if sb.show else "hidden")
            TextView: tv:
                attr action = ""
                text << "Snackbar action: {}".format(self.action)
            Button: 
                text = "Show snackbar with action"
                clicked :: 
                    sb2.show = True
        Snackbar: sb:
            duration = 4000
            text = "Cheers!"
        
        Snackbar: sb2:
            text = "Email deleted"
            action_text = "Undo"
            clicked :: print("action clicked!")
            action :: 
                tv.action = change['value']


### Spacer

A pretty "space" widget for adding spacing to a layout. This is not really used anymore and may be removed in the future.


### Spinner

A spinner is a dropdown menu list. Set the `items` attribute to the values to display and set or observe the `selected` index to handle changes.

 
 [![Spinners enaml-native](https://img.youtube.com/vi/yGHEvlg5uRo/0.jpg)](https://youtu.be/yGHEvlg5uRo)


    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
        Spinner: sp:
            items = ["blue",'red','green','orange','yellow','white','black']
        TextView:
          text << "Selected: {}".format(sp.items[sp.selected])

> Note: Currently the text attributes (ex font, color, size, etc..) cannot be changed.

### Switch

An "on/off" switch. It has the same api as a `CheckBox` with `text` and `checked` attributes commonly being used.
 
 
    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
        
        Switch: sw:
            text = "Switch"
            checked = True
   
        Switch:
            text = "Bound switch"
            checked := sw.checked

### SwipeRefreshLayout

A layout that lets you swipe down to trigger a refresh. Use the `refreshed` event to handle reload. The following example also shows the http usage.

    :::python
    from enamlnative.widgets.api import *
    from enamlnative.core.http import AsyncHttpClient
    
    enamldef ContentView(Flexbox): view:
        flex_direction = "column"
        attr httpclient = AsyncHttpClient()
        attr request
        SwipeRefreshLayout:
            trigger_distance = 10
            indicator_color = "#0F0"
            indicator_background_color = "#EEE"
            refreshed::
                f = httpclient.fetch(http_url.text)
                view.request = f.request
            ScrollView:
                Flexbox:
                    flex_direction = "column"
                    EditText: http_url:
                        text = "http://worldclockapi.com/api/json/est/now"
                    TextView:
                        text = "Swipe to refresh"
                    Conditional:
                        condition << request is not None
                        ProgressBar:
                            progress << request.response.progress
                        TextView:
                            text << "Status: {} Reason: ".format(
                                      request.response.status_code,
                                      request.response.reason,
                                )
                        Conditional:
                            condition << request.response.ok
                            TextView:
                              text << "{}".format(request.response.content)

### TabFragment

A page of a `ViewPager` that works with a `TabLayout`. See the [TabLayout](#tablayout) for usage.

### TabLayout

Adds tabs to a [ViewPager](#viewpager). Can set the different text and indicator colors. Tabs are automatically added when a `TabFragment` is added to the `ViewPager`.

Set the `title` of the `TabFragment` to define the text of the tab.
 
[![Tabs in enaml-native](https://img.youtube.com/vi/hNXCHNe_Zik/0.jpg)](https://youtu.be/hNXCHNe_Zik)


    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
    
        ViewPager:
            TabLayout: tab_layout:
                tab_color = '#7fff'
                tab_color_selected = '#fff'
                background_color = '#3574a3'
            Looper:
                iterable << ['First', 'Second', 'Third']
                TabFragment:
                  title = loop_item
                  Flexbox:
                    background_color = '#fff'
                    flex_direction = 'column'
                    padding = (10,10,10,10)
                    Spinner:
                      items = ['top', 'bottom']
                      selected << 0 if tab_layout.layout_gravity == 'top' else 1
                      selected :: tab_layout.layout_gravity = self.items[self.selected]
                    TextView:
                      text = "Tab modes"
                    Spinner:
                      items = ['fixed','scrollable']
                      selected << 0 if tab_layout.tab_mode == 'fixed' else 1
                      selected :: tab_layout.tab_mode = self.items[self.selected]
                    TextView:
                      text = "Tab gravity"
                    Spinner:
                      items = ['fill', 'center']
                      selected << 0 if tab_layout.tab_gravity == 'fill' else 1
                      selected :: tab_layout.tab_gravity = self.items[self.selected]

### Toast

A toast flashes a simple message to the user for a given duration. Set the `show` attribute to `True` to display it. It will automatically hide after the given duration.
 
 [![Toast and Snackbar in enaml-native](https://img.youtube.com/vi/4zRgHin2d9s/0.jpg)](https://youtu.be/4zRgHin2d9s)

You can also show a toast message from code using the `AndroidApplication.instance().show_toast(msg)` api.
  
    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        flex_direction = "column"
        Button: 
            text = "Show toast"
            clicked :: 
                toast.show = True
        TextView:
            text << "Toast: {}".format("active" if toast.show else "hidden")        
        Button: 
            text = "Show custom toast"
            clicked :: 
                toast2.show = True

        Toast: toast:
            text = "Cheers!"

        Toast: toast2:
            #: Time in ms to flash
            duration = 5000
            #: Custom component
            CardView: card:
                background_color = "#555"
                radius = 10
                Flexbox:
                    align_items = "center"
                    padding = (20, 10, 20, 10)
                    Icon:
                        text_color = "#fff"
                        text = "{fa-check}"
                    TextView:
                        padding = (10, 10, 10, 10)
                        text = "PAGE ADDED"
                        text_color = "#fff"

> Note: Clicks events are NOT supported in custom Toasts on Android! Use a [Snackbar](#snackbar) instead!

### ViewPager

A viewpager lets you swipe between multiple screens. You can set the `paging_enabled` attribute to `False` to only allow changing programatically. Observe or set the `current_index` to change the page.
 
To add Pages you must add a `TabFragment` or `PagerFragment` (any subclass of `Fragment`). Tabs and a pager strip can also be added.

> Note: Pages can now use a different `transition`. 
See [android-viewpager-transformers](https://github.com/geftimov/android-viewpager-transformers/wiki)
 
  
 [![View pager and screens in enaml-native](https://img.youtube.com/vi/QjYptyQETcU/0.jpg)](https://youtu.be/QjYptyQETcU)

 
    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *
    
    enamldef Navigation(Toolbar): toolbar:
        #: An "iOS" like navigation where the text scrolls out when the pages change
        background_color = "#CCC"
        attr text_color = "#039be5"
        layout_height = "140"
        content_padding = (4,4,4,4)
        attr pager
        Flexbox:
            justify_content = "space_between"
            align_items = "center"
            IconButton:
                enabled << pager.current_index>0
                background_color << toolbar.background_color
                text << "{md-arrow-back}" if self.enabled else ""
                text_size = 32
                text_color << toolbar.text_color
                style = "borderless"
                clicked :: pager.current_index -= 1 
            Flexbox:
                layout_width = "wrap_content"
                ViewPager:
                    current_index := pager.current_index
                    paging_enabled = False
                    Looper:
                        iterable = pager.pages
                        PagerFragment:
                            Flexbox:
                                justify_content = "center"
                                align_items = "center"
                                TextView:
                                    text = loop_item.title
                                    #text_color << toolbar.text_color
                                    text_size = 18
                                    font_family = 'sans-serif-medium'
            IconButton:
                enabled << pager.current_index<len(pager.pages)-1
                text << "{md-arrow-forward}" if self.enabled else ""
                background_color << toolbar.background_color
                text_size = 32
                text_color << toolbar.text_color
                style = "borderless"
                clicked :: pager.current_index += 1
    
    enamldef BottomNav(Toolbar): view:
        attr pager 
        background_color = "#ccc"
        layout_height = "140"
        attr active_color = "#039be5"
        Flexbox:
            justify_content = "space_between"
            align_items = "center"
            Looper:
                iterable << pager.pages
                IconButton:
                    text = loop_item.icon
                    text_color << view.active_color if pager.current_index == loop_index else "#777"
                    text_size = 32
                    style = "borderless"
                    clicked :: pager.current_index = loop_index
    
    enamldef ContentView(Flexbox): view:
        flex_direction = "column"
        Navigation:
            pager << screens
        ViewPager: screens:
            paging_enabled = True
            PagerFragment:
                title = "Home"
                icon = "{md-home}"
                TextView:
                    text = "Python powered native apps!"
            PagerFragment:
                title = "Pictures"
                icon = "{md-photo}"
                TextView:
                    text = "Content goes here!"
            PagerFragment:
                title = "Settings"
                icon = "{md-settings}"
                TextView:
                    text = "A multi screen app in < 20 lines? Yep!"
        BottomNav:
            pager << screens
              

### WebView

A component for loading a web page. Use the `url` to set the page. You can observe `title`, `loading`, `progress`, and `error` to see the state. 

Control the page by triggering the `go_forward`, `go_back`, and `reload` events.

 
 [![Webview in enaml-native](https://img.youtube.com/vi/L3IVK1ogMZ4/0.jpg)](https://youtu.be/L3IVK1ogMZ4)


    :::python
    from enamlnative.android.app import AndroidApplication
    from enamlnative.widgets.api import *
    
    enamldef ContentView(ScrollView): web_view:
        LinearLayout:
            orientation = "vertical"
            EditText: web_url:
              text = "github.com/frmdstryr/enaml-native"
              input_type = 'text_uri'
              editor_actions = True
              editor_action ::
                #: When done editing, load the page
                action = change['value']
                if action['key']==5: # Why 5 now?
                  url = web_url.text.lower()
                  if not (url.startswith("http://") or url.startswith("https://")):
                    url = "https://"+url
                  web_view.url = url
            ProgressBar:
              visible << web_view.loading
              progress << web_view.progress
            TextView:
              visible << web_view.error
              text_color = '#FF0000'
              text << u"Error: {} - {}".format(web_view.error_code, web_view.error_message)
            WebView: web_view:
              layout_height = 'match_parent'
              layout_width = 'match_parent'
              #: When url updates, set the text
              url = "https://github.com/frmdstryr/enaml-native"
              url >> web_url.text
              title :: AndroidApplication.instance().show_toast(change['value'])




More to come... 
