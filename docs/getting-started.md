### Quickstart

The easiest way to try out enaml-native is by downloading the [Python Playground](https://play.google.com/store/apps/details?id=com.frmdstryr.pythonplayground) app. This app allows you to paste code into a web based editor and run it as if it were built as part of the app!

[![Python Playground](https://img.youtube.com/vi/2IfRrqOWGPA/0.jpg)](https://youtu.be/2IfRrqOWGPA)


Continue on below to install the dependencies for required building your own enaml-native apps.


### Installing

enaml-native uses the same toolchains as kivy, so the same dependencies must be installed. Currently only python 2.7 is supported (same as kivy-ios).

### Overview
1. Install the [system](#system-dependencies) dependencies
2. Install the [app](#app-dependencies) SDKs and tools (Android and/or iOS dependencies)
3. Install [enaml-native](#installing-enaml-native)
4. Create a [new project](#creating-and-run-a-new-project)


Instructions for each are below. Please feel free to suggest changes or ask for help if you run into issues.

### System dependencies

The toolchain supports ubuntu and osx. Install as necessary for your system.

##### Ubuntu

Install the following dependencies

    :::sh
    #: Install python-for-android dependencies
    #: See https://python-for-android.readthedocs.io/en/latest/quickstart/
    sudo dpkg --add-architecture i386
    sudo apt update
    sudo apt install -y build-essential ccache git zlib1g-dev python2.7 python2.7-dev libncurses5:i386 libstdc++6:i386 zlib1g:i386 unzip ant ccache autoconf libtool

    #: Install java
    sudo apt install openjdk-7-jdk
    #: or actual java (preferred)
    #: see http://www.webupd8.org/2012/09/install-oracle-java-8-in-ubuntu-via-ppa.html
    sudo add-apt-repository ppa:webupd8team/java
    sudo apt update
    sudo apt install oracle-java8-installer
    sudo apt install oracle-java8-set-default


#### OSX

Install the following dependencies

    :::sh
    #: Install brew see https://brew.sh/
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

    #: Install system dependencies
    brew install python autoconf automake libtool pkg-config
    brew link libtool



### App dependencies

#### Android (Ubuntu or osx)

To build android apps, the android SDK and crystax NDK must be installed.

##### Android SDK

1. Download [android studio](https://developer.android.com/studio/index.html)
2. Once done, open it and go to `Tools->Android->SDK Manager` from the menu
3. Under the `SDK Platforms` tab, select `Android 7.1.1` (or latest)
4. and under the `SDK Tools` tab, select `Android SDK Build-Tools 26` (or latest), `Android Emulator`, `Android SDK Platform-Tools`, and `Android SDK Tools` (they should be selected by default)
5. Now click apply and let everything download (takes a LONG time)

##### Crystax NDK

1. Go to [crystax.net](https://www.crystax.net/) and click on `Downloads`
2. Download crystax 10.3.2 [for linux](https://www.crystax.net/download/crystax-ndk-10.3.2-linux-x86_64.tar.xz) or [for osx](https://www.crystax.net/download/crystax-ndk-10.3.2-darwin-x86_64.tar.xz)
3. Once downloaded, extract it to `~/Android/crystax-ndk/` on linux or `~/Library/Android/crystax-ndk/` on osx

#### iOS (OSX only)

1. Install `xcode` from the App Store


### Installing enaml-native

You can now use the [enaml-native-cli](https://github.com/codelv/enaml-native-cli) instead of
installing from source. Simply use:

  
    :::sh
    pip install --user enaml-native-cli
    

Which installs all the python requirements for you.

If pip does not work, use `sudo apt install python-pip` on ubuntu or `brew install python` on osx
 

### Create and run a new project

To create a new project use the cli to init a new project.

    :::bash
    
    # Format enaml-native init <ProjectName> <bundleId> <Destination>
    enaml-native init HelloWorld com.example.helloworld apps/


Now cd to the destination folder, activate the virtual env, and build the python and ndk libraries.

    :::bash
    
    #: Go into project folder
    cd apps/HelloWorld
    
    #: Activate the venv
    source venv/bin/activate
    
    #: Build python and ndk libraries
    enaml-native build-python 


Next, on android, we have to do a gradle sync by building the android project. 

    :::bash
    enaml-native build-android 


We must install the native python libraries and modules by running build python again.

    :::bash
    
    enaml-native build-python 


Now either start the emulator or plug in a phone and we can run with
 
    :::bash
     
    enaml-native run-android 
 

Your app's code resides in the `src` directory. Any files here get installed on the app.

The `view.enaml` contains the UI that is shown, and `main.py` is the startup script. 

Next [learn the basics](https://www.codelv.com/projects/enaml-native/docs/learn-the-basics)

> Note: iOS support is not yet fully implemented.