# enaml-native
Build mobile apps in python using enaml and widgets native to the platform.

[demo](https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-startup-speed-test.gif)

Video here: [on youtube](https://youtu.be/cEYmyObl17A)

<div>
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app.png" width="240" style="float: left;">
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-2.png" width="240" style="float: left;">
<img src="https://raw.githubusercontent.com/frmdstryr/enaml-native/master/docs/imgs/enaml-native-android-app-3.png" width="240" style="float: left;"></div>

The goal of this project is to be an alternative to using [kivy](https://kivy.org/) for building mobile apps with python. 

I made this because wanted to have a more "React Native" like environment that: 
1. Uses python 
2. Uses native widgets (Android / iOS)
3. Can be run from Android Studio / XCode (ie no bootstraps)
4. Uses enaml's models, and declarative and dynamic widget framework instead of kvlang

   
_Note: This is currently only works for Android and is very limited at the moment as it's very new. I've been working on this for less than a week_

## Thanks to ##
 
This project is built on top of several existing projects:
1. [Enaml](https://github.com/nucleic/enaml)
2. [python-for-android](https://github.com/kivy/python-for-android/)
3. [pybridge](https://github.com/joaoventura/pybridge)

_Note: I'm not affiliated with any of these but have contributed to some of them_

## How it works ##

1. An  toolkit for enaml was created that uses [pyjnius](https://github.com/kivy/pyjnius) to create native android widgets. (Eventually will use [pyobjus](https://github.com/kivy/pyobjus) for iOS )
2. A slightly customized version of [pybridge](https://github.com/joaoventura/pybridge) is used that
    unpacks python assets, starts the python interpreter, and provides an interface to commuicate between the two 
3. An enaml view  generates the native widgets and displays them using native API's
4. A customzied bootstrap for [python-for-android](https://github.com/kivy/python-for-android) is used to build python modules for each arch (x86 and armeab-v7a included) 



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


### Issues ###

A lot of the same issues as `Kivy` are here. Since it's packaging and must load python.

###### Large Apk / App size ######
Apk size are probably going to be at least 8 MB (when packaged for one arch).  Installed size will be around 30 MB.

After removing unused libraries the installed size is about ~24 MB.

###### Slow startup times ######

~~Startup times are (now less) SLOW. The loading splash comes immediately but on a nexus 5, it takes ~~about 20~~ 13 seconds for python to start and render the UI. This is a killer at the moment...~~

Now loading now takes ~~about 3 seconds. I think even more improvements can be made.~~ about 2 seconds!    

But this seems to be a reasonable loading time. 

Profiling results:
 
 ```
 
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:          141961 function calls (140210 primitive calls) in 3.379 seconds
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:    Ordered by: cumulative time
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:        33    0.001    0.000    1.820    0.055 /data/user/0/com.jventura.pyapp/assets/python/site-packages/jnius/reflect.py:153(autoclass)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:        28    0.002    0.000    1.819    0.065 /data/user/0/com.jventura.pyapp/assets/python/site-packages/jnius/reflect.py:420(cached_autoclass)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         1    0.001    0.001    1.269    1.269 /data/user/0/com.jventura.pyapp/assets/python/enamlnative/android/app.py:10(<module>)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         1    0.000    0.000    1.226    1.226 /data/user/0/com.jventura.pyapp/assets/python/stdlib.zip/json/__init__.py:257(load)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         2    0.000    0.000    1.197    0.598 /data/user/0/com.jventura.pyapp/assets/python/stdlib.zip/json/__init__.py:293(loads)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         2    0.000    0.000    1.197    0.598 /data/user/0/com.jventura.pyapp/assets/python/stdlib.zip/json/decoder.py:361(decode)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         2    1.197    0.598    1.197    0.598 /data/user/0/com.jventura.pyapp/assets/python/stdlib.zip/json/decoder.py:372(raw_decode)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         1    0.000    0.000    1.020    1.020 /data/user/0/com.jventura.pyapp/assets/python/bootstrap.py:22(router)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         1    0.000    0.000    1.020    1.020 /data/user/0/com.jventura.pyapp/assets/python/bootstrap.py:33(handle)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         1    0.000    0.000    1.020    1.020 /data/user/0/com.jventura.pyapp/assets/python/bootstrap.py:100(start)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         1    0.008    0.008    1.020    1.020 /data/user/0/com.jventura.pyapp/assets/python/enamlnative/android/app.py:51(start)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:         1    0.000    0.000    1.012    1.012 /data/user/0/com.jventura.pyapp/assets/python/enamlnative/android/app.py:60(get_view)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:        28    0.056    0.002    0.590    0.021 /data/user/0/com.jventura.pyapp/assets/python/site-packages/jnius/reflect.py:369(load_spec)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:      26/1    0.001    0.000    0.577    0.577 /data/user/0/com.jventura.pyapp/assets/python/site-packages/enaml/widgets/toolkit_object.py:147(initialize)
05-27 01:54:35.779 19891-19891/com.jventura.pyapp I/pybridge:        26    0.001    0.000    0.574    0.022 /data/user/0/com.jventura.pyapp/assets/python/site-packages/enaml/application.py:351(create_proxy)
 
 
 ```
 Notes: 
  -  jnius.reflect is taking 10s of this.  Now a static loading method for JavaClasses is used, reducing this by a factor of 10 !!
  -  Enaml can load quickly when cache files are properly included.



## iOS ##

Will come if the Android version works well...