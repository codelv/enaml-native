### Project structure

An enaml-native app is organized similar to a react-native app.

Create a new project with the [enaml-native-cli](https://github.com/codelv/enaml-native-cli).

The project directory consists of the basic structure:
  
    :::python
    android/      #: Android project using gradle
    ios/          #: iOS xcode project with cocoapods
    src/          #: Python source for your app 
    venv/         #: Python venv for enaml-native packages and p4a recipes
    package.json  #: Project config

This structure is created for you using the [enaml-native-cli](https://github.com/codelv/enaml-native-cli) 
when you run `enaml-native init <name> <bundle_id> <destination>`. 
Your actual apps are in the `android` and `ios` folders. The build scripts are configured 
to run enaml-native commands that build and package your python source files as required 
for the app based on the dependencies.

### Configuring the project

The `package.json` file is your project config. If you open it you see the following.
    
    :::json
    {
      "name": "Enaml-Native Demo",
      "bundle_id":"com.codelv.enamlnative.demo",
      "version": "1.8",
      "private": true,
      "sources": [
        "src/apps/playground",
        "src"
      ],
      "android": {
        "ndk":"~/Android/Crystax/crystax-ndk-10.3.2",
        "sdk":"~Android/Sdk",
        "arches": ["x86"],
        "dependencies": {
          "python2crystax": "",
          "enaml-native": "",
          "tornado": ">=4.0",
          "singledispatch":"",
          "backports_abc":"",
          "ply": ""
        },
        "excluded":[]
      },
      "ios": {
        "project": "demo",
        "arches": [
          "x86_64",
          "i386",
          "armv7",
          "arm64"
        ],
        "dependencies": {
          "openssl":"1.0.2l",
          "python":"2.7.13",
          "tornado": ">=4.0",
          "singledispatch": ">=0",
          "backports_abc": ">=0",
          "ply": "==3.10"
        },
        "excluded":[]
      }
    }


As you can see there's a few shared properties such as `name`, `bundle_id`, and `version` which are 
self explanatory, `sources`, and separate configs for `ios` and `android`. 

The `sources` list is a list of the source folders that the build system will copy into 
the __root__ of your python app. It does a recursive copy so any files, folders, subfolders, and 
files within will be added into your will be available on the actual app. You can add images, 
data files, etc.. it doesn't care.

Each platform config (`ios` and `android`) has `arches`, `dependencies`, and `excluded`. 
The rest are specfic for the platform.

As you may have guessed, `arches` defines which platforms to compile python and extensions modules 
for and `dependencies` is a list of python requirements to install on the app. Pure python 
requirements are installed via pip, anything with compiled extensions _MUST_ have a recipe for 
the specific platform. More on that later. 

> Note: As of cli v1.3, the dependency key and value simply are joined together using 
`"{}{}".format(k, v)` and sent to p4a as build requirements. So any `recipe` dependencies 
should NOT have a version (as it uses whatever recipe version is installed in the apps venv)! 
Pip dependencies can include versions. 

The `excluded` list is a list of [patterns](https://docs.python.org/2.7/library/glob.html) 
that you can use to exclude unused python modules from your app to reduce the app size.

For android there's `sdk` and `ndk` which are the paths used for building. You MUST update these to 
point to wherever your SDK and NDK are installed. 

For ios there's the `project` which defines the name of the `<project>.xcworkspace` that will be 
built.

If you're interested you can read through the 
[enaml-native cli](https://github.com/codelv/enaml-native-cli/blob/master/enaml-native) source 
which is what actually uses this config file.

### Build process

The build process depends on the platform but from a high level the following must occur.

1. Python dependencies must be cross compiled for the target platform and arches for each platform.
2. App python source, site-packages, and the standard library must be "bundled" to be included in the native app
3. The native app build system (gradle, xcode) must be configured to include the bundled python and any linked with compiled libraries. 
4. Native build system builds the app and uses python via native hooks and [the bridge](https://www.codelv.com/projects/enaml-native/docs/bridge).

> See [enaml-native packages](#enamlnativepackages)

### Building python

The `package.json` config file defines an `arches` list for each platform. 
This is the list of ABI's or target platforms to build your python and extensions for. 

> This is very complicated internally and only supported by OSX and linux! 
> Note: You can skip this by downloading and including precompiled libraries. Links to come see issue [#22](https://github.com/codelv/enaml-native/issues/22)

To cross compile python and modules for different arches you must:

1. Add or remove from the config `arches` list
2. Run `enaml-native clean-python`
3. Run `enaml-native build-python`

This will rebuild for both Android and iOS (if applicable). 
If you want to restrict building to only one or the other (on OSX only) pass the 
`--ios` or `--android` flag.

Python builds are done using modified versions of [python-for-android](https://github.com/kivy/python-for-android/) 
and [kivy-ios](https://github.com/kivy/kivy-ios/). The python build process is VERY complicated 
and prone to errors on new installs due to the various system dependencies.  

> Note: These modified projects are now included in the [enaml-native-cli](https://github.com/codelv/enaml-native-cli).


#### Debugging build failures

If the build fails for whatever reason you can get the full log by adding the `-d` flag like

`enaml-native build-python -d`


This will print the entire p4a build in debug mode. See the p4a docs. You can check the following
locations to ensure the build is working in each stage.

            
1. Make sure the download is correct in
    `~/.local/share/python-for-android/packages/<recipe-name>`

2. Make sure the patches applied and build is correct under
    `~/.local/share/python-for-android/build/other_builds/<recipe-name>`

3. Make sure everything was installed to
    `~/.local/share/python-for-android/dists/enaml-native/python`
    
4. Finally make sure everything was copied to:
    Python sources:
    `<app dir>/build/python/<arch>/site-packages/`
    
    Native libraries:
    `<app dir>/build/python/<arch>/modules/`
    
5. Lastly make sure enaml-native is copying everything during the build-android command to the 
   actual android project.
   
    Python sources:
   `<app dir>/android/app/src/main/assets/python/`
    
    Native libraries:
    `<app dir>/venv/packages/enaml-native/android/src/main/lib/<arch>/`
            
For more detailed debugging see what the actual [build command](https://github.com/codelv/enaml-native-cli/blob/master/enaml-native#L433) 
from the cli is doing.

### Release your app

It's easiest to just make release builds using android-studio or xcode. It will prompt you to 
do any configuration necessary.

Once that is done you can then do release builds with the enaml-native cli using 
`enaml-native build-android --release` or `enaml-native build-ios --release`. 
The `--release` flag tells it to do a release build (it's debug by default). 

For help see the documentation for each platform, enaml-native does nothing special here.

#### Reducing app size

Since apps must include both the python interpreter (as native libraries) and all the python
and app sources, the installed apps can get large if care is not taken to remove unused modules.

> Note: Future changes try to reduce app size automatically by using cx_Freeze's module finder 
and running code "minification" on python builds! 

If your app uses the [twisted](https://twistedmatrix.com/) even loop, for example, the twisted 
package alone is a whopping **7.3MB** (and that's even excluding tests!). Most android and ios 
apps aren't even that big as is! So how do we reduce it?

##### Excluding unused packages and modules

As mentioned earlier the `excluded` list in the `package.json` can be used to remove unnecessary
packages and files from the python build (located under `build/python/python.tar.gz` in your app
directory). To find out which packages are using a lot of space use the following command:

    :::bash
    du -h build/python/build
    
    #: Or for big hitters
    du -h build/python/build | grep M
      
This will list all the folders and the size of all the contents in a "human readable" size format.
  
  
    $ du -h build/python/build | grep M
    1.1M    build/python/build/enaml/widgets
    3.2M    build/python/build/enaml
    1.5M    build/python/build/setuptools
    2.7M    build/python/build/enamlnative
    1.7M    build/python/build/encodings
    1.1M    build/python/build/twisted/words
    1.2M    build/python/build/twisted/python
    1.1M    build/python/build/twisted/web
    2.2M    build/python/build/twisted/internet
    1.4M    build/python/build/twisted/conch
    13M     build/python/build/twisted
    32M     build/python/build


Wow, this app's unoptimized python sources is 32MB uncompressed (4.6MB gzippped), yikes! 
The app with no optimisations is ~45MB installed. We can see, enaml, enamlnative, and twisted are 
all big. Lets reduce see if we can reduce that.

 
    :::json
    "android": {
      # etc...
      "excluded": [
         "setuptools",
          "pkg_resources",
          "exampleproj",
          "sqlite3",
          "unittest",
          "xml",
          "hotshot",
          "email",
          "home",
          "enaml/workbench*",
          "enaml/stdlib*",
          "enaml/applib*",
          "enaml/scintilla*",
          "enaml/widgets/[!_tw]*.pyo",
          "enamlnative/ios*",
          "enamlnative/core/eventloop*",
          "enamlnative/core/hotswap*",
          "twisted/internet/iocpreactor*",
          "twisted/conch*",
          "twisted/words*",
          "twisted/trial*",
          "twisted/mail*",
          "incremental/test*",
          "multiprocessing"
      ]
      # etc..
    } 

In `package.json` we add a bunch of excludes to the list, then run `enaml-native run-android` again 
to make sure the app still works correctly. This reduces the app size by about 10MB, to about 36MB
of usage but improvements can still be made.  Twisted is just a huge project (and this app also
includes the `enaml-native-charts` which adds about 4-5MB!).

You can also use the apk analyzer in android-studio which nicely graphs which files are using space
within an apk (it even shows within the python.tar.gz!) so use that as well!


##### Building for separate arches or excluding unused arches

Another way to significantly reduce app apk size is by building apps for a specific arch. 

    :::json
        "arches": [
            "x86", # Remove this line and run `enaml-native build-python`
            "armeabi-v7a"
        ], 

For example, dropping the `x86` arch (which is typically only used for emulators and some tablets) 
tcuts the size of the stock  `HelloWorld` apk down by about ~30% (9.7MB to 6.6MB) and the installed
app size by about 10%!

> Note: As time goes on, more optimizations will be found and added. The installed optimized app size is 
still slightly larger than a react-native app (by 20-30%).  


### Enaml-native packages

With the release of the [enaml-native-cli](https://github.com/codelv/enaml-native-cli) it is now 
possible to create a single pip package that includes `android` and `ios` libraries along
with the python source to use them. These are called `enaml native packages` for lack of a better 
name and can be installed with either `pip` or the `enaml-native` cli. 

This is based on the design from the [react native package manager](https://github.com/rnpm/rnpm).

> Note: This is early development and will probably change

#### Why?

Because `enaml-native` is growing and apps will typically want to only include the native 
dependencies they need. The project was redesigned and broken down into smaller installable 
`EnamlPackages` each containing their own with separate native and python requirements.

This is to address issues python-for-android is having with non-reproducible builds due to 
recipes linking to master versions as well as the issue unique to enaml-native where different
native libraries are required.  

It is also a step making it more like react-native which does package management very well.  
Using these packages will allow any user to create, maintain, and share their own versions of 
pluggable libraries as needed. There is no need to have your code merged in by some "core" group
of maintainers.

#### Concept 

The concept of the package is pretty simple. 

1. Each "app" project now has it's own `venv` with the `enaml-native-cli` installed.
2. You install your apps `packages` and `recipes` in the `venv` using either pip or the cli
3. Once installed, they are available for the build process to use as an app requirement
4. Define which of these are needed by your app in your apps requirements (the `package.json`)


#### Package format

A package is simply a directory with the following subdirectories and files.

    :::python
    android/          #: Android library using gradle (if applicable)
    ios/              #: iOS xcode library using cocoapods (if applicable)
    src/              #: Python source for your app 
    src/setup.py      #: Setupfile for your package's source (this is what is installed on the app)
    setup.py          #: Pip setup file for the enaml-native package
    

To make an "enaml-package" that follows this format use: 
`enaml-native init-package <some-package-name> <destination/folder>`

#### Linking native libraries

If your package requires native dependencies (ex the `enaml-native-maps` package 
requires native android `GoogleMaps`) the android or ios project can be "linked" 
to your library when its installed by the user. This is done by the 
`enaml-native link` command. 

"Linking" is automatically adding the necessary changes to the users android and ios projects
(such as adding your library as a project to compile build.gradle) so they can simply install
and use it right away. This makes it easier for new users to quickly get started with your code 
without having to read through how to configure it all manually.

An entry point `enaml_native_linker` was added to the cli that lets you define a custom function
to link the users project where required.  

> Note: Currently only linking has been implemented for android (you can use your an entry point)

Unlinking is the reverse of linking and unlinking our package from a users project should remove
any changes made during linking. This is required so upgrading or switching dependencies is 
seamless and error free. 



### Android specifics

You can open the `android` folder in Android studio and it will load like any normal android project. 
This way you can easily modify any native java code and get all the highlighting and error 
checking, etc. all android documentation applies here. The project uses the gradle build system.  

#### Building for Android

The android build process is done in two phases.

1. Build CPython and compiled extensions for each arch via `enaml-native build-python`
2. Gradle hook to bundle all pure python app source, the standard library, and site-packages. 

##### Building python and compiled extensions for Android

enaml-native builds python and any dependencies that have compiled components (c, c++, cython) 
using a fork of [python-for-android](https://github.com/codelv/enaml-native/tree/master/python-for-android).

This fork is modified as follows:

1. Added an enaml bootstrap
2. All recipes removed and those required for enaml-native were created as separate p4a-<recipe> 
   projects using the `p4a_recipe` entry_point.
3. Several other small modifications.

> Note: The recipes were removed so that version specific recipes will always be used. This ensures
 that builds do not break in the future and makes it easy to update when new versions are released.

Building is invoked with `enaml-native build-python` based on the config file. This calls 
`enaml-native ndk-build` on the [native hook](https://github.com/codelv/enaml-native/blob/master/android/src/main/jni) 
and then does a `python-for-android create` build to compile python and any recipes.  

Once done all of your libraries will go to the jni libs folder 
`venv/packages/enaml-native/android/src/main/libs/<arch>`. 
All modules here will be included in the app by gradle (see [build.gradle](https://github.com/codelv/enaml-native/blob/master/android/build.gradle#L24)).

> Note: Libraries matching the pattern `lib*.so` are automatically copied during the App install 
  on the device. This speeds up the startup. Any modules NOT matching this need copied manually 
  by your app's main activity.


> Note: If you want to add a dependency that has a compiled component it MUST have a recipe! 
  You can create your own to install using the `p4a_recipe` entry_point.

These compiled modules are then imported using a custom import hook, see [import_hooks.py](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/core/import_hooks.py).

##### Bundling python for Android

enaml-native hooks itself into the gradle build process to include your python source and libraries.
This hook is in [android/build.grade](https://github.com/codelv/enaml-native/blob/master/android/build.gradle).

It simply runs `enaml-native bundle-assets` which packages all the python and app source code 
into a file  `python.tar.gz` and copies it to `android/app/src/main/assets/python/python.zip`.

The intermediate steps of this can be checked by looking in the following locations:

- p4a's dists folder `~/.local/share/python-for-android/dists/enaml-native/python`
- Your apps `build/python/` folder

> Note: This hook does NOT include python or any extensions ONLY pure python assets and other  
  recipe files! See above for building extensions.

#### Adding libraries with Gradle

To add custom libraries:

1. Open the project in android-studio 
2. Modify the `android/app/build.gradle` as needed.  
3. Run gradle sync (should prompt you when you make a change) and it will collect your new libraries

You can see there's a few already being used. Once a library is added with gradle you can use it 
via making a wrapper Proxy and Toolkit component (see the 
[native component](https://www.codelv.com/projects/enaml-native/docs/native-components) docs) .



### iOS specifics

You can open the project.xcworkspace within the `ios` folder in xcode and work in your app normally. All iOS
docs apply here.

The android build process is done in two phases.

1. Build CPython and compiled extensions  for each arch via `./enaml-native build-python`
2. Gradle hook to bundle all pure python app source, the standard library,  and site-packages. 

#### Building for iOS

The iOS build process is done in two phases.

1. Build CPython and compiled extensions  for each arch via `./enaml-native build-python`
2. A Build Phase hook to bundle all pure python app source, the standard library, and site-packages. 

##### Building python and compiled extensions for iOS

enaml-native builds python and any dependencies that have compiled components (c, c++, cython) 
using a fork of [kivy-ios](https://github.com/codelv/enaml-native/tree/master/python-for-ios).

This fork is __heavily__ modified as follows:

1. All builds were converted to create dylibs (Min iOS version is set to 8)
2. Python updated to 2.7.13
3. Added and modified several recipies to work with enaml-native

Building is invoked with `./enaml-native build-python` in [enaml-native](https://github.com/codelv/enaml-native/blob/master/enaml-native)
based on the config file. This calls `python-for-ios/toolchain.py` build internally.

The entire build process is complicated and very issue prone. I'm hoping to be able to elimnate this entriely by
providing a build server to compile libraries for you.

> Note: As of this writing I have NOT submitted an app to the App Store

These compiled modules are then imported using a custom import hook, see [import_hooks.py](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/core/import_hooks.py).

There's a few blog posts on what exactly was changed that may help you when building new recipies [on my blog](http://blog.codelv.com).


#### Adding libraries with CocoaPods

To add custom libraries:

1. Modify the `ios/<app>/Podfile` as needed
2. cd to `ios/<app>` and run `pod install` or `pod update`
3. Rebuild your xcode project

You can see there's a few already being used. Once a library is added with cocopods you can use it via making
a wrapper Proxy and Toolkit component (see the [native component](https://www.codelv.com/projects/enaml-native/docs/native-components) docs) .


That's all for now! Thanks for reading! Please suggest more docs if something is confusing.
