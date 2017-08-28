### Hello world

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
        TextView:
            text = "Hello world!"

The most basic view declaration contains an `enamldef` statement that extends a Layout and nests any child components within it. 
Above we see our `ContentView` is extending the `LinearLayout`.  The `LinearLayout` lays out it's children in
either rows or columns.

Next a `TextView` is defined within and we set the `text` property to "Hello world".


### Text Input 
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
           pass
        CheckBox: cb:
           #: Two way binding
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
           layout_height = '400'
           layout_width = 'match_parent'
        View: 
           background_color = '#0000FF'   
           layout_height = '100'
           layout_width = 'match_parent'

> Note: This will probably change once FlexBox support is added!

