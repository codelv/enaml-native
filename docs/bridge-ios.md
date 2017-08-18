### Bridge (Python - Objective C)
> Note: This has not yet been implemented and is simply a declaration or spec of how I intend to make it. I'm not an expert in iOS or Obj-C development. This is based on the little information I know. 

Please see the [Bridge (Android)](../bridge-android) page for a description on what the Bridge does and why it's needed. 

The iOS bridge implementation uses the CPython API for invoking python from Obj-C (ie callbacks) and uses ffi for invoking the required bridge methods.  It is designed to look and be used more like Swift than Obj-C. 


### Usage
In python, define a subclass of `ObjcBridgeObject` and declare the ObjcMethods, ObjcProperties, and ObjcCallbacks you need.

__Example 1 - Defining Obj-C objects using the bridge__

    :::python

    class UIButton(ObjcBridgeObject):
        __nativeclass__ = set_default('UIButton')
        __signature__ = set_default(dict(buttonWithType='UIButtonType))
        setTitle = ObjcMethod('NSString', dict(forState='UIControlState'))
        addTarget = ObjcMethod('NSObject', dict(action='@selector'))
        frame = ObjcProperty('TODO:...')
        onClick = ObjcCallback()


Bridge objects are used to define how the bridge should pack and unpack the values over the bridge. Methods are defined like they are in Obj-C just instead of parameters adding to the method name `setTitle_forName` we're using the keyword arguments to do this behind the scenes.  


__Example 2 - Using Obj-C bridge objects__
    :::python

    button = UIButton(buttonWithType=UIKit.UIButtonTypeRoundedRect)
    button.setTitle("Click me", forState=UIKit.ControlStateNormal)
    button.frame = CGRectMake(15, 50, 300, 500)
    #...

There's a few things to note here. 

First, it does not use the Obj-C like syntax that many other python/obj-c implementations do (pyobjc, pyobjus). It's more like Swift and it's more pythonic. 

More to come (lets see if I can implement what's above first)!
