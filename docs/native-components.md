### Native Components

This is a short introduction into how enaml-native takes the components you define in your view code to the native widget that actually draws on the screen on Android or iOS. After reading this you should be able to add your own "native components" that can be used within your enaml-native views.

All components in enaml-native boil down to a single or collection of actual native widgets. What we are actually using in enaml-native is a proxy to a native widget (well a proxy to a proxy to be exact). Our enaml code is "Declarative" meaning we are just describing explicitly how the components should be created, organized, and interact with eachother. The actual implementation is abstracted out leaving it to be done however necessary.  

Adding new native components can be extremely easy (ex [Icons](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/android/android_iconify.py)) or rather difficult (ex the [ViewPager](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/android/android_view_pager.py)) depending on the level of interaction required and the available methods. 

### Overview

To implement your own component you must:

1. Install the actual native components for your platform (via Gradle or CocaPods) or include the source(s) from your own libraries 
2. Create a `ToolkitObject` (or subclass) declaration for your component
3. (optional) Add the declaration to the `enamlnative.widgets.api` module
4. Create an `ProxyToolkitObject` (or subclass) implementation for your component
5. Add the implementation to the `FACTORIES` for your toolkit (`enamlnative.android.factoires` for Android or `enamlnative.ios.factories` for iOS)
6. Import and use your component in an enaml file!

> Note: If you've implemented widgets for enaml before in Qt, enaml-native is very similar. You can jump right to the [bridge](https://www.codelv.com/projects/enaml-native/docs/bridge) docs as that is the main difference between creating widgets in enaml using PyQt vs in enaml-native (android/ios).

### Declaration

By convention, the declaration is typically defined in the `enamlnative.widgets` package and included in the `enamlnative.widgets.api` module.

 A declaration consists of two parts, a `ToolkitObject` or "Declarative" component declaration and a `ProxyToolkitObject` abstract implementation declaration.
 
#### Component declaration

The component declaration must extend the `ToolkitObject`  (or more commonly a subclass of one) and define the attributes the component has, events it can trigger, and the api for updating the proxy implementation. 

Attributes define "declarative members" that can be used with enaml operators and therefore the component usage. 

Any atom member wrapped in the `d_` function is considered a declarative member and can be used within an `enamldef` block. Those not wrapped with `d_` can only be accessed on the right hand side of an expression like normal python objects. 

Declarations often extend an existing declaration and match the same inheritance structure of the native component (ex the `CheckBox` subclasses the `CompoundButton`, which subclasses the `TextView`, etc..). Typically you can fallback to `View` or `ViewGroup` if no other superclasses exist.  If your native component isn't a `View` (for example a [Toast](https://www.codelv.com/projects/enaml-native/docs/components#toast)) you should subclass the `ToolKitObject` directly.
 
__Example 1 - Members__

    :::python
    
    class ProgressBar(View):
        """ A simple control for displaying a ProgressBar.
        """
        #: Sets the current progress to the specified value.
        progress = d_(Int())
    
        #: Sets the current progress to the specified value.
        secondary_progress = d_(Int())

        #: Set the upper range of the progress bar max.
        max = d_(Int())
    
        #: Set the lower range of the progress bar
        min = d_(Int())
    
        #: A reference to the ProxyProgressBar object.
        proxy = Typed(ProxyProgressBar)
    
        # --------------------------------------------------------------------------
        # Observers
        # --------------------------------------------------------------------------
        @observe('progress', 'secondary_progress', 'max', 'min')
        def _update_proxy(self, change):
            """ An observer which sends the state change to the proxy.
            """
            # The superclass implementation is sufficient.
            super(ProgressBar, self)._update_proxy(change)

From [enamlnative.widgets.progress_bar](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/widgets/progress_bar.py)


Here the `ProgressBar` is extending the `View` declaration and adding the new declarative attributes `progress`, `secondary_progress`, `min`, and `max`. 

> Note: Attributes can be made read only (from the declaration) using `writable=False` or write only with `readable=False`. This is useful for events that should only be triggered by the proxy object.

#### Proxy declaration

