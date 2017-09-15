
Currently there is no `live` debugger where you can breakpoint and step through code like in react-native. There are a few helpful things you can do to make life easier though.

### Development server

A development server is included that let's you make changes to the code without having to rebuild the app. It operates in two modes. See [dev.py](https://github.com/codelv/enaml-native/blob/master/src/enamlnative/core/dev.py)

#### Client mode
In client mode, you run a `dev server` on your system and the app connects to it.  This lets you make changes using whatever editor you like. All changes within the apps `src` directories (in the `package.json`) will be watched for changes using watchdog. 

To use client mode and the dev server:

1. set `app.dev="<dev server ip>"`
2. set `app.reload_view` to a function reloads your modules and sets the `app.view
3. Rebuild the app
4. Finally start the dev server by running  `./enaml-native start` in your project folder.
5. Now make changes to your source files and watch it reload.

You will see:

    
    $ ./enaml-native start
    Entering into src
    Watching /home/jrm/Workspace/Apps/TestBible/src
    Tornado Dev server started on 8888
    Client connected!



and in the device log


    07-22 12:22:39.542 /app I/pybridge: Dev server connecting ws://192.168.34.103:8888/dev...
    07-22 12:22:39.687 /app I/pybridge: Dev server connected

A youtube video of reloading is here:

[Live Reloading](https://youtu.be/CbxVc_vNiNk)

#### Server mode

In server mode, the app hosts a web page with an editor and uses a websocket server to process changes to the code. This is how the playground app works. 

To enable server mode:

1. Set `app.dev = "server"`
2. Rebuild the app
3. Open `http://<ip of device>:8888` in your browser (when using a simulator run `adb forward tcp:8888 tcp:8888` and use `localhost`) 
4. Edit code in the browser.
    
### Profiling

You can profile using standard `cProfile` builtin to python. Usage is the same. See https://docs.python.org/2/library/profile.html

### Debugging the bridge 

One of the great things about using the bridge is being able to get a complete trace of everything that was happening.  To enable this set `app.debug = True` and rebuild the app. It will generate a nice trace of all bridge methods and callbacks. 



    07-22 12:01:55.014 /app I/pybridge: ======== Py <-- Native ======
    07-22 12:01:55.015 /app I/pybridge: ['event', [0, 111, 'onPageScrollStateChanged', [['java.lang.Integer', 2]]]]
    07-22 12:01:55.015 /app I/pybridge: ['event', [0, 111, 'onPageSelected', [['java.lang.Integer', 0]]]]
    07-22 12:01:55.015 /app I/pybridge: ['event', [0, 114, 'onTabUnselected', [['android.support.design.widget.TabLayout.Tab', 'android.support.design.widget.TabLayout$Tab@6c6e5d4']]]]
    07-22 12:01:55.015 /app I/pybridge: ['event', [45, 804, 'onCreateView', []]]
    07-22 12:01:55.015 /app I/pybridge: ===========================
    07-22 12:01:55.046 /app I/pybridge: ======== Py --> Native ======
    07-22 12:01:55.047 /app I/pybridge: ('c', (838, u'android.widget.ScrollView', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.047 /app I/pybridge: ('c', (839, u'android.widget.LinearLayout', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.047 /app I/pybridge: ('m', (839, 0, 'setOrientation', [('int', 1)]))
    07-22 12:01:55.048 /app I/pybridge: ('c', (840, u'android.support.v7.widget.CardView', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.048 /app I/pybridge: ('m', (840, 0, 'setPadding', [('int', 60), ('int', 60), ('int', 60), ('int', 60)]))
    07-22 12:01:55.048 /app I/pybridge: ('c', (841, u'android.view.ViewGroup$MarginLayoutParams', [('int', -1), ('int', -1)]))
    07-22 12:01:55.048 /app I/pybridge: ('m', (840, 0, 'setLayoutParams', [('android.view.ViewGroup$LayoutParams', ExtType(code=1, data='\xcd\x03I'))]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (841, 0, 'setMargins', [('int', 30), ('int', 30), ('int', 30), ('int', 30)]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (840, 0, 'setContentPadding', [('int', 30), ('int', 30), ('int', 30), ('int', 30)]))
    07-22 12:01:55.049 /app I/pybridge: ('c', (842, u'android.widget.LinearLayout', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (842, 0, 'setOrientation', [('int', 1)]))
    07-22 12:01:55.049 /app I/pybridge: ('c', (843, u'android.widget.TextView', [('android.content.Context', ExtType(code=1, data='\xff'))]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (843, 0, 'setTextKeepState', [('java.lang.CharSequence', u'Chapter - 1')]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (843, 0, 'setTypeface', [('android.graphics.Typeface', u'sans-serif-condensed-light'), ('int', 0)]))
    07-22 12:01:55.049 /app I/pybridge: ('m', (843, 0, 'setTextSize', [('float', 18.0)]))
    ...
    07-22 12:01:55.051 /app I/pybridge: ('r', (45, ('android.view.View', ExtType(code=1, data='\xcd\x03F'))))
    07-22 12:01:55.051 /app I/pybridge: ===========================
    07-22 12:01:55.087 /app I/pybridge: ======== Py <-- Native ======
    07-22 12:01:55.087 /app I/pybridge: ['event', [46, 805, 'onCreateView', []]]
    07-22 12:01:55.087 /app I/pybridge: ===========================

