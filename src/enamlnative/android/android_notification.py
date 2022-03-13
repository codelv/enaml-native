"""
Copyright (c) 2017-2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Apr 4, 2018
"""
from typing import ClassVar, Optional
from atom.api import Bool, Instance, List, Typed
from enaml.application import deferred_call
from enamlnative.widgets.notification import ProxyNotification
from .android_content import (
    BroadcastReceiver,
    Context,
    Intent,
    PendingIntent,
    SystemService,
)
from .android_image_view import Bitmap, Glide, RequestBuilder, RequestManager
from .android_toolkit_object import AndroidToolkitObject
from .android_utils import Uri
from .app import AndroidApplication
from .bridge import JavaBridgeObject, JavaMethod, JavaStaticMethod

package = "androidx.core.app"


class Notification(JavaBridgeObject):
    """A wrapper for an Android's notification apis"""

    __nativeclass__ = f"{package}.NotificationCompat"

    class Builder(JavaBridgeObject):
        """Builds a notification.

        Notes
        ------
        The constructor automatically sets the when field to
        System.currentTimeMillis() and the audio stream to the STREAM_DEFAULT.

        """

        __nativeclass__ = f"{package}.NotificationCompat$Builder"
        __signature__ = [Context, str]
        addAction = JavaMethod(f"{package}.NotificationCompat$Action")
        addAction_ = JavaMethod("android.R", "java.lang.CharSequence", PendingIntent)
        addInvisibleAction = JavaMethod(f"{package}.NotificationCompat$Action")
        addInvisibleAction_ = JavaMethod(
            "android.R", "java.lang.CharSequence", PendingIntent
        )
        addPerson = JavaMethod(str)
        build = JavaMethod(returns="android.app.Notification")

        setAutoCancel = JavaMethod(bool)
        setBadgeIconType = JavaMethod("android.R")
        setCategory = JavaMethod(str)
        setChannelId = JavaMethod(str)
        setColor = JavaMethod("android.graphics.Color")
        setColorized = JavaMethod(bool)
        setContent = JavaMethod("android.widget.RemoteViews")
        setContentInfo = JavaMethod("java.lang.CharSequence")
        setContentIntent = JavaMethod(PendingIntent)
        setContentText = JavaMethod("java.lang.CharSequence")
        setContentTitle = JavaMethod("java.lang.CharSequence")
        setCustomBigContentView = JavaMethod("android.widget.RemoteViews")
        setCustomContentView = JavaMethod("android.widget.RemoteViews")
        setCustomHeadsUpContentView = JavaMethod("android.widget.RemoteViews")
        setDefaults = JavaMethod(int)
        setDeleteIntent = JavaMethod(PendingIntent)
        setExtras = JavaMethod("android.os.Bundle")
        setFullScreenIntent = JavaMethod(PendingIntent, bool)

        setGroup = JavaMethod(str)
        setGroupAlertBehavior = JavaMethod(int)
        setGroupSummary = JavaMethod(bool)
        setLargeIcon = JavaMethod(Bitmap)
        setLights = JavaMethod("android.graphics.Color", int, int)
        setLocalOnly = JavaMethod(bool)
        setNumber = JavaMethod(int)
        setOngoing = JavaMethod(bool)
        setOnlyAlertOnce = JavaMethod(bool)
        setPriority = JavaMethod(int)
        setProgress = JavaMethod(int, int, bool)
        setPublicVersion = JavaMethod("android.app.Notification")
        setRemoteInputHistory = JavaMethod("Landroid.app.Notification;[")
        setShortcutId = JavaMethod(str)
        setShowWhen = JavaMethod(bool)
        setSmallIcon = JavaMethod("android.R")
        setSmallIcon_ = JavaMethod("android.R", int)
        setSortKey = JavaMethod(str)
        setSound = JavaMethod(Uri)
        setSound_ = JavaMethod(Uri, int)
        setStyle = JavaMethod(f"{package}.NotificationCompat$Style")
        setSubText = JavaMethod("java.lang.CharSequence")
        setTicker = JavaMethod("java.lang.CharSequence", "android.widget.RemoteViews")
        setTicker_ = JavaMethod("java.lang.CharSequence")
        setTimeoutAfter = JavaMethod("long")
        setUsesChronometer = JavaMethod(bool)
        setVibrate = JavaMethod("J[")
        setVisibility = JavaMethod(int)
        setWhen = JavaMethod("long")

        #: Glide Manager for loading bitmaps
        manager = Instance(RequestManager)

        #: BroadcastReceiver for handling actions
        _receivers = List(BroadcastReceiver)

        def _default_manager(self):
            app = AndroidApplication.instance()
            return RequestManager(__id__=Glide.with__(app))

        def load_bitmap(self, src: str) -> Bitmap:
            mgr = self.manager
            assert mgr is not None
            r = RequestBuilder(__id__=mgr.load(src)).asBitmap()
            return Bitmap(__id__=r.__id__)

        def update(
            self,
            title: str = "",
            text: str = "",
            info: str = "",
            sub_text: str = "",
            ticker: str = "",
            importance: int = 3,  # IMPORTANCE_DEFAULT
            group: str = "",
            group_summary: Optional[bool] = None,
            group_alert_behavior: Optional[int] = None,
            small_icon="@mipmap/ic_launcher",
            large_icon="",
            number=None,
            ongoing=None,
            local_only=None,
            style=None,
            color=None,
            colorized=None,
            sound=None,
            light_color="",
            light_on=500,
            light_off=500,
            show_when=None,
            show_stopwatch=False,
            show_progress=False,
            progress_max=100,
            progress_current=0,
            progress_indeterminate=False,
            auto_cancel=True,
            timeout_after=0,
            sort_key="",
            vibration_pattern=[],
            shortcut_id="",
            category="",
            badge_icon_type=None,
            only_alert_once=None,
            notification_options=None,
            actions=None,
        ):
            """Creates and shows a notification. On android 8+ the channel
            must be created.

            Parameters
            ----------
            badge_icon_type: Int
                Sets which icon to display as a badge for this notification.
            category: String
                Set the notification category.
            channel_id: String
                The id of the channel this notification is displayed on
            color: String
                A color string ex #F00 for red
            colorized: Bool
                Set whether this notification should be colorized.
            group: String
                Set this notification to be part of a group of notifications
                sharing the same key.
            group_summary: Bool
                Set this notification to be the group summary for a group of
                notifications.
            group_alert_behavior: Int
                Sets the group alert behavior for this notification.
            title: String
                Set the title (first row) of the notification, in a standard
                notification.
            text: String
                Set the text (second row) of the notification, in a standard
                notification.
            info: String
                Set the large text at the right-hand side of the notification.
            sub_text: String
                Set the third line of text in the platform notification
                template.
            ticker: String
                Sets the "ticker" text which is sent to accessibility services.
            importance: Int
                The importance or priority of the notification
            number: Int
                Set the large number at the right-hand side of the
                notification.
            ongoing: Bool
                Set whether this is an ongoing notification.
            local_only: Bool
                Set whether or not this notification is only relevant to the
                current device.
            style: String
                A style resource string
            small_icon: String
                A resource identifier @drawable/my_drawable
            large_icon: String
                A resource that glide can load (file:// or http://) url
            show_when: Bool
                Control whether the timestamp set with setWhen is shown in the
                content view.
            show_stopwatch: Bool
                Show the when field as a stopwatch.
            show_progress: Bool
                Show a progressbar
            progress_current: Int
                Current progress
            progress_max: Int
                Max progress
            progress_indeterminate: Bool
                Progress should be indeterminate
            light_color: String
                Set the argb value that you would like the LED on the device to
                blink
            light_on: Int
                Set the on duration of the LED
            light_off: Int
                Set the off duration of the LED
            auto_cancel: Bool
                Close automatically when tapped
            only_alert_once: Bool
                Set this flag if you would only like the sound, vibrate and
                ticker to be played if the notification is not already showing
            timeout_after: Long
                Specifies the time at which this notification should be
                canceled, if it is not already canceled.
            sort_key: String
                Set a sort key that orders this notification among other
                notifications from the same package.
            shortcut_id: String
                If this notification is duplicative of a Launcher shortcut,
                sets the id of the shortcut, in case the Launcher wants to hide
                the shortcut.
            sound: String
               Set the Uri of the sound to play.
            vibration_pattern: List of Long
                Set the vibration pattern to use.
            notification_options: Int
                Set the default notification options that will be used.
            actions: List
                A list of actions to handle

            Returns
            --------
            result: Future
                A future that resolves with the builder of the notification
                that was created.

            References
            ----------
            - https://developer.android.com/guide/topics/ui/notifiers/notifications.html
            - https://developer.android.com/training/notify-user/build-notification.html

            """
            if title:
                self.setContentTitle(title)
            if importance:
                self.setPriority(importance)
            if small_icon:
                self.setSmallIcon(small_icon)
            if text:
                self.setContentText(text)
            if sub_text:
                self.setSubText(sub_text)
            if ticker:
                self.setTicker_(ticker)
            if info:
                self.setContentInfo(info)
            if style:
                self.setStyle(style)
            if color:
                self.setColor(color)
            if colorized is not None:
                self.setColorized(bool(colorized))
            if number is not None:
                self.setNumber(int(number))
            if ongoing is not None:
                self.setOngoing(bool(ongoing))
            if only_alert_once is not None:
                self.setOnlyAlertOnce(bool(only_alert_once))
            if local_only is not None:
                self.setLocalOnly(bool(local_only))
            if auto_cancel:
                self.setAutoCancel(bool(auto_cancel))
            if show_when is not None:  # When is shown by default
                self.setShowWhen(bool(show_when))
            if show_stopwatch:
                self.setUsesChronometer(bool(show_stopwatch))
            if show_progress:
                self.setProgress(
                    int(progress_max),
                    int(progress_current),
                    bool(progress_indeterminate),
                )
            if timeout_after:
                self.setTimeoutAfter(int(timeout_after))
            if category:
                self.setCategory(category)
            if group:
                self.setGroup(group)
            if group_summary is not None:
                self.setGroupSummary(bool(group_summary))
            if group_alert_behavior is not None:
                self.setGroupAlertBehavior(int(group_alert_behavior))
            if shortcut_id:
                self.setShortcutId(shortcut_id)
            if large_icon:
                self.setLargeIcon(self.load_bitmap(large_icon))
            if light_color:
                self.setLights(light_color, light_on, light_off)
            if sort_key:
                self.setSortKey(sort_key)
            if sound:
                self.setSound(Uri.parse(sound))
            if vibration_pattern:
                self.setVibrate([int(i) for i in vibration_pattern])
            if badge_icon_type is not None:
                self.setBadgeIconType(int(badge_icon_type))
            if notification_options is not None:
                self.setDefaults(int(notification_options))
            if actions is not None:
                app = AndroidApplication.instance()
                for (action_icon, action_text, action_callback) in actions:
                    action_key = f"com.codelv.enamlnative.Notify{self.__id__}"
                    intent = Intent()
                    intent.setAction(action_key)
                    receiver = BroadcastReceiver.for_action(
                        action_key, action_callback, single_shot=False
                    )
                    self._receivers.append(receiver)
                    self.addAction_(
                        "@mipmap/ic_launcher",
                        action_text,
                        PendingIntent.getBroadcast(app, 0, intent, 0),
                    )

        async def show(self):
            """Build and show this notification"""
            mgr = await NotificationManager.get()
            notificaion_id = await self.build()
            notification = Notification(__id__=notificaion_id)
            mgr.notify(self.__id__, notification)