The `proxy` is a reference to the proxy implementation of this component.  The proxy must know when to update it's state and what values to use.
 
 > Note: The proxy must also update the state of the declaration when events from the widget occur see the [implementation](#implementation)). 
 
The `_update_proxy` method tells enaml how to update the proxy component when one of the attributes changes (or an event is triggered from the declaration). This almost always calls the [default handler](https://github.com/nucleic/enaml/blob/master/enaml/widgets/toolkit_object.py#L241) which trys to invoke `set_<attr>(<value>)` if the proxy has implemented it. The `observe` decorator (from the atom framework) tells the object to invoke the update handler when any of the given attributes change.

The `proxy` must implement the `ProxyToolkitObject` declaration that comes along with each component declaration.  This is an abstract definition of the API that the proxy must implement and is typically simply a reference to the declaration and a few `set_<attr>(<value>)` or similar methods which will fulful the `_update_proxy` method's requirements.
 
__Example 2 - Proxy declaration__
 
    :::python
     class ProxyProgressBar(ProxyView):
         """ The abstract definition of a proxy ProgressBar object.
         """
         #: A reference to the Label declaration.
         declaration = ForwardTyped(lambda: ProgressBar)
     
         def set_progress(self, progress):
             raise NotImplementedError
     
         def set_secondary_progress(self, progress):
             raise NotImplementedError
     
         def set_max(self, value):
             raise NotImplementedError
     
         def set_min(self, value):
             raise NotImplementedError

At first it may seem overwhelming, but it's very intuitive. and extremely flexible. Hat's off to the developers of enaml here for a great job with the design here! 

### Implementation

The declared components must have implementations for a given platform or UI framework that actually does all the work (rendering, layout, animations, etc..) that the declaration requires. These are called "toolkits". 

In "normal" enaml, there is one toolkit (there was also wx toolkit but it was dropped), which is implemented with Qt and interfaced using PyQt or PySide. 

In enaml-native there are two tookits, one for Android (in [enamlnative.android](https://github.com/codelv/enaml-native/tree/master/src/enamlnative/android)), and one for iOS (in [enamlnative.ios](https://github.com/codelv/enaml-native/tree/master/src/enamlnative/ios)) each implemented with widgets specific to the OS and interfaced using an async [bridge](https://www.codelv.com/projects/enaml-native/docs/bridge)..  

> Note: The bridge is needed since previous implementations have proven that integrating python into the native UI eventloop is too slow (Facebook came to the same conclusion using javascript for react-native)    


This is where all the declaration is actually turned into a native widget. So lets get down to it.

#### Creating the implementation

An implementation typically extends the "superclass" implementation and the "proxy" declaration. It "wraps" the actual native component and implements the proxy interface and enaml lifecycle api as needed.

Let's look at an example.

__Example 3 - Uikit ProgressBar__

    :::python
    '''
    Copyright (c) 2017, Jairus Martin.
    Distributed under the terms of the MIT License.
    The full license is in the file COPYING.txt, distributed with this software.
    Created on Aug 3, 2017
    @author: jrm
    '''
    
    from atom.api import Typed, set_default
    from enamlnative.widgets.progress_bar import ProxyProgressBar
    
    from .bridge import ObjcMethod, ObjcProperty
    from .uikit_view import UIView, UiKitView
    
    class UIProgressView(UIView):
        """ From:
            https://developer.apple.com/documentation/uikit/uiview?language=objc
        """
        #: Properties
        progress = ObjcProperty('float')
        setProgress = ObjcMethod('float', dict(animated='bool'))
    
    
    class UiKitProgressView(UiKitView, ProxyProgressBar):
        """ An UiKit implementation of an Enaml ProxyToolkitObject.
        """
    
        #: A reference to the toolkit widget created by the proxy.
        widget = Typed(UIProgressView)
    
        # --------------------------------------------------------------------------
        # Initialization API
        # --------------------------------------------------------------------------
        def create_widget(self):
            """ Create the toolkit widget for the proxy object.
            """
            self.widget = UIProgressView()
    
        def init_widget(self):
            """ Initialize the state of the toolkit widget.
            This method is called during the top-down pass, just after the
            'create_widget()' method is called. This method should init the
            state of the widget. The child widgets will not yet be created.
            """
            super(UiKitProgressView, self).init_widget()
    
            d = self.declaration
            if d.progress:
                self.set_progress(d.progress)
    
        # --------------------------------------------------------------------------
        # ProxyProgressBar API
        # --------------------------------------------------------------------------
        def set_progress(self, progress):
            self.widget.progress = progress/100.0
            
            
        # etc..


Source [enamlnative/ios/uikit_progress_view.py](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/ios/uikit_progress_view.py)

First the `ProxyProgressBar` interface that must be implemented for our `ProgressBar` component to work is imported. 

Skip over the `UIProgressView` class definition for now, we'll get there shortly. 

Next, we define our `UiKitProgessView` which extends the `UiKitView` (a subclass of`ProxyToolKitObject`) and our `ProxyProgressBar` ensuring the interface methods are there.

Then the class defines the `widget = Typed(UIProgressView)` which is the holder for our "native" widget. After that we see the `create_widget` method, which (as you can guess) creates an instance of our native widget which is followed by `init_widget` which initializes the widget to all of the initial values declared in the enaml view. 

The `init_widget` reads all of the attributes declared and calls the correct `set_<attr>(<value>)` handler for each. Some implementations must do additional setup here such as defining an adapter for data models, and connecting up listeners.

Finally, we see the implementation of the `ProxyProgressBar` API methods  (ex `set_progress`) which here just updates a property of the native widget.

When implementing a new component, most of the time it's easiest to simply copy the most similar component and update it from there.


###### Bridge objects

Let's talk about the `UIProgressView` we skipped over earlier. 

Since enaml-native uses an async bridge instead of an actual direct wrapper that does it automatically (like PyQt) we must explicity define what that properties and methods that widget or object has so we can use them in python. 

> For more information see the [bridge](https://www.codelv.com/projects/enaml-native/docs/bridge) docs. 

We do it this way because it's several _orders of magnitude_ faster than using a reflection or cache based implementation that serializes back and forth on every call (and it also nicely works with code inspection!).

Once we define the methods and properties the actual native widget has, the bridge handles the rest, and we can use it just like a normal python object.

So when we do `self.widget = UIProgressView()` the bridge is actually creating the native [UIProgressView](https://developer.apple.com/documentation/uikit/uiprogressview) and then setting `self.widget.progress = progress/100.0` the bridge actually does that assignment on the real native object. Hence we have a "proxy" to the native object in python that allows us to do everything we need to implement our component declaration like it were in python.


##### Component lifecycle and changes

When implementing a component, it's important to understand the flow that the application goes through during creation of components and how to handle changes such as children being added or removed.

> Note: See [enaml/widgets/toolkit_object.py](https://github.com/nucleic/enaml/blob/master/enaml/widgets/toolkit_object.py) for more info on the API. enaml's code base has great documentation.


###### Creation

When `application.start()` is called, `intialize()` is called on each node to generate the tree and proxy implementations. After the tree is built, `activate_proxy()` (see [toolkit_object.py](https://github.com/nucleic/enaml/blob/master/enaml/widgets/toolkit_object.py#L201)) is called on the root "node" of the enaml declarative tree, which walks down the nodes and calls the `activate_top_down()` method of each declaration and proxy object in the tree (depth first traversal).  Then `activate_bottom_up()` is called on each proxy object the way back up.  

These methods are typically only reimplemented by the most basic Toolkit object of each toolkit. For enaml-native these are rewritten in is [AndroidToolKitObject](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/android/android_toolkit_object.py) and [ObjcToolKitObject](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/ios/uikit_toolkit_object.py). They simply call `create_widget()` and `init_widget()` in the top down pass, and call `init_layout()` in the bottom up pass (same as the Qt toolkit built into enaml).
 
So this means when creating and initializing the widget in `create_widget` and `init_widget` respectively, the parent widget should be created and initialized however no children yet will exist. Thus any APIs that require interaction with the children (such as adding them as a subview) can only be done in the `init_layout` bottom up pass because at this point all of the children should be properly initialized. After `init_layout` is called the component should be ready for display. 


###### Manipulation

There are three commonly used methods that may need overridden to handle changes to the tree, `child_added`, `child_removed`, and `child_moved`. As you can guess these are called when the event occurs and should be used by the proxy implementation to update the native widget accordingly.

> Note: See [enaml/core/object.py](https://github.com/nucleic/enaml/blob/master/enaml/core/object.py) for more documentation on the object API

###### Deletion
 
 A component and proxy should cleanup and delete all used native objects in the `destroy()` is method. 
 


 > Note: The best way to learn how to use these different lifecycle methods are to look at all of the existing components.
 

### Adding the factories

An implementation must be added to the `FACTORIES` for the given toolkit. This is in `enamlnative.<toolkit>.factories` and is simply a dictionary that defines a function which returns the class of the implementation to use for a given declaration..
 
The application uses this dictionary at runtime to resolve and import only the components needed. You can add or replace factories here as needed for any new or customized components you may need.


### Using new components

Once a new component has been added it can simply be imported and used like any other component!


This document will continue to improve. Please leave feedback on parts that may be missing or unclear.



