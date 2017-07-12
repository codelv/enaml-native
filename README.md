# enaml-native
Build mobile apps in python using enaml and widgets native to the platform.


Latest video here [on youtube](https://youtu.be/4bm5fb5k5mc)

Try out the beta demo app here [on google play](https://play.google.com/apps/testing/com.frmdstryr.enamlnative.demo)


<div>
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-1.png" width="240" style="float: left;">
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-2.png" width="240" style="float: left;">
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-3.png" width="240" style="float: left;">
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-4.png" width="240" style="float: left;">
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-5.png" width="240" style="float: left;">
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-6.png" width="240" style="float: left;">
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-7.png" width="240" style="float: left;">
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-8.png" width="240" style="float: left;">
</div>

The goal of this project is to be an alternative to using [kivy](https://kivy.org/) for building mobile apps with python. 

I made this because wanted to have a more "React Native" like environment that: 
1. Uses python 
2. Uses native widgets (Android / iOS)
3. Can be run from Android Studio / XCode (ie no bootstraps)
4. Uses enaml's models, and declarative and dynamic widget framework instead of kvlang

   
### Features ###

1. Conditional and Looper based rendering
2. Data binding
3. Declarative syntax


## Thanks to ##
 
This project is built on top of several existing projects:
1. [Enaml](https://github.com/nucleic/enaml)
2. [python-for-android](https://github.com/kivy/python-for-android/)
3. [pybridge](https://github.com/joaoventura/pybridge)
4. [react-native](https://github.com/facebook/react-native) (inspiration)
5. [pyjnius](https://github.com/kivy/pyjnius/)

_Note: I'm not affiliated with any of these but have contributed to some of them_

## Usage ##

1. Create a `main.py` with a function called `main`
2. Declare and import an enaml view using widgets from the Android toolkit.
3. Create an instance of AndroidApplication 
3. Set the application view
3. Call `app.start()`

## How it works ##

1. A slightly customized version of [pybridge](https://github.com/joaoventura/pybridge) is used that unpacks python assets, starts the python interpreter, and provides an interface to commuicate between the two 
2. An enaml view  generates the native widgets and displays them using native API's
3. Python and Java commuicate using the bridge.


### Startup ###

When the app is started:
1. A loading view is shown (can be customized to be any view)
2. The python assets are extracted (if needed)
3. Python is started in a thread and the `main` function from `main.py` is called
4. An AndroidAppliction is started that runs an event loop (can use either the builtin, tornado, or twisted) 
5. The enaml view is constructed, loaded, and shown
6. The Bridge sends and handles all events


### The Bridge ###

Using pyjnius and the JNI was extremely slow, so pyjnius was replaced with a "java - python bridge" that allows you to create proxy python objects that are actually implemented in java. The bridge essentially queues all object creation and manipulation commands, serializes them using msgpack, and sends them over to Java (currently using JNI, may eventually use sockets). Java then unpacks and processes each command using reflection (currently...) and the Proxy interface. Any callbacks and Java widget events are queued, packed, and dispatched back over the bridge to be procssed by the python event loop. The result is a smooth interaction with minimal JNI use (only passes a msgpack byte arrays).

More documentation on how to use the bridge will come soon. 


### Original implementation ###
Note: This is no longer used.
A toolkit for enaml was created that uses [pyjnius](https://github.com/kivy/pyjnius) to create native android widgets. (Eventually will use [pyobjus](https://github.com/kivy/pyobjus) for iOS )


### Python libraries ###
You can use any pure python modules and any moodule with compiled objects as long as it has a `recipe` to build it. A customzied bootstrap for [python-for-android](https://github.com/kivy/python-for-android) is used to build python modules for each arch (x86 and armeab-v7a included) using the Crystax NDK. 

I'm thinking of making an easier way of doing this similar to node_modules.


## Android ##

### Running ###

1. Clone the project
2. Open in Android Studio, install Android API 25, if it's not already included.
3. Copy prebuilt python modules from `src/main/python/<arch>/` to `src/main/assets/python` for the arch you want to run on
4. Run project in Android Studio


### Cross compiling ###

Any python modules with compiled components must be cross compiled for the specific platform. To make this easier a modifed version of  kivy's [python-for-android](https://github.com/kivy/python-for-android/) is included in this repo with a new bootstrap and support for Crystax's Python 2.7.10. 

1. Install the [Crystax NDK v10.3.2](https://www.crystax.net/en/download) (or latest)
2. Clone the project, install dependencies for python-for-android
3. Edit the makefile and update `ARCH`, `SDK_DIR`, `NDK_DIR`, and packages as needed 
4. Run `make clean-python`
5. Run `make build-python` this will build the required python dependencies and copy the libs and python modules from `~/.local/share/python-for-android/dists/enaml-native/` to `src/main/libs/<arch>/` and `src/main/python/<arch>/` respectively
6. Remove any unused modules and shared libraries in `src/main/python/<arch>/`



## iOS ##

Will come if the Android version works well...
