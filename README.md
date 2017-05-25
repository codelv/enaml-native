# enaml-native
Build mobile apps in python using with enaml and widgets native to the platform.


## How ##

1. An  toolkit for enaml was created using [pyjnius](https://github.com/kivy/pyjnius) and native android widgets
2. An enaml view  generates the android widgets and displays them using native Android API's
3. A customzied bootstrap for [python-for-android](https://github.com/kivy/python-for-android) is used to build python modules for each arch (x86 and armeab-v7a included)
4. A customized version of [pybridge](https://github.com/joaoventura/pybridge) starts everything


## Setup ##

1. Clone the project
2. Open in Android Studio
3. Copy prebuilt python modules from `src/main/python/<arch>/` to `src/main/assets/python` for the arch you want to run on
4. Run project in Android Studio

## Building python modules ##
1. Install the [Crystax NDK v10.3.2](https://www.crystax.net/en/download) (or latest)
2. Clone the project, install dependencies for python-for-android
3. Run `make clean-python`
4. Run `make build-python`
5. Copy libs from  `~/.local/share/python-for-android/dists/enaml-native/libs` to  `src/main/libs/<arch>/`
6. Copy `modules` and `site-packages` from  `~/.local/share/python-for-android/dists/enaml-native/python` to  `src/main/python/<arch>/`