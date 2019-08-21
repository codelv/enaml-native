
## Hello World

A new app will load the `ContentView` and render it's components. 

```python

from enamlnative.widgets.api import Flexbox, TextView

enamldef ContentView(Flexbox):
    TextView:
        text = "Hello world!"

```

The `enamldef` is just like the python `class` statement. You can subclass components and set 
attributes or add child components to them.  

This doesn't really do anything so how about something more interesting.

## Setting attributes

Most components can be customized when they are created, with different parameters. 
These creation parameters are called `properties`, `members` or `attributes`. 

For example, one basic component is the ImageView. When you create an image, you can 
use an attribute named `src` to control what image it shows.


```python

from enamlnative.widgets.api import Flexbox, ImageView

enamldef ContentView(Flexbox):
    ImageView:
        src = "https://upload.wikimedia.org/wikipedia/commons/d/de/Bananavarieties.jpg"
        width = 193
        height = 110

```

Your own components can also use the `attr` keyword to define new members. This lets you make a 
single component that is used in many different places in your app, with slightly different 
attributes in each place. Here's an example
 
 
```python

from enamlnative.widgets.api import Flexbox, TextView

enamldef Greeting(TextView):
    attr name = ""
    text << "Hello {}".format(name)

enamldef ContentView(Flexbox):
    flex_direction = "column"
    align_items = "center"
    Greeting:
        name = "Bob"
    Greeting:
        name = "Jane"    
    Greeting:
        name = "Angel"
```

Creating the `Greeting` subclass of the `TextView` and adding the `attr name` lets us customize the 
component with our own attributes.  These attributes are stored within a component instance when 
 it's added as child of another component.

## Changing state

Attributes of components in enaml-native are stateful. Whenever an attribute is changed, enaml
will update the UI automatically. This means you can update the UI by simply updating the value of 
an attributes.  

```python

from enaml.application import Application
from enamlnative.widgets.api import Flexbox, TextView

enamldef Blink(TextView):
    #: Visible by default
    visible = True
    
    #: Called when component is activated
    activated :: blink()
    
    #: Blink and then schedule it to blink again
    func blink():
        # Toggle the visibility
        self.visible = not self.visible
        
        # Schedule blink again 1 second later
        app = Application.instance()
        app.timed_call(1000, blink)


enamldef ContentView(Flexbox):
    flex_direction = "column"
    Blink:
        text = "Python is cool"
    Blink:
       text = "But on mobile it's better"
    Blink:
       text = "And that's a wrap"

```

This will make the text of each "Blink" component flash on an off. There's also some more powerful 
ways to handle state changes, which we'll discuss shortly, but for now let's discuss what's
going on here.

When the `ContentView` is shown it walks down the tree activates all child components. Here we
set a handler when the `activated` event occurs in the `Blink` component and have it call a 
function that toggles the `visible` attribute of the View.  

The use of the `func` keyword is like `def` for defining a method in python. The difference is it 
will know the current component as `self`, and have access to the scope of the block it's in.

Enaml's application event loop provides the `timed_call` method which lets us schedule a function 
and it's parameters to be called later, like a timer.  Here we schedule the `blink` function 
in a "scheduled" loop ever 1000ms. 

