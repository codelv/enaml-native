### Quickstart

The easiest way to try out enaml-native is by downloading the [Python Playground](https://play.google.com/store/apps/details?id=com.frmdstryr.pythonplayground) app. This app allows you to paste code into a web based editor and run it as if it were built as part of the app!

[![Python Playground](https://img.youtube.com/vi/2IfRrqOWGPA/0.jpg)](https://youtu.be/2IfRrqOWGPA)


Continue on below to install the dependencies for required building your own enaml-native apps.


### Installing

enaml-native uses the same toolchains as kivy, so the same dependencies must be installed. Currently only python 2.7 is supported (same as kivy-ios).

### Overview
1. Install the [system](#system-dependencies) dependencies
2. Install the [python](#python-dependencies) requirements
3. Install the [app](#app-dependencies) SDKs and tools (Android and/or iOS dependencies)
4. Install [enaml-native](#installing-enaml-native)
5. [Run](#running) an enaml-native project
6. Create a [new project](#creating-a-new-project)
7. Use the [dev server](#using-dev-server) for live reloading of code


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


### Python dependencies

Now install the python dependencies


    pip install atom
    pip install appdirs
    pip install colorama>=0.3.3
    pip install cython
    pip install sh>=1.10,<1.12.5
    pip install jinja2
    pip install six


If pip does not work, use `sudo apt install python-pip` on ubuntu or `brew install python` on osx

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

Now finally, we can install enaml-native

1. Clone this repo using `git clone https://github.com/codelv/enaml-native`

### Running

1. Go to the to the enaml-native project folder
2. Open `package.json` and update the `sdk` and `ndk` paths as needed (android only)
2. Run `./enaml-native build-python`
3. Now open the `android` folder in android and press play or run `./enaml-native run-android`  or open `App.xcodeproj` under the `ios` folder with xcode and press play or run `./enaml-native run-ios`
4. Hopefully it works! If not please submit an issue.


### Create a new project

Finally, you can create your own project.

1. Change to the cloned enaml-native project folder (or any enaml-native project)
2. Run `./enaml-native init <ProjectName> <bundleId> <Destination>`
3. Change to the destination folder
4. Modify your app code in `src`
5. Run the project as shown in [running](#running)


### Using the dev server

_Note: This may change in the future_

enaml-native ships with a dev server for reloading code on the fly without needing to rebuild the app. See the demo here [live reloading](https://youtu.be/CbxVc_vNiNk). This is similar to [hot reloading](https://facebook.github.io/react-native/blog/2016/03/24/introducing-hot-reloading.html) in react-native. It saves a lot of time when trying to build a UI as you can quickly try out code. It typically takes about 1-3 seconds for a reload vs about 10-15 for an app build and install, so you save 5x-10x per change (which adds up quickly).

The dev server watches your source files and notifies the app when they changed. The app then updates the files on the device with the changes, and invokes the reload method and recreates the UI. Currently only the view file is reloaded. Full reloading (anything except native libraries) will be added sometime in the future.

#### Enabling reloading

1. Set `app.dev="<dev_server_ip>"` in your `main.py` where `dev_server_ip` is the ip of your computer
2. Define a `def reload_view(app)` function and set `app.reload_view = reload_view`. This just typically imports your enaml views, reloads them (using pythons `reload` function), and reassigns `app.view`
3. Rebuild the app
4. Make sure your device is on the same LAN network or can access the dev server (you can test it in the browser)

#### Starting the dev server

1. cd to the project folder
2. Run `./enaml-native start`

#### Using

Make a change to your source code, and wala, the app reloads!
