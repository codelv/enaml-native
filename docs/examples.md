### Playground

The easiest way to try out these examples is by downloading the [Python Playground]() app. This app allows you to paste code into a web based editor and run it as if it were built as part of the app!

Once downloaded, start the app, and then go to [http://your-phone-address:8888](http://localhost:8888). If using a simulator run `adb forward tcp:8888 tcp:8888` and go to [http://localhost:8888](http://localhost:8888).

Copy and paste the example code in and click the play button. The app reloads and there you go! You can try out any code this way as well so feel free to play around!

### Basics

#### Text

Use a `TextView` to show text. You can set color, size, font, and other properties.  
    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
        TextView:
            text = "Hello world!"
            text_color = "#00FF00"
            text_size = 32
            font_family = "sans-serif"



#### Text Inputs
You can observe text input changes by binding to the `text` attribute.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
        orientation = "vertical"
        EditText: et1:
           pass
        EditText: et2:
           #: Two way binding
           text := et1.text
        TextView:
            text << "You typed: {}".format(et1.text)




### Toggle Switch 
You can handle Switch, CheckBox, and ToggleButton checked changes with the `checked` attribute.

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(LinearLayout):
        orientation = "vertical"
        Switch: sw:
           text = "Switch"
        CheckBox: cb:
            text = "Checkbox"
            #: Two way binding
            checked := sw.checked
        PushButton:
            text = "PushButton"
            checked := sw.checked
        TextView:
            text << "Switch state: {}".format(sw.checked)



### Button 
You can handle button clicks with the `clicked` event.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
        Button: btn:
           attr clicks = 0
           text = "Click me!"
           clicked :: self.clicks +=1
        TextView: txt:
           text << "Clicked: {}".format(btn.clicks)



### Clickable 
Any `View` can be made clickable by setting `clickable=True` and using the `clicked` event.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
        TextView: txt:
           attr clicks = 0
           text << "Click me: {}".format(self.clicks)
           clickable = True
           clicked :: self.clicks +=1



### Width and Height 
You can define size using `layout_width` and `layout_height`. Can be either an integer string `200` (in dp), `wrap_content`, or `match_parent`.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
        orientation = "vertical"
        View: 
           background_color = '#00FF00'   
           layout_height = '200'
           layout_width = 'match_parent'
        View: 
           background_color = '#FFFF00'   
           layout_height = '300'
           layout_width = 'match_parent'
        View: 
           background_color = '#0000FF'   
           layout_height = '100'
           layout_width = 'match_parent'

> Note: This will probably change once Flexbox support is added!