> Note: The built in event loop uses [tornado's ioloop](http://www.tornadoweb.org/en/stable/ioloop.html)

## Changing styles

Nearly all components in enaml-native subclass the basic `View` component which lets you customize
the style by setting the`background_color`. Many components also subclass the `TextView` which
lets you customize the common text properties of the component such as `text_color`, `text_size`, 
`font_family`, and `font_style`.

> See [TextView](http://enaml-native.readthedocs.io/en/latest/widgets/textview.html#enamlnative.widgets.text_view.TextView)
for a full list of attributes


## Padding and margin

To add spacing around a component set the `padding` to a list of the `[left, top, right, bottom]`
padding in `dp` units. When nested in a layout that supports it, you can also use `margin` in the
same format.

## Width and height

You can set the `width` and `height` to a specific number or tell it to `match_parent` or 
`wrap_content`. Setting one to `wrap_content` will make it use only the space needed in that 
dimension, while `match_parent` will fill up as much as it can.

When a component is nested in a `Flexbox` layout, the width and height can also be defined by using
the `flex_basis`. 


## Handling events

Users interact with mobile apps mainly through touch. They can use a combination of gestures, 
such as tapping on a button, scrolling a list, or zooming on a map.

enaml-native exposes many of the events components receive allowing you to handle all sorts of 
common gestures, but the one component you will most likely be interested in is the basic `Button`.

```python

from enamlnative.android.application import AndroidApplication
from enamlnative.widgets.api import Flexbox, Button

enamldef ContentView(Flexbox):
    flex_direction = "column"
    align_items = "center"
    Button:
        text = "Press me"
        clicked :: AndroidApplication.instance().show_toast("You tapped the button!")
```

Pressing the button will trigger the "clicked" event, which will run handler we set 
in this case displays an popup message. The `::` here signifies a notification block, which is
just the handler code that will run when the event occurs.

> If you like, you can specify a "text_color" to change the color of your button or set "flat=True"
to make it render without the button border.

## Clickable

In some cases, the basic button doesn't look right for your app, you can build your own button 
by making any `View` clickable. This is done by setting `clickable=True` and then handling the
`clicked` event like a regular `Button`. 

```python

from enamlnative.android.application import AndroidApplication
from enamlnative.widgets.api import Flexbox, Button

enamldef ContentView(Flexbox):
    flex_direction = "column"
    align_items = "center"
    Flexbox:
        clickable = True
        clicked :: AndroidApplication.instance().show_toast("Row touched!")
        background_style = "?attr/selectableItemBackground" 
        Icon:
            text = "{fa-user}"
        TextView:
            text = "Touchable row"
        
```
  
> Android: If you want to add a different touch animation you can change 
 `background_style = "?attr/selectableItemBackground"` to your own animation. 


## Atom models

It's very common for UI's to follow the model view controller (MVC) pattern. The basic premise is
that the data that your app displays should be represented by a "Model" and the UI is just one
"View" into the Model. The controller's job is to handle the interactions between the two. Enaml 
provides some special python classes and operators to make this easy for you.

Say we wanted to make a simple Places's app display a list of places, and when one is selected
it shows a page with more details. One way to do this would be to make a model for the app's
state, and a model for the contact. Here's an example.

```python
from atom.api import Atom, List, Bool, Range, Enum, Unicode, Instance

class Place(Atom):
    name = Unicode()
    address = Unicode()
    enabled = Bool()
    rating = Range(0, 5)
    
class AppState(Atom):
    places = List(Place)
    current_place = Instance(Place)
    current_screen = Enum('list', 'details')


```

The [atom](https://github.com/nucleic/atom) framework provides memory efficient constructs on top
of python that help you model things in your app.  It's somewhat similar to django's models in that
it will provide type checking and has constructs for associating objects with each other. Let's
see how this can be used.

```python
from enamlnative.widgets.api import Flexbox, TextView
from models import AppState, Place

#: Create a global instance of the state
#: this could also be made into a singleton
state = AppState()

enamldef PlaceDetails(Dialog):
    attr place: Place
    Flexbox:
        flex_direction = 'column'
        TextView:
            text << place.name
        TextView:
            text << place.address
        LinearLayout:
            RatingBar: 
                rating << place.rating
        Button:
            flat = True
            text = "Back"
            clicked :: state.current_screen = 'list'
        
enamldef PlacesList(Flexbox):
    attr places = []
    flex_direction = "column"
    Looper:
        iterable << places
        Flexbox:
            attr place = loop_item
            clickable = True
            clicked :: 
                state.current_place = place
                state.current_screen = 'details'
            TextView:
                text << place.name

enamldef ContentView(ScrollView):
    PlacesList:
        places << state.places
    PlaceDetails:
        place << state.current_place
        show << state.current_screen == 'place_details'

```

Above, we could use the `AppState` class to store where the user is within the app. When an item
is selected from the `places` list, we simply update our app state by setting the `current_place` 
to the one selected and update the `current_screen` to go to the "details" page. 

Using a `state` model keeps everything organized in one place and easily let's us serialize it
to push it to a server or save it locally in a file to be restored later.