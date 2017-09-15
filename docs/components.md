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
                    AutoCompleteTextView: search:
                        choices << list(finder.icons)
                        text << finder.icons[0]

                    Flexbox:
                        Looper:
                            iterable = [72, 64, 48, 32, 24, 18]
                            Icon:
                                text_size = loop_item
                                padding = (8, 0, 8, 0)
                                text << u"{%s}"%search.text if search.text in finder.icons else "" #: TODO: Trigger on value accepted
            CardView:
              Flexbox:
                    flex_direction = "column"
                    Text:
                      text = "Icon packs"
                    Spinner: icon_pack:
                      items = ['Entypo','Font awesome','Ionicons', 'Material community', 'Material',
                                'Meteocons', "Weather"]
                    #: Use one because it's way faster than a looper
                    Icon:
                      text_size = 32
                      text << u" ".join([u"{%s}"%n for n in finder.icons])



### IconButton

It's a button that allows Icons in the text. See the [Icon](#icon) and [Button](#button) components.




More to come... 
