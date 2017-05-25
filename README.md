# enaml-native
Build mobile apps in python using with enaml and widgets native to the platform.

The goal of this project is to be an alternative to using [kivy](https://kivy.org/) for building mobile apps with python. 

I made this because wanted to have a more "React Native" like environment that: 
1. Uses python 
2. Uses native widgets (Android / iOS)
3. Can be run from Android Studio / XCode (ie no bootstraps)
4. Uses enaml's models, and declarative and dynamic widget framework instead of kvlang

   
_Note: This is currently only works for Android and is very limited at the moment as it's very new._  (I've been working on this for less than a week).

## Thanks to ##
 
This project is built on top of several existing systems:
1. [Enaml](https://github.com/nucleic/enaml)
2. [python-for-android](https://github.com/kivy/python-for-android/)
3. [pybridge](https://github.com/joaoventura/pybridge)

_Note: I'm not affiliated with any of them but have contributed to all of these projects_

## How it works ##

1. An  toolkit for enaml was created that uses [pyjnius](https://github.com/kivy/pyjnius) to create native android widgets. (Eventually will use [pyobjus](https://github.com/kivy/pyobjus) for iOS )
2. A customized version of [pybridge](https://github.com/joaoventura/pybridge) is used that
    a. Unpacks python
    b. Loads python
    c. Provides an interface to commuicate between the two 
3. An enaml view  generates the native widgets and displays them using native API's
4. A customzied bootstrap for [python-for-android](https://github.com/kivy/python-for-android) is used to build python modules for each arch (x86 and armeab-v7a included) 


## Running ##

1. Clone the project
2. Open in Android Studio, install Android API 25, if it's not already included.
3. Copy prebuilt python modules from `src/main/python/<arch>/` to `src/main/assets/python` for the arch you want to run on
4. Run project in Android Studio

## Cross compiling ##

Any python modules with compiled components must be cross compiled for the specific platform. To make this easier a modifed version of  kivy's [python-for-android](https://github.com/kivy/python-for-android/) is included in this repo with a new bootstrap and support for Crystax's Python 2.7.10. 

1. Install the [Crystax NDK v10.3.2](https://www.crystax.net/en/download) (or latest)
2. Clone the project, install dependencies for python-for-android
3. Update `ARCH`, `SDK_DIR`, `NDK_DIR`, and packages as needed 
4. Run `make clean-python`
5. Run `make build-python` this will build the required python dependencies and copy the libs and python modules from `~/.local/share/python-for-android/dists/enaml-native/` to `src/main/libs/<arch>/` and `src/main/python/<arch>/` respectively
6. Remove any unused modules and shared libraries in `src/main/python/<arch>/`
7. Run in android studio


