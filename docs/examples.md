### Playground

The easiest way to try out these examples is by downloading the [Python Playground](https://play.google.com/store/apps/details?id=com.frmdstryr.pythonplayground) app. This app allows you to paste code into a web based editor and run it as if it were built as part of the app!

Once downloaded, start the app, and then go to [http://your-phone-address:8888](http://localhost:8888). If using a simulator run `adb forward tcp:8888 tcp:8888` and go to [http://localhost:8888](http://localhost:8888).

Copy and paste the example code in and click the play button. The app reloads and there you go! You can try out any code this way as well so feel free to play around!

[![Python Playground](https://img.youtube.com/vi/2IfRrqOWGPA/0.jpg)](https://youtu.be/2IfRrqOWGPA)

> Note: This project is changing very rapidly, some of these examples will only work on the master branches version of code!


### Basics

#### Text

Use a `TextView` to show text. You can set color, size, font, and other properties.  

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        TextView:
            text = "Hello world!"
            text_color = "#00FF00"
            text_size = 32
            font_family = "sans-serif"



#### Text Inputs
You can observe text input changes by binding to the `text` attribute.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        flex_direction = "column"
        EditText: et1:
           pass
        EditText: et2:
           #: Two way binding
           text := et1.text
        TextView:
            text << "You typed: {}".format(et1.text)




#### Toggle Switch 
You can handle Switch, CheckBox, and ToggleButton checked changes with the `checked` attribute.

    :::python
    from enamlnative.widgets.api import *
    
    enamldef ContentView(Flexbox):
        flex_direction = "column"
        Switch: sw:
           text = "Switch"
        CheckBox: cb:
            text = "Checkbox"
            #: Two way binding
            checked := sw.checked
        PushButton:
            text = "PushButton"
            checked := sw.checked
        TextView:
            text << "Switch state: {}".format(sw.checked)



#### Buttons 
You can handle button clicks with the `clicked` event.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        Button: btn:
           attr clicks = 0
           text = "Click me!"
           clicked :: self.clicks +=1
        TextView: txt:
           text << "Clicked: {}".format(btn.clicks)



#### Clickable 
Any `View` can be made clickable by setting `clickable=True` and using the `clicked` event.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        TextView: txt:
           attr clicks = 0
           text << "Click me: {}".format(self.clicks)
           clickable = True
           clicked :: self.clicks +=1



#### Width and Height 
You can define size using `layout_width` and `layout_height`. Can be either an integer string `200` (in dp), `wrap_content`, or `match_parent`.

    :::python
    from enamlnative.widgets.api import *

    enamldef ContentView(Flexbox):
        orientation = "vertical"
        Flexbox: 
           background_color = '#00FF00'   
           layout = dict(flex_basis = 0.3)
        Flexbox: 
           background_color = '#FFFF00'   
           layout = dict(flex_basis = 0.2)
        Flexbox: 
           background_color = '#0000FF'  
           layout = dict(flex_basis = 0.5)




### App Login

An app that shows simple login and logout screens. 

[![See the demo on youtube](https://img.youtube.com/vi/mSb37wTMfW0/0.jpg)](https://youtu.be/mSb37wTMfW0)

    :::python

    """

    A simple login app example.


    """
    from atom.api import *
    from enaml.core.api import *
    from enamlnative.widgets.api import *
    from enamlnative.core.app import BridgedApplication

    class User(Atom):
        username = Unicode()
        password = Unicode()


    class App(Atom):
        """ App state and controller """

        theme_color = Unicode("#cab")

        #: Define our "user database"
        users = List(User,default=[
            User(username="Bob",password="secret"),
            User(username="Jane",password="sweet"),
        ])

        #: Current user
        current_user = Instance(User)

        def login(self,user,password):
            """ Return a user if the user and pwd match """
            #: Simulate a login that takes time
            app = BridgedApplication.instance()

            #: Get an async result
            result = app.create_future()

            def simulate_login(result, user,password):
                for u in self.users:
                    if u.username==user and u.password==password:
                        self.current_user = u
                        result.set_result(self.current_user)
                        return

                #: No passwords match!
                self.current_user = None
                result.set_result(self.current_user)

            #: Simulate the call taking some time
            #: In a real app we would check using some web service
            app.timed_call(1000,simulate_login,result,user,password)

            return result



    enamldef SignInScreen(PagerFragment): view:
        attr app: App
        attr working = False
        attr pager << view.parent
        attr error = ""
        Flexbox:
            flex_direction = "column"
            background_color = "#eee"
            justify_content = "center"
            padding = (30, 30, 30, 30)

            Flexbox:
                justify_content="center"
                Flexbox:
                    layout_height="wrap_content"
                    layout_width="wrap_content"
                    flex_direction="column"
                    justify_content="center"
                    #background_color="#f00"
                    Icon:
                        text = "{fa-rocket}"
                        text_size = 128
                        text_color << view.app.theme_color
                    TextView:
                        text = "Your company"
            Flexbox:
                flex_direction = "column"
                #layout = dict(flex_basis=0.4)
                TextView:
                    text = "Username"
                EditText: username:
                    #: So it clears when the user is reset
                    text << "" if view.app.current_user else ""
                TextView:
                    text = "Password"
                EditText: password:
                    #: So it clears when the user is reset
                    text << "" if view.app.current_user else ""
                    input_type = "text_web_password"

                TextView:
                    text << view.error
                    text_color = "#f00"
                Conditional: cond:
                    condition << bool(view.working)
                    ActivityIndicator:
                        padding = (0,10,0,0)
                        style="small"                    
                Conditional:
                    condition << bool(not view.working and not view.app.current_user)
                    Button:
                        style = "borderless"
                        text << "Sign In"
                        #text_color << view.app.theme_color
                        attr root << view
                        func on_login_result(r):
                            #: Why is scope screwed up?
                            view = self.root
                            view.working = False
                            if r is None:
                                view.error = "Invalid username or password"
                            else:
                                view.error = ""
                                view.pager.current_index +=1

                        clicked :: 
                            view.working = True
                            self.root = view
                            #: Simulate an async login request
                            view.app.login(
                                username.text,
                                password.text).then(on_login_result)

                Conditional:
                    #: Dispal
                    condition << view.app.current_user is not None
                    Flexbox:
                        layout_height = "wrap_content"
                        justify_content = "center"
                        Icon:
                            padding = (0,10,0,0)
                            text = "{fa-check}"
                            text_size = 32
                            text_color << view.app.theme_color


    enamldef HomeScreen(PagerFragment): view:
        attr app: App
        attr user << app.current_user
        Flexbox:
            background_color << "#eee"
            justify_content = "center"
            Flexbox:
                flex_direction="column"
                Flexbox:
                    justify_content = "center"
                    Icon:
                        padding = (0,10,0,0)
                        text = "{fa-thumbs-up}"
                        text_size = 128
                        text_color << view.app.theme_color
                Flexbox:
                    justify_content = "center"
                    TextView:
                        text << "{}, you rock!".format(view.user.username) if view.user else ""
                        text_color << view.app.theme_color
                Flexbox:
                    flex_direction = "column"
                    justify_content = "flex_end"
                    Button:
                        style = "borderless"
                        text = "Logout"
                        clicked :: 
                            view.app.current_user = None
                            view.parent.current_index = 0


    enamldef ContentView(Flexbox): root:
        #: Our app state
        attr app = App()
        ViewPager: 
            #: Don't let them go by swiping!
            paging_enabled = False
            SignInScreen:
                app << root.app
            HomeScreen:
                app << root.app

### App Intro

A simple app intro screen with dots for paging and next/back buttons. 

[![See the demo on youtube](https://img.youtube.com/vi/UxctC4L2zD0/0.jpg)](https://youtu.be/UxctC4L2zD0)

    :::python
    """

    A simple app intro screen!

    """
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *

    enamldef PagerDots(Flexbox):
        attr icon = "fa-circle"
        attr color = "#fff"
        attr pager
        layout_height = "100"
        justify_content = "space_between"
        align_content = "center"
        layout = dict(align_self = "flex_end")
        attr pages << [c for c in pager._children if isinstance(c,Fragment)]
        attr next_enabled = True
        attr back_enabled = True
        Flexbox:
            Button:
                enabled << pager.current_index>0 and back_enabled
                style = "borderless"
                text << "Back" if self.enabled else ""
                text_color << color
                clicked :: pager.current_index -=1
        Flexbox:
            #layout_width = "wrap_content"
            justify_content = "center" 
            align_items = "center"
            Looper:
                iterable << range(len(pages))
                Icon:
                    text = "{%s}"%icon
                    padding = (5,5,5,5)
                    text_color << color
                    alpha << 1 if pager.current_index==loop_index else 0.4
                    clickable = True
                    clicked :: pager.current_index = loop_index
        Flexbox:
            Button:
                enabled << pager.current_index+1<len(pages) and next_enabled
                style = "borderless"
                text << "Next" if self.enabled else ""
                text_color << color
                clicked :: pager.current_index +=1

    enamldef AppIntro(Flexbox): view:
        alias screens
        flex_direction = "column"
        #padding = (10, 10, 10, 10)
        ViewPager: view_pager:
            Block: screens:
                pass
        PagerDots: dots:
            pager << view_pager

    enamldef Text(TextView):
      text_color = "#fff"
      text_size = 18
      font_family = "casual"

    enamldef HomeScreen(PagerFragment):
        Flexbox:
            flex_direction = "column"
            padding = (10,10,10,10)
            ImageView:
                src = "@mipmap/ic_launcher"
            Text:
              text = "Welcome to the python playground!"
              text_size = 32
            Text:
              padding = (0, 30, 0, 0)
              text = "This app lets you write an Android app using python from your web browser!!"
            Text:
              padding = (0, 30, 0, 0)
              text = "Swipe or click next to get started."

    enamldef GettingStartedScreen(PagerFragment):
        Flexbox:
            flex_direction = "column"
            padding = (10,10,10,10)
            Flexbox:
                flex_direction = "column"
                layout = dict(flex_basis=0.7)
                Text:
                  text = "Getting Started"
                  text_size = 32
                Text:
                  padding = (0, 30, 0, 0)
                  text = "Open settings and get the Wifi IP address of your device. " \
                         "Now open your browser and go to:"
                Flexbox:
                    layout_height = 'wrap_content'
                    justify_content = "center"
                    Text:
                        text = "http://<device-ip>:8888/"
                Text:
                  padding = (0, 30, 0, 0)
                  text = "If using a simulator, run:"
                Flexbox:
                    layout_height = 'wrap_content'
                    justify_content = "center"      
                    Text:
                        text = "adb forward tcp:8888 tcp:8888"
                Text:
                     text = "and go then to:"
                Flexbox:
                    layout_height = 'wrap_content'
                    justify_content = "center"
                    Text:
                        text = "http://localhost:8888/"
            Flexbox:
                justify_content = "center"
                align_items = "center"
                layout = dict(flex_basis=0.3)
                Icon:
                  text = "{fa-terminal}"
                  text_size = 128

    enamldef PlayScreen(PagerFragment):
        Flexbox:
            flex_direction = "column"
            padding = (10,10,10,10)
            Flexbox:
                flex_direction = "column"
                layout = dict(flex_basis=0.7)
                Text:
                  text = "Play!"
                  text_size = 32
                Text:
                  padding = (0, 30, 0, 0)
                  text = "Enter your code in the editor and press play! "\
                         "The app will reload with your code!"
                Text:
                  padding = (0, 30, 0, 0)
                  text = "Documentation and examples can be found at: "
                Text:
                    text_color = "#123"
                    text = "www.codelv.com/projects/enaml-native/docs/"
            Flexbox:
                justify_content = "center"
                align_items = "center"
                layout = dict(flex_basis=0.3)
                Icon:
                  text = "{fa-rocket}"
                  text_size = 128


    enamldef ContentView(AppIntro): view:
      background_color = "#6CA6CD"
      Block:
        block = parent.screens
        HomeScreen:
            pass
        GettingStartedScreen:
            pass
        PlayScreen:
            pass



### Email Inbox

A simple app showing usage of a toolbar, drawer, and scrollview. 

[![See the demo on youtube](https://img.youtube.com/vi/73GLBTNTVIA/0.jpg)](https://youtu.be/73GLBTNTVIA)

    :::python
    """

    A simple email app.

    """

    from atom.api import *
    from enaml.core.api import *
    from enamlnative.widgets.api import *

    class Message(Atom):
        name = Unicode()
        subject = Unicode()
        message = Unicode()

    class Folder(Atom):
        name = Unicode()
        messages = List(Message)

    class User(Atom):
        name = Unicode()
        email = Unicode()

    class App(Atom):
        #: Our user
        user = Instance(User)

        def _default_user(self):
            return User(name="Me", email="user@example.com")

        #: Selected folder
        current_folder = Instance(Folder)

        def _default_current_folder(self):
            return self.folders[0]

        #: Selected message
        current_message = Instance(Message)

        #: Email folders
        folders = List(Folder,default=[
            #: Create some dummy data
            Folder(name="Inbox",messages=[
                Message(name="John Doe", subject="Subject",message="This is a message") for i in range(30)    
            ]),
            Folder(name="Sent",messages=[
                Message(name="Me", subject="Subject",message="This is a draft") for i in range(30)    
            ]),
            Folder(name="Draft",messages=[
                Message(name="Me", subject="Subject", message="This is a draft") for i in range(30)    
            ]),
        ])

    enamldef Drawer(ScrollView): view:
        #: Required to set drawer to left or right
        attr app: App
        layout_gravity = "left"
        layout_width = '300'
        layout_height = 'match_parent'
        background_color = "#fff"
        Flexbox:
            flex_direction = "column"
            Flexbox:
                padding = (10,10,10,10)
                Icon:
                    layout_width = "64"
                    text = "{fa-user}"
                    text_size = 32
                Flexbox:
                    flex_direction = "column"
                    padding = (20, 0, 0, 0)
                    TextView:
                        text << app.user.name
                        font_family = "sans-serif-medium"
                    TextView:
                        text << app.user.email
            Flexbox:
                layout_height="1"
                layout_width = "match_parent"
                background_color = "#ccc"
            Looper:
                iterable << app.folders
                Flexbox:
                    align_items = "center"
                    padding = (10,10,10,10)
                    clickable = True
                    clicked :: 
                        #: Set folder and close the drawer
                        app.current_folder = loop_item
                        view.parent.opened = []
                    Icon:
                        text = "{md-folder}"
                        text_size = 24
                    TextView:
                        padding = (20, 0, 0, 0)
                        text << loop_item.name


    enamldef ContentView(DrawerLayout): drawer:
        attr app = App()
        Flexbox:
            flex_direction = "column"
            background_color = "#eee"
            Toolbar:
                layout_height = "100"
                content_padding = (0,0,0,0)
                background_color = "#123"
                Flexbox:
                    align_items = "center"
                    IconButton:
                        text = "{md-menu}"
                        text_size = 24
                        text_color = "#fff"
                        layout_width = "50"
                        style = "borderless"
                        clicked ::
                            drawer.opened =  [] if drawer.opened else [left_drawer] 
                    TextView:
                        text << app.current_folder.name
                        text_color = "#fff"
                        text_size = 24
                        font_family = "sans-serif-medium"

            ScrollView:
                Flexbox:
                    flex_direction = "column"
                    Looper:
                        iterable << app.current_folder.messages
                        Flexbox:
                            padding = (10,20,10,20)
                            align_items = "center"
                            Icon:
                                layout = dict(flex_basis=0.3)
                                text = "{fa-user}"
                                text_size = 32
                            Flexbox:
                                padding = (10,0,0,0)
                                layout = dict(flex_basis=0.7)
                                flex_direction = "column"
                                TextView:
                                    text << loop_item.name
                                    font_family = "sans-serif-medium"
                                TextView:
                                    text << loop_item.subject
                        Flexbox:
                            #: Add a bottom border
                            layout_height="1"
                            background_color = "#ccc"
                    Button:
                        style="borderless"
                        text = "Load more"
                        clicked :: 
                            msgs = app.current_folder.messages[:]
                            #: Add more messages
                            msgs.extend([Message(name="Jack and Jill",subject="Hello!",message="Went up the hill again!") for i in range(10)])
                            app.current_folder.messages = msgs

        Drawer: left_drawer:
            app << drawer.app
        
      
### GPS Location Updates

There's a simple API for starting and stopping the GPS. The permissions must be added to the manifest.

[![See the demo on youtube](https://img.youtube.com/vi/Ra_ANAxzPD8/0.jpg)](https://youtu.be/Ra_ANAxzPD8)


    :::python


    from enamlnative.core.api import *
    from enamlnative.widgets.api import *

    from enamlnative.android.app import AndroidApplication
    from enamlnative.android.api import LocationManager, Location


    enamldef ContentView(Flexbox): view:
        flex_direction = "column"
        justify_content = "center"
        attr app = AndroidApplication.instance()
        attr started = False
        attr location: Location
        attr status = "Press start to begin"
        func on_location_update(location):
            #: Called when a location updates
            view.location = location

        func on_result(allowed):
            #: Called with result of
            if allowed:
                view.status = "Success! Waiting for location updates..."
                view.started = True
            else:
                view.status = "Permission denied or location is off."

        TextView: status:
            text << view.status
        Conditional:
            condition << location is not None
            TextView:
                text << "Location: gps={l.lat},{l.lng} "\
                        "acc={l.accuracy} alt={l.altitude}".format(l=location)
        Button:
            text << "Stop" if started else "Start"
            clicked ::
                #: Get the service
                status.text = "Checking permission..."
                if started:
                    view.status = "Stopped"
                    LocationManager.stop()
                    view.started = False
                else:
                    view.status = "Starting..."
                    LocationManager.start(on_location_update).then(on_result)

### Permissions

Example demonstrates the API for checking permissions and requesting access. Note permissions not in the manifest will be denied immediately without a popup request.

[![See the demo on youtube](https://img.youtube.com/vi/8QYsYSxkL2s/0.jpg)](https://youtu.be/8QYsYSxkL2s)

    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *

    from enamlnative.android.app import AndroidApplication

    enamldef ContentView(Flexbox): view:
        flex_direction = "column"
        justify_content = "center"
        attr app = AndroidApplication.instance()
        TextView:
            text = "Permission:"
        Spinner: sp:
            items = ['android.permission.ACCESS_FINE_LOCATION',
                     'android.permission.INTERNET',
                     'android.permission.CAMERA']

        TextView:
            text = "Status:"
        TextView: status:
            text = ''
        Button:
            text << "Check Permission"
            clicked ::
                #: Get the service
                status.text = "Checking permission..."

                #: Check with AndroidApplication.instance().has_permission(<perm>)
                #: Returns a boolean with the result
                app.has_permission(
                    sp.items[sp.selected]
                #: We have to pass in our scope to lambdas
                ).then(lambda r,s=status:setattr(s,'text',"Allowed:{}".format(r)))

        Button:
            text << "Request Permission"
            clicked ::
                #: Get the service
                status.text = "Checking Location permission..."
                #: Request with 
                #: AndroidApplication.instance().request_permissions([<perm>,...])
                #: Returns a dictionary with the result of each
                app.request_permissions(
                    [sp.items[sp.selected]]

                #: We have to pass in our scope to lambdas
                ).then(lambda r,s=status:setattr(s,'text',"Result:{}".format(r)))
            
            
### Wifi Thermostat

> Note: Source code and play store link coming soon...

[![See the demo on youtube](https://img.youtube.com/vi/7S8aWfzf89A/0.jpg)](https://youtu.be/7S8aWfzf89A)


### Barcode and QRCode scanning

Scan barcodes using the zxing library. 

> Note: Requires the [enaml-native-barcode](https://github.com/codelv/enaml-native-barcode) package

[![See the demo on youtube](https://img.youtube.com/vi/lYF8XioDd78/0.jpg)](https://youtu.be/lYF8XioDd78)


    :::python
    from enamlnative.core.api import *
    from enamlnative.widgets.api import *
    from zxing.widgets.barcode import BarcodeView, BarcodeFinderView
    from enamlnative.android.app import AndroidApplication
    
    app = AndroidApplication.instance()
    
    enamldef ContentView(Flexbox): view:
        flex_direction = "column"
        BarcodeFinderView:
            #: Request permission
            active = True
            mode = 'single'
            #: Set clickable
            clickable = True
            clicked :: self.scanning = not self.scanning
            scanned :: app.show_toast("{}".format(change['value']))




More to come!

