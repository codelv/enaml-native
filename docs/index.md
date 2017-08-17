# Enaml-Native

Documentation for enaml-native. Use the menu on the right. 

## What is enaml-native?
The goal of enaml-native is to be the python version of [react-native](https://facebook.github.io/react-native/). To borrow react-native's tagline:
>  enaml-native lets you build mobile apps using only python. It uses the same design as enaml, letting you compose a rich mobile UI from declarative components.

It's a long way from being there but it's a start. It borrows many of the concepts used by react-native, such as using an async bridge and native widgets. Apps can be run and built in Android Studio or Xcode like you do with native apps. A simple `enaml-native` cli helps you create, build, and run projects. Android apps use the `gradle` build system, iOS apps use `xcode`. Python builds are done with modified versions of `python-for-android` for android and `kivy-ios`. 


### Apps are declarative

enaml-native apps are written declaratively using [enaml](http://nucleic.github.io/enaml/docs/get_started/introduction.html).  It's like JSX, just without `setState`, virtual doms, and view diffing.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(LinearLayout):
        TextView:
            text = "Python powered native apps!"

### Use native libraries
You can use native libraries by making a simple wrapper for them.

    :::python
    #: Wrapper
    class LayoutParams(JavaBridgeObject):
        __javaclass__ = set_default('android.view.ViewGroup$LayoutParams')
        width = JavaField('int')
        height = JavaField('int')

    #: Usage
    params = LayoutParams()
    params.width = 20


and using in python as any python normal object (see the [bridge](https://github.com/frmdstryr/enaml-native/wiki/Bridge) docs for more info).

