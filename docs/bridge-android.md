### Bridge - (Java - Python) 

The bridge is an async way of communicating between python and java. It's based partially on this talk [Alexander Kotliarskyi - React Native: Under the Hood | YGLF2015](https://youtu.be/hDviGU-57lU).  Using an async bridge keeps the _slowness_ of python and the JNI from blocking the UI. It is essentially a python-java  rpc interface that allows python to create, update, and delete Java objects and listen to events and results those objects create. Instead of using JSON (like react-native) it uses msgpack, since msgpack is [significantly faster](https://gist.github.com/schlamar/3134391) in python.

This uses a different approach than pyjnius which creates all of these fields for you automatically via reflection. The tradeoff here is speed. Even when you cache and recreate `jnius` classes it is still significantly slower in object creation and method calling than the bridge approach used here (we're talking several orders of magnitude slower). The bridge was designed to have as little overhead as possible. All bridge objects are implemented using the `Atom` framework's `Properties` which is implemented in c++ and has minimal memory overhead.


The bridge is implemented in two files:
1. [com.enaml.Bridge](https://github.com/frmdstryr/enaml-native/blob/master/android/app/src/main/java/com/enaml/Bridge.java) in Java
2. [enamlnative.android.bridge](https://github.com/frmdstryr/enaml-native/blob/master/src/enamlnative/android/bridge.py) in Python 

### Usage

In python, define a subclass of `JavaBridgeObject` and declare the JavaMethods, JavaFields, and JavaCallbacks you need. For example:

__Example 1 - Defining Java objects using the bridge__
    
    :::python

    class ArrayAdapter(JavaBridgeObject):
        __nativeclass__ = set_default('android.widget.ArrayAdapter')
        __signature__ = set_default(('android.content.Context', 'android.R'))
        add = JavaMethod('java.lang.Object')
        addAll = JavaMethod('[Ljava.lang.Object;')
        remove = JavaMethod('java.lang.Object')
        clear = JavaMethod()



From this you see we set the `__nativeclass__` property to the java class name this object is creating.  

Next we define the `__signature__` which is a tuple that defines the constructors used. Multiple signatures are not supported (as of now).  If you want multiple signatures, either override `__init__` to handle each, or just make a subclass for each constructor.

Then we define multiple `JavaMethod` properties that specify the name, type of arguments, and return type. You then just use them like you would a normal python class.

__Example 2 - Using bridge objects__
    
    :::python

    #: We can do a little magic for the style property
    self.adapter = ArrayAdapter(self.get_context(), '@layout/simple_spinner_dropdown_item')

    #...
    self.adapter.clear()
    self.adapter.addAll(items)


We'll cover how these calls are then serialized and handled in the next section. But first, let's cover a few more basics. 

A field is similarly defined using `JavaField` and passing the field type. 

__Example 3 - Setting fields__
    
    :::python

    class LayoutParams(JavaBridgeObject):
        __nativeclass__ = set_default('android.view.ViewGroup$LayoutParams')
        width = JavaField('int')
        height = JavaField('int')
        LAYOUTS = {
            'fill_parent': -1,
            'match_parent': -1,
            'wrap_content': -2
        }

Also, these are just python objects, so you can define attributes as however needed.

__Example 4 - Subclassing bridge objects__
    
    :::python
    class MarginLayoutParams(LayoutParams):
        __nativeclass__ = set_default('android.view.ViewGroup$MarginLayoutParams')
        __signature__ = set_default(('int', 'int'))
        setMargins = JavaMethod('int', 'int', 'int', 'int')
        setLayoutDirection = JavaMethod('int')


    class LinearLayoutLayoutParams(MarginLayoutParams):
        __nativeclass__ = set_default('android.widget.LinearLayout$LayoutParams')
        gravity = JavaField('int')
        weight = JavaField('int')


Like python classes, you can extend other `JavaBridgeObject` instances and it will inherit all the methods, field, callbacks, etc, reducing the work you need to do. 


__Example 5 - Defining Java Callbacks__

    :::python

    class RatingBar(ProgressBar):
        __nativeclass__ = set_default('android.widget.RatingBar')
        setIsIndicator = JavaMethod('boolean')
        setMax = JavaMethod('int')
        setNumStars = JavaMethod('int')
        setOnRatingBarChangeListener = JavaMethod('android.widget.RatingBar$OnRatingBarChangeListener')
        setRating = JavaMethod('float')
        setStepSize = JavaMethod('float')
        onRatingChanged = JavaCallback('android.widget.RatingBar', 'float', 'boolean')



Callbacks are defined using the `JavaCallback` property. You pass the types of parameters method receives.  Then you can `connect` the callback to a handler as you would in PyQt or PySide.

__Example 6 - Connecting Java Callbacks__

    :::python

    self.widget = RatingBar(self.get_context())

    #: ...
    #: Setup listener
    self.widget.setOnRatingBarChangeListener(self.widget.getId())
    self.widget.onRatingChanged.connect(self.on_rating_changed)


    # --------------------------------------------------------------------------
    # OnRatingBarChangeListener API
    # --------------------------------------------------------------------------

    def on_rating_changed(self, bar, rating, user):
        d = self.declaration
        with self.widget.setRating.suppressed():
            d.rating = rating



In this we see how you create the widget, set the listener to the id of the widget we created (will explain later), and then connect the callback to our handler `on_rating_changed`.  The callback must accept the arguments passed from Java (you can also just use `*args`). All primitive types will be passed to the handler as is  (ex, 'int', 'bool', etc..) anything else will be passed using a `reference`. More on references later.

This is doing some magic which I'll explain later (ex. the widget doesn't actually implement that interface!) , but for now just remember, define the listener or `JavaCallback` properties, set your listener to the id of the listening widget, and connect the callbacks to handlers you're interested in (unconnected handlers will do nothing).

__Example 7 - Defining return values__
    
    :::python

    class TabLayout(FrameLayout):
        __nativeclass__ = set_default('android.support.design.widget.TabLayout')
        addTab = JavaMethod('android.support.design.widget.TabLayout$Tab')
        newTab = JavaMethod(returns='android.support.design.widget.TabLayout$Tab')
        #: etc..


Up until now this was all fairly simple and looks like normal `synchronous` python code. However, when we need to get return values from methods, or return values in callbacks, things become a little more tricky. Due to the fact that the bridge is asynchronous and batched together, results are returned as `Futures` that are implemented using whichever event loop you choose (twisted or tornado at the moment).

To tell the bridge we expect a return value from this method, you pass the `returns` argument along with the return type to the `JavaMethod` or `JavaCallback` constructor.  This tells the bridge that the result needs sent back over the bridge (from either side).   

When using a return with a `JavaCallback`,  you simply return the value in your handler and the bridge will do the rest (assuming the python bridge can properly encode it). 

__Example 8 - Handling return values__
    
    :::python
    from enamlnative.android.app import AndroidApplication
    #...
    app = AndroidApplication.instance()
    for page in pages:
        result = self.widget.newTab()
        result.then(lambda tab,page=page: self.on_new_tab(tab,page))

_Note: This API may change in the future._

With `JavaMethod` returns values, as in the above example, the `TabLayout.newTab` method returns a newly created tab (Tabs have no public constructors).  This value is returned `asynchronously`, what you actually get a is a `Future` object that will complete when the value is returned from Java. To do something when it is complete you have to add a callback on the future when it is done. You can have the app instance do this for you, by calling `app.add_done_callback(future,callback)`. Or you can decorate your function (ex. `@inlineCallbacks` with twisted) and use the `yield` statement.

__Example 9 - Creating references__
    
    :::python

    def on_new_tab(self, tab, page):
        tab = Tab(__id__=tab)
        d = page
        if d.title:
            tab.setText(d.title)

As mentioned earlier, primitive data types (those that can be packed with msgpack) such as int, boolean, long, string, etc.. are sent directly in callbacks and results. Objects, such as view or references (the Tab in the example above) are passed via a `reference`. The reference is simply an integer that can be _casted_ to the object in python by passing the `__id__` keyword argument when constructing a `JavaBridgeObject`. Once this is done, all of the method calls on that object will properly be sent to the correct object as if it were created in python.

__Example 10 - Update now__
    
    :::python

    self.widget.showLoading("Reloading....",now=True)

If you're about do do something that will take some time (loading a file, etc..) and you want to have the UI display an update before this happens, you can force the bridge to process events right away by passing the `now=True` keyword argument during a method call. This will tell the bridge to send out any pending events before returning.


That's about it (for now). There's plenty of examples in the `enamlnative.android` package of how to use the bridge for you to look at. Feel free to create an issue with questions.


***


### Details

The bridge works by serializing every creation, method call, and deletion, into a msgpack message which java then handles using reflection (currently).  You can set `app.debug = True` to see all the messages being sent back and forth.  

__Example 1 - Bridge serialization__
    
    07-17 17:27:19.047 11491-11522/com.frmdstryr.enamlnative.demo I/pybridge: ======== Py --> Java ======
    07-17 17:27:19.048 11491-11522/com.frmdstryr.enamlnative.demo I/pybridge: ('c', (1, u'android.widget.LinearLayout', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-17 17:27:19.048 11491-11522/com.frmdstryr.enamlnative.demo I/pybridge: ('m', (1, 0, 'setOrientation', [('int', 1)]))
    07-17 17:27:19.048 11491-11522/com.frmdstryr.enamlnative.demo I/pybridge: ('c', (2, u'android.support.v7.widget.Toolbar', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-17 17:27:19.048 11491-11522/com.frmdstryr.enamlnative.demo I/pybridge: ('m', (2, 0, 'setBackgroundColor', [('android.graphics.Color', u'#004981')]))
    07-17 17:27:19.048 11491-11522/com.frmdstryr.enamlnative.demo I/pybridge: ('m', (2, 0, 'setTitle', [('java.lang.CharSequence', u'Enaml Native - Intro')]))
    07-17 17:27:19.048 11491-11522/com.frmdstryr.enamlnative.demo I/pybridge: ('m', (2, 0, 'setTitleTextColor', [('android.graphics.Color', u'#FFFFFF')]))
    07-17 17:27:19.048 11491-11522/com.frmdstryr.enamlnative.demo I/pybridge: ('m', (2, 0, 'setSubtitleTextColor', [('android.graphics.Color', u'#EEEEEE')]))
    07-17 17:27:19.048 11491-11522/com.frmdstryr.enamlnative.demo I/pybridge: ('m', (1, 0, 'addView', [('android.view.View', ExtType(code=1, data='\x02'))]))

The above is a small section of the log from the demo app. 

The message format depends on the command, the basic format is :

    :::python
    [
    ('<command>',(<args...>)),
    ('<command 2>',(<args 2...>)),
    #: etc...
    ]

These commands then get processed by `processEvents` in `Bridge.java` which maps to either do a creation, update, or deletion of the given object (and a few others). The objects are stored using a given id in a cache and deleted when the python object get's gc'd. This id is passed back as the reference id in callbacks.

### Serialization and conversion
There's a few things you need to know about how conversion occurs when passing back and forth across the bridge:

1. First, primitives are sent directly, strings, ints, bools, etc.. 
2. Any JavaBridgeObject is passed using a msgpack extension type and dereferenced by java
3. Some tricks are used to minimize object creation in python and support things like implementing interfaces

In java, the method invoke commands are mapped to reflection calls that must match a given signature. The unpacker does a few things to make this easy. Look at the `unpackValue` method in `Bridge.java` (it's pretty simple).

1. Passing an `int` for a method argument that is an interface will create a `Proxy` implementation of that interface using the `int` as a reference object to return invocations to. This is how the `JavaCallback` works.
2. Passing a `JavaBridgeObject` will get mapped to the `object with that id` from the cache. 
3. Defining a signature that takes the an `android.graphics.Color` and passing a string argument 

    ::python
    backgroundColor = JavaMethod('android.graphics.Color')

will get mapped to `backgroundColor(int color)` where the color is created using `Color.parseColor(arg)`.

4. Defining a signature that takes an `android.R` will get parsed as an android resources string and converted as needed. (ex. `@layout/simple_spinner_dropdown_item` is mapped to `R.layout.simple_spinner_dropwdown_item`)



That's all for now! Cheers!




