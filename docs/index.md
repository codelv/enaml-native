### Enaml-Native

Documentation for enaml-native. Use toolbar above to choose another page. 

### What is enaml-native?
The goal of enaml-native is to be the python version of [react-native](https://facebook.github.io/react-native/). To borrow react-native's tagline:
>  enaml-native lets you build mobile apps using only python. It uses the same design as enaml, letting you compose a rich mobile UI from declarative components.

It's a long way from being there but it's a start. It borrows many of the concepts used by react-native, such as using an async bridge and native widgets. Apps can be run and built in Android Studio or Xcode like you do with native apps. A simple `enaml-native` cli helps you create, build, and run projects. Android apps use the `gradle` build system, iOS apps use `xcode`. Python builds are done with modified versions of `python-for-android` for android and `kivy-ios`. 

### Why enaml?

This short video explains what enaml solves and why it's perfect for building UI's for mobile apps.

[![Enaml introduction](https://img.youtube.com/vi/ycFEwz_hAxk/0.jpg)](https://youtu.be/ycFEwz_hAxk)



### Apps are declarative

enaml-native apps are written declaratively using [enaml](http://nucleic.github.io/enaml/docs/get_started/introduction.html).  It's like JSX, just without `setState`, virtual doms, and view diffing.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        TextView:
            text = "Python powered native apps!"

### Use native libraries
You can use native libraries by making a simple wrapper for them.

    :::python
    #: Wrapper
    class LayoutParams(JavaBridgeObject):
        __nativeclass__ = set_default('android.view.ViewGroup$LayoutParams')
        width = JavaField('int')
        height = JavaField('int')

    #: Usage
    params = LayoutParams()
    params.width = 20


and using in python as any python normal object (see the [bridge](https://www.codelv.com/projects/enaml-native/docs/bridge) docs for more info).