# Android really messed this one up
class NotificationManager(JavaBridgeObject):
    """Android NotificationManager. Use the `show_notification` and
    `create_channel` class methods.

    """

    IMPORTANCE_NONE = -1000
    IMPORTANCE_MIN = 1
    IMPORTANCE_LOW = 2
    IMPORTANCE_DEFAULT = 3
    IMPORTANCE_HIGH = 4
    IMPORTANCE_MAX = 5

    PRIORITIES = {
        "low": IMPORTANCE_LOW,
        "normal": IMPORTANCE_DEFAULT,
        "high": IMPORTANCE_HIGH,
    }

    #: Holds the singleton instance
    _instance: ClassVar[Optional["NotificationManager"]] = None
    __nativeclass__ = f"{package}.NotificationManagerCompat"

    ACTION_BIND_SIDE_CHANNEL = "android.support.BIND_NOTIFICATION_SIDE_CHANNEL"
    EXTRA_USE_SIDE_CHANNEL = "android.support.useSideChannel"

    cancel = JavaMethod(str, int)
    cancel_ = JavaMethod(int)
    cancelAll = JavaMethod()

    notify = JavaMethod(int, "android.app.Notification")  # type: ignore
    notify_ = JavaMethod(str, int, "android.app.Notification")

    from_ = JavaStaticMethod(Context, returns=f"{package}.NotificationManagerCompat")

    _receivers = List(BroadcastReceiver)

    @classmethod
    def instance(cls) -> Optional["NotificationManager"]:
        """Get an instance of this service if it was already requested.

        You should request it first using `NotificationManager.get()`

        __Example__

            :::python

            await NotificationManager.get()


        """
        return cls._instance

    @classmethod
    async def get(cls) -> "NotificationManager":
        """Acquires the NotificationManager service async."""
        app = AndroidApplication.instance()
        if cls._instance:
            return cls._instance
        obj_id = await cls.from_(app)
        return cls(__id__=obj_id)

    def __init__(self, *args, **kwargs):
        """Force only one instance to exist"""
        cls = self.__class__
        if cls._instance is not None:
            name = cls.__name__
            raise RuntimeError(
                f"Only one instance of {name} can exist! "
                f"Use {name}.instance() instead!"
            )
        super().__init__(*args, **kwargs)
        cls._instance = self

    @classmethod
    async def create_channel(
        cls,
        channel_id: str,
        name: str,
        importance: int = IMPORTANCE_DEFAULT,
        description: str = "",
    ) -> Optional["NotificationChannel"]:
        """Before you can deliver the notification on Android 8.0 and higher,
        you must register your app's notification channel with the system by
        passing an instance of NotificationChannel
        to createNotificationChannel().

        Parameters
        ----------
        channel_id: String-
            Channel ID
        name: String
            Channel name
        importance: Int
            One of the IMPORTANCE levels
        description: String
            Channel description

        Returns
        -------
        channel: NotificationChannel or None
            The channel that was created.

        """
        app = AndroidApplication.instance()
        assert app is not None
        activity = app.activity
        assert activity is not None
        if activity.api_level < 26:
            return None
        channel = NotificationChannel(channel_id, name, importance)
        channel.setDescription(description)
        mgr = await NotificationChannelManager.get()
        mgr.createNotificationChannel(channel)
        return channel

    @classmethod
    def show_notification(cls, channel_id: int, *args, **kwargs):
        """Create and show a Notification. See `Notification.Builder.update`
        for a list of accepted parameters.

        """
        app = AndroidApplication.instance()
        builder = Notification.Builder(app, channel_id)
        builder.update(*args, **kwargs)
        return builder.show()

    @classmethod
    async def cancel_notification(cls, notification_or_id, tag=None):
        """Cancel the notification.

        Parameters
        ----------
        notification_or_id: Notification.Builder or int
            The notification or id of a notification to clear
        tag: String
            The tag of the notification to clear

        """
        mgr = await cls.get()
        if isinstance(notification_or_id, JavaBridgeObject):
            nid = notification_or_id.__id__
        else:
            nid = notification_or_id
        if tag is None:
            mgr.cancel_(nid)
        else:
            mgr.cancel(tag, nid)


