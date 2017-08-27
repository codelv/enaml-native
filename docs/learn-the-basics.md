### Intro

Enaml-native is like Enaml, but it uses native Android or iOS components instead of Qt components as building blocks. So to understand the basic structure of an enaml-native app, you need to understand some of the basic Enaml concepts, like declarative components and data binding operators.  If you already know Enaml, you still need to learn some enaml-native specifics.


### Hello world

As is standard, let's start with a "Hello world" app.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
        TextView:
            text = "Hello world!"



### What's going on here?

This doesn't look like python? We're using enaml to define a _view_ within our app. Enaml is a subset of the python language that provides a very powerful way of building UI's. 

If you're unfamiliar with enaml read the [enaml introduction](https://nucleic.github.io/enaml/docs/get_started/introduction.html) to get an idea of what it is and why it's used. Once done read about the [enaml syntax](https://nucleic.github.io/enaml/docs/get_started/anatomy.html). Enaml is at the core of enaml-native.

First, all the enaml-native components are imported using a standard python import statement. Next the `enamldef` keyword is used to define a new component named `ContentView` that extends the `LinearLayout` component. The `enamldef` keyword has similarities to the `class` keyword in python. After that we add a `TextView` to our layout and assign the `"Hello world!"` expression to the `text` attribute of the view.  In enaml, everything on the right hand side is evaluated lazily within the context of the view state at runtime where you can reference other components and their state. 


### Components

Above we see our code is defining `ContentView`, a new component that is extending the `LinearLayout`. If you're familiar with Android or iOS, the `LinearLayout` (or `UIStackView`) is a widget that lays out it's children in either a single row or column, in this case the child is the `TextView`. This is a very simple component declaration, with enaml-native new components are created often. Everything you see on the screen is some sort of component. Components can be simple or complex but, like a python class, must have at least one body statement (which can just be the `pass` keyword).  

### Attributes

Components can be customized by setting attributes. These are like python class attributes but they use the [atom framework](https://github.com/nucleic/atom) and are often type restricted. Attributes are set to customize the underlying native widget so it is created and updated as desired. For example the text of a button or the checked state of a switch.

Attempting to set an attribute that has not been defined by the component will throw an error.  Often times you need to hold extra state within the component. You can define custom attributes using the `attr` keyword.


    :::python
    from enamlnative.widgets.api import *
    from atom.api import Unicode
    
    enamldef Count(View):
        #: A new attribute with a default of 0
        attr count = 0
        
        #: A new attribute that is restricted to a given type
        attr name: Unicode


These custom attributes can then be used like any other enaml attribute.

### References

Components often need to reference other components for interactions or to update their state accordingly. References are made by adding a `<name>:` after the component.  Once defined, references can be used to access the attributes of a component.


    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(View):
        TextView: echo_me:
          text = "Hello"
          
        TextView:
          #: Use the reference `echo_me` 
          text = echo_me.text
        

The example is pretty useless, but you get the idea. References are used very often within enaml-native apps.

### Operators

One of the most powerful features of enaml is it's data binding operators. Enaml's data binding operators are what makes enaml much nicer than working with react or react-native in many cases.  The operators are `>>`, `<<`, `:=`, `::` and `=`.

#### Simple = operator

The `=` operator sets the inital state of the attribute. The attribute may later be changed by other components that interact with it.

#### Subscribe << operator

The `<<` operator a one way binding from a model to the UI component. This allows your UI to automatically update whenever a change occurs in your model and it automatically binds to changes in any atom objects used in the python expression. 


    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(View):
        Switch: sw:
          checked = False
          
        TextView: tv:
          #: Use subscribe operator to update the label whenever the switch changes
          text << "Checked {}".format(sw.checked)

In the above example, whenever the user toggles the switch, the text updates to display the switches checked state.

#### Update >> operator

The `>>` operator is a one way binding that notifies the component when the UI component updates the attribute. This allows your UI changes to then be properly handled (ex, updating your model). 

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(View):
        Switch: sw1:
          checked = False
          checked >> sw2.checked
        Switch: sw2:
          checked = False
          
In this example, when switch `sw1` is toggled, switch `sw2` will also be set to the same state. However if switch `sw2` is toggled, switch `sw1` will not change. 


#### Delegate := operator

The `:=` operator does a two way binding between the UI component and a model (or another components's) attribute. This allows you to easily keep two attributes in sync (ex, UI attribute and model attribute or two UI attributes).

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(View):
        Switch: sw1:
          checked := sw2.checked
        Switch: sw2:
          checked = True

In this example, toggling either switch will cause the other to toggle as well. Both switches will always stay in sync even though only one is being applied.  Generally this operator will be used to bind to an attribute of a data model.

    :::python
    from atom.api import Atom, Bool
    from enamlnative.widgets.api import *
    
    class Model(Atom):
      enabled = Bool()
    
    enamldef ContentView(View):
        attr model = Model()
        Switch:
          checked := model.enabled

In the above example our model's enabled state will be bound to the switch checked state. If either are changed they will both stay in sync.

#### Notify :: operator

The `::` operator notifies the component when an event occurs, such as a button click, and allows you to handle the event as needed.

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(View):
        Button:
          clicked ::
              #: This block of code will execute when clicked
              print("Button was clicked!")

Above we see the notify operator triggers the _event handler_ directly within the component. Any python code (except for `yield` and `return` statments can be used within the handler block. 

#### More about operators

There's a good talk by the developer of enaml [on youtube](https://www.youtube.com/watch?v=ycFEwz_hAxk&t=3s) where he describes the operators in more detail. 

If you're familiar with react or react-native programming, these operators eliminate the need for `setState`, the "flux" pattern, and other state containers such as `Redux`. Enaml and Atom handle all of the state and changes for you.  

If you're familiar with Android or iOS programming, this entirely eliminates the need to add listeners, callback functions, or use key value observers. Enaml and the native toolkit implementation(s) handles all of this seamlessly behind the scenes. See the more advanced documentation or the code for more details if you're interested.

### Dynamic Components

Docs coming soon!

#### Conditionals


#### Loopers


#### Blocks



### Layouts

Coming soon...
