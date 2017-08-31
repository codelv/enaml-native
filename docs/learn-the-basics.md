### Intro

Enaml-native is like Enaml, but it uses native Android or iOS components instead of Qt components as building blocks. So to understand the basic structure of an enaml-native app, you need to understand some of the basic Enaml concepts, like declarative components and data binding operators.  If you already know Enaml, you still need to learn some enaml-native specifics.


### Hello world

As is standard, let's start with a "Hello world" app.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
        TextView:
            text = "Hello world!"


This doesn't look like python? We're using enaml to define a _view_ within our app. Enaml is a subset of the python language that provides a very powerful way of building UI's. 

If you're unfamiliar with enaml read the [enaml introduction](https://nucleic.github.io/enaml/docs/get_started/introduction.html) to get an idea of what it is and why it's used. Once done read about the [enaml syntax](https://nucleic.github.io/enaml/docs/get_started/anatomy.html). Enaml is at the core of enaml-native.

First, all the enaml-native components are imported using a standard python import statement. Next the `enamldef` keyword is used to define a new component named `ContentView` that extends the `LinearLayout` component. The `enamldef` keyword has similarities to the `class` keyword in python. After that we add a `TextView` to our layout and assign the `"Hello world!"` expression to the `text` attribute of the view.  In enaml, everything on the right hand side is evaluated lazily within the context of the view state at runtime. This lets you reference other components and their state. 


### Components

With enaml-native new components are created often. Everything you see on the screen is some sort of component. Components can be simple or complex but, like a python class, must have at least one body statement (which can just be the `pass` keyword).

A component is defined by extending an existing component and specifying any attributes or children the new component needs. Above the `ContentView` is a new component extends the `LinearLayout` component and includes a `TextView` child. Components are commonly used to encapsulate several views with a desired layout and the attributes required to populate the view. Doing this makes parts of your app easier to reuse and makes your code easier to read much like classes do in object-oriented programming. 

Many builtin components are simply wrappers around native widgets that expose their functionality as attributes. If you're familiar with Android or iOS, the `LinearLayout` (or `UIStackView`) is a widget that lays out it's children in either a single row or column. When we use this component it's creating the native widget and any required properties or adapters for us.  It's possible to define your own components to wrap any special native widgets you may have, see the more advanced documentation for that. 

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
    
    enamldef ContentView(LinearLayout):
        #: Define a reference variable of `echo_me`
        TextView: echo_me:
          text = "Hello"
          
        TextView:
          #: Use the reference `echo_me` 
          text = echo_me.text
        

The example is pretty useless, but you get the idea. There's also a few other useful reference scope variables: `self`, `parent` and `children`. Self is just like the `self` of a class, it's a reference to the current component. Parent, as the name implies, is a reference to the `parent` component of the current component (or `None` for the root component). Children, is a list that contains a reference to all `children` components of the current component.


    :::python
    from enamlnative.widgets.api import *
    
    #: Define a component with the reference "view"
    enamldef ContentView(LinearLayout): view:
        attr text = "Hello!"
        
        #: Self reference example
        Button: 
          text = "add"
          clicked :: 
            #: Will print out "Button add clicked" when clicked
            print("Button {} clicked".format(self.text))
        
        #: Parent reference example
        TextView: 
          #: Use the reference `parent` to set the text to the `text` attribute
          #: Note: If a reference is not used in this case we would get a recursive loop!
          text << parent.text
          
        #: Children reference example
        TextView: 
          #: Use the reference `children` to print out the repr string of each
          #: direct child of the ContentView
          text = ",".join([c for c in parent.children])


References are used very often within enaml-native apps. The scope of each reference depends on where the component is but generally they're all availble for use (with some exceptions) within the entire enamldef block.  References of one component cannot be accessed outside of that components declaration (unless an `alias` keyword is used) but that will be covered later (look in the enaml docs for the examples). 

### Operators

One of the most powerful features of enaml is it's data binding operators. Enaml's data binding operators are what makes enaml much nicer than working with react or react-native in many cases.  The operators are `>>`, `<<`, `:=`, `::` and `=`.

#### Simple = operator

The `=` operator sets the inital state of the attribute. The attribute may later be changed by other components that interact with it.

#### Subscribe << operator

The `<<` operator a one way binding from a model to the UI component. This allows your UI to automatically update whenever a change occurs in your model and it automatically binds to changes in any atom objects used in the python expression. 


    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(LinearLayout):
        Switch: sw:
          checked = False
          
        TextView: tv:
          #: Use subscribe operator to update the label whenever the switch changes
          text << "Checked {}".format(sw.checked)

In the above example, whenever the user toggles the switch, the text updates to display the switches checked state. Enaml will see that `sw.checked` is an observable attribute and will update whenever it's changed. It can observe any number of attributes on the RHS, even those returned from functions, and will update when any of the observed attributes change!  

#### Update >> operator

The `>>` operator is a one way binding that notifies the component when the UI component updates the attribute. This allows your UI changes to then be properly handled (ex, updating your model). 

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(LinearLayout):
        Switch: sw1:
          checked = False
          checked >> sw2.checked
        Switch: sw2:
          checked = False
          
In this example, when switch `sw1` is toggled, switch `sw2` will also be set to the same state. However if switch `sw2` is toggled, switch `sw1` will not change. 

In some cases you might want to know what the previous value was before the change occured. You can use the `change` scope variable to see and react accordingly.   


    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(LinearLayout):
        EditText: et:
          text >> 
                #: When text changes
                try:
                    #: If an integer was typed, update the text
                    if int(change['value']):
                        tv.text = change['value']
                except ValueError:
                    pass
        TextView: tv:
          pass

The above example with update the TextView's text attribute if the user enters an integer into the EditText's input field. Using this operator, along with the `<<` operator is very useful for doing things like to and from conversion of a value based on a unit input.  

The `change` variable is a dictionary containing useful change information such as the current value `change["value"]`, the name that changed `change["name"]`, the type of change `change["type"]`, the the previous value `change["oldvalue"]`, and the object that was changed `change["object"]`.



#### Delegate := operator

The `:=` operator does a two way binding between the UI component and a model (or another components's) attribute. This allows you to easily keep two attributes in sync (ex, UI attribute and model attribute or two UI attributes).

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(LinearLayout):
        Switch: sw1:
          checked := sw2.checked
        Switch: sw2:
          checked = True

In this example, toggling either switch will cause the other to toggle as well. Both switches will always stay in sync even though only one is being applied.  Generally this operator will be used to bind to an attribute of a data model as shown below.

    :::python
    from atom.api import Atom, Bool
    from enamlnative.widgets.api import *
    
    class Model(Atom):
      enabled = Bool()
    
    enamldef ContentView(LinearLayout):
        attr model = Model()
        Switch:
          checked := model.enabled

In the above example our model's enabled state will be bound to the switch checked state. If either are changed they will both stay in sync.

#### Notify :: operator

The `::` operator notifies the component when an event occurs, such as a button click, and allows you to handle the event as needed.

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(LinearLayout):
        Button:
          clicked ::
              #: This block of code will execute when clicked
              print("Button was clicked!")

Above we see the notify operator triggers the _event handler_ directly within the component. Any python code (except for `yield` and `return` statments can be used within the handler block. 

> Note: Certain events may contain additional data that may be needed to decide how the event should be handled. When a key is pressed, or an action selected, it may be important to know which key.  Event data is passed into your handler block via the `change` scope variable.  The change dictionary keys depend on the type of event that occurred.

#### More about operators

There's a good talk by the developer of enaml [on youtube](https://www.youtube.com/watch?v=ycFEwz_hAxk&t=3s) where he describes the operators in more detail. 

If you're familiar with react or react-native programming, these operators eliminate the need for `setState`, the "flux" pattern, and other state containers such as `Redux`. Enaml and Atom handle all of the state and changes for you.  

If you're familiar with Android or iOS programming, this entirely eliminates the need to add listeners, callback functions, or use key value observers. Enaml and the native toolkit implementation(s) handles all of this seamlessly behind the scenes. See the more advanced documentation or the code for more details if you're interested.

### Dynamic Components

Often time's you'll want to be display a component only when a certain condition is met. Additionally it's common to have to repeat a component based on a list of items. Enaml has an extremely powerful dynamic component system that allows you to do this and more. 

#### Conditionals

The `Conditional` node does not have any display widget, but instead uses it's `condition` attribute to decide if it's children should be rendered or not. 


    :::python
    from enaml.core.api import Conditional
    from enamlnative.widgets.api import *
    
    enamldef ContentView(LinearLayout):
        Switch: sw:
            checked = False
        Conditional:
            condtion << sw.checked
            #: This will only be shown if the switch is turned on!
            TextView:
                text = "Show me!"
                
In the above example the TextView will be shown or hidden based on the checked state or the switch. The `Condtional` inserts into or removes it's children from the parent component based on the `condition` attribute.  This is very efficient as __only__ the components within the Condtional block need to be rerendered.  

> Note: The condition must be a boolean. If you're simply checking for exitance use `is not None` or wrap the expression in a `bool(expr)` call.
          
#### Loopers

The `Looper` node also does not have any display widget, but instead uses it's `iterable` attribute to to generate a component for each item within the iterable list. 


    :::python
    from enaml.core.api import Looper
    from enamlnative.widgets.api import *
    
    enamldef ContentView(LinearLayout):
        attr items = ["one", "two", "three"]
        Looper:
            iterable << items
            #: This node is repeated for each item and given
            #: the additional scope variables `loop_index` and `loop_item`
            TextView:
                text = "{}. {}".format(loop_index+1, loop_item)
        
                
In the above example three TextView components will be added to the ContentView the text being "1. one", "2. two", and "3. three" for each component respectively. Items within the loop arg given new variables `loop_item` and `loop_index` which are self explanitory. Enaml's `Looper` is also very efficient in that it will only create or destroy child components that have been changed and reuses those that have not. 

> Note: If you happen to need to loop over two or more lists you can use `attr` keywords to save references to the parent loop's item as needed. 

#### Blocks

The `Block` node is a component specific to enaml-native. It's useful if you want to be able to define default content of a component but then later be able to override it in a subcomponent if needed. 

    :::python
    from enamlnative.core.api import Block
    from enamlnative.widgets.api import *
    
    enamldef Card(CardView): card:
        attr header = "Header"
        attr footer = "Footer"
        #: Alias allows accessing the `content` reference outside
        #: this component
        alias content
        TextView:
            text << card.header
        Block: content:
            TextView:
                text = "Default content!"
        TextView:
            text << card.footer
        
    
    enamldef ContentView(LinearLayout):
        #: Use our card component
        Card:
            Block:
                block << parent.content
                #: This block's children replace referenced block's content!
                TextView:
                    text = "New card content!"

The block makes it easy to define "template" like components where you can easily override certain parts, maximizing code reusability. If you're familiar with templating languages like django's templates this is a similar concept.  

> Note: It's important to notice here that a Block without a `block` attribute set is a placeholder and a Block with the `block` attribute set overrides the placeholder's content.

### Layouts

There are several platform dependent layouts that can be used, however it's recommended to use `Flexbox` which supports both Android and iOS. 

If you're unfamiliar with flexbox, there great examples from Google's [flexbox-layout](https://github.com/google/flexbox-layout) for Android. 






More to come on layouts!

### Summary

That's the basics of enaml and enaml-native. With knowledge of all of these, you should be ready to start building your own apps!  If you have any questions create an issue or use post a question on stackoverflow to request help!

