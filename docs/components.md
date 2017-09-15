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

More to come... 