class NotificationChannel(JavaBridgeObject):
    """Required for android 26 and up."""

    __nativeclass__ = "android.app.NotificationChannel"
    __signature__ = [str, "java.lang.CharSequence", int]
    setGroup = JavaMethod(str)
    setLightColor = JavaMethod("android.graphics.Color")
    setBypassDnd = JavaMethod(bool)
    setDescription = JavaMethod(str)
    setImportance = JavaMethod(int)
    setName = JavaMethod("java.lang.CharSequence")
    showBadge = JavaMethod(bool)

    setVibrationPattern = JavaMethod("J[")


class NotificationChannelManager(SystemService):
    SERVICE_TYPE = Context.NOTIFICATION_SERVICE
    __nativeclass__ = "android.app.NotificationChannelManager"

    # This is not in the docs
    createNotificationChannel = JavaMethod(NotificationChannel)


class AndroidNotification(AndroidToolkitObject, ProxyNotification):
    """An Android implementation of an Enaml ProxyNotification."""

    #: A reference to the widget created by the proxy.
    builder = Typed(Notification.Builder)

    #: Keep track of
    shown = Bool()

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """The notification is created in init_layout"""
        pass

    def init_layout(self):
        """Create the notification in the top down pass if show = True"""
        d = self.declaration
        self.create_notification()
        if d.show:
            self.set_show(d.show)

    def destroy(self):
        """A reimplemented destructor that cancels
        the notification before destroying.

        """
        builder = self.builder

        async def cancel_notification():
            await NotificationManager.cancel_notification(builder)
            del self.builder

        deferred_call(cancel_notification)
        super().destroy()

    # -------------------------------------------------------------------------
    # Notification API
    # -------------------------------------------------------------------------
    def create_notification(self):
        """Instead of the typical create_widget we use `create_notification`
        because after it's closed it needs created again.
        """
        d = self.declaration
        builder = self.builder = Notification.Builder(self.get_context(), d.channel_id)
        d = self.declaration

        # Apply any custom settings
        if d.settings:
            builder.update(**d.settings)

        for k, v in self.get_declared_items():
            handler = getattr(self, f"set_{k}")
            handler(v)

        builder.setSmallIcon(d.icon or "@mipmap/ic_launcher")
        # app = self.get_context()
        # intent = Intent()
        # intent.setClass(app, )
        # builder.setContentIntent(PendingIntent.getActivity(app, 0, intent, 0))

        #: Set custom content if present
        for view in self.child_widgets():
            builder.setCustomContentView(view)
            break

    def get_declared_items(self):
        """Get the members that were set in the enamldef block for this
        Declaration.

        Returns
        -------
        result: List of (k,v) pairs that were defined for this widget in enaml
            List of keys and values

        """
        d = self.declaration
        engine = d._d_engine
        if engine:
            for k, h in engine._handlers.items():
                # Handlers with read operations
                if not h.read_pair:
                    continue
                v = getattr(d, k)
                if k in ("show", "icon", "settings"):
                    continue  # We set these explicitly
                yield (k, v)

    def refresh(self):
        """If the"""
        if self.shown:
            self.builder.show()

    # -------------------------------------------------------------------------
    # ProxyNotification API
    # -------------------------------------------------------------------------
    def set_channel_id(self, channel_id):
        self.builder.setChannelId(channel_id)
        self.refresh()

    def set_color(self, color):
        self.builder.setColor(color)
        self.refresh()

    def set_title(self, title):
        self.builder.setContentTitle(title)
        self.refresh()

    def set_info(self, info):
        self.builder.setContentInfo(info)
        self.refresh()

    def set_text(self, text):
        self.builder.setContentText(text)
        self.refresh()

    def set_sub_text(self, sub_text):
        self.builder.setSubText(sub_text)
        self.refresh()

    def set_priority(self, priority):
        self.builder.setPriority(Notification.PRIORITIES[priority])
        self.refresh()

    def set_show_progress(self, show):
        self.set_progress(self.declaration.progress)

    def set_show_when(self, show):
        self.builder.setShowWhen(show)

    def set_progress(self, progress):
        d = self.declaration
        if d.show_progress:
            self.builder.setProgress(100, progress, d.progress_indeterminate)
        else:
            self.builder.setProgress(0, 0, False)
        self.refresh()

    def set_progress_indeterminate(self, indeterminate):
        self.set_progress(self.declaration.progress)

    def set_style(self, style):
        self.builder.setStyle(style)
        self.refresh()

    def set_settings(self, settings):
        self.builder.update(**settings)
        self.refresh()

    def set_show(self, show):
        if show:
            self.shown = True
            self.builder.show()
        else:
            self.shown = False
            NotificationManager.cancel_notification(self.builder)

            # Androids destroys it so create a new one
            self.create_notification()
