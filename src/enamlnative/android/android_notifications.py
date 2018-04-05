"""
Copyright (c) 2017-2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Apr 4, 2018

@author: jrm
"""
from atom.api import ForwardInstance, Int, set_default

from .bridge import (
    JavaBridgeObject, JavaStaticMethod, JavaCallback, JavaMethod
)
from .app import AndroidApplication
from .android_content import Context, SystemService

class Notification(JavaBridgeObject):
    """ A wrapper for an Android's notification apis
    
    """
    __nativeclass__ = set_default('android.support.v4.app.NotificationCompat')

    class Builder(JavaBridgeObject):
        """ Builds a notification.
        
        Notes
        ------
        The constructor automatically sets the when field to 
        System.currentTimeMillis() and the audio stream to the STREAM_DEFAULT.
        
        """
        __nativeclass__ = set_default(
            'android.support.v4.app.NotificationCompat$Builder')
        __signature__ = set_default(('android.content.Context',
                                     'java.lang.String'))
        addAction = JavaMethod(
            'android.support.v4.app.NotificationCompat$Action')
        addAction_ = JavaMethod('int', 'java.lang.CharSequence',
                                'android.app.PendingIntent')
        addInvisibleAction = JavaMethod(
            'android.support.v4.app.NotificationCompat$Action')
        addInvisibleAction_ = JavaMethod('int', 'java.lang.CharSequence',
                                         'android.app.PendingIntent')
        addPerson = JavaMethod('java.lang.String')

        build = JavaMethod(returns='android.app.Notification')

        setAutoCancel = JavaMethod('boolean')
        setBadgeIconType = JavaMethod('android.R')
        setCategory = JavaMethod('java.lang.String')
        setChannelId = JavaMethod('java.lang.String')
        setColor = JavaMethod('android.graphics.Color')
        setColorized = JavaMethod('boolean')
        setContent = JavaMethod('android.widget.RemoteViews')
        setContentInfo = JavaMethod('java.lang.CharSequence')
        setContentIntent = JavaMethod('android.app.PendingIntent')
        setContentText = JavaMethod('java.lang.CharSequence')
        setContentTitle = JavaMethod('java.lang.CharSequence')
        setCustomBigContentView = JavaMethod('android.widget.RemoteViews')
        setCustomContentView = JavaMethod('android.widget.RemoteViews')
        setCustomHeadsUpContentView = JavaMethod('android.widget.RemoteViews')
        setDefaults = JavaMethod('int')
        setDeleteIntent = JavaMethod('android.app.PendingIntent')
        setExtras = JavaMethod('android.os.Bundle')
        setFullScreenIntent = JavaMethod('android.app.PendingIntent',
                                         'boolean')

        setGroup = JavaMethod('java.lang.String')
        setGroupAlertBehavior = JavaMethod('int')
        setGroupSummary = JavaMethod('boolean')
        setLargeIcon = JavaMethod('android.graphics.Bitmap')
        setLights = JavaMethod('android.graphics.Color', 'int', 'int')
        setLocalOnly = JavaMethod('boolean')
        setNumber = JavaMethod('int')
        setOngoing = JavaMethod('boolean')
        setOnlyAlertOnce = JavaMethod('boolean')
        setPriority = JavaMethod('int')
        setProgress = JavaMethod('int', 'int', 'boolean')
        setPublicVersion = JavaMethod('android.app.Notification')
        setRemoteInputHistory = JavaMethod('Landroid.app.Notification;[')
        setShortcutId = JavaMethod('java.lang.String')
        setShowWhen = JavaMethod('boolean')
        setSmallIcon = JavaMethod('android.R')
        setSmallIcon_ = JavaMethod('android.R', 'int')
        setSortKey = JavaMethod('java.lang.String')
        setSound = JavaMethod('android.net.Uri')
        setSound_ = JavaMethod('android.net.Uri', 'int')
        setStyle = JavaMethod(
            'android.support.v4.app.NotificationCompat$Style')
        setSubText = JavaMethod('java.lang.CharSequence')
        setTicker = JavaMethod('java.lang.CharSequence',
                               'android.widget.RemoteViews')
        setTicker_ = JavaMethod('java.lang.CharSequence')
        setTimeoutAfter = JavaMethod('long')
        setUsesChronometer = JavaMethod('boolean')
        setVibrate = JavaMethod('J[')
        setVisibility = JavaMethod('int')
        setWhen = JavaMethod('long')


class NotificationChannel(JavaBridgeObject):
    """ Required for android 26 and up. """
    __nativeclass__ = set_default('android.app.NotificationChannel')
    __signature__ = set_default(('java.lang.String',
                                 'java.lang.CharSequence',
                                 'int'))
    setGroup = JavaMethod('java.lang.String')
    setLightColor = JavaMethod('android.graphics.Color')
    setBypassDnd = JavaMethod('boolean')
    setDescription = JavaMethod('java.lang.String')
    setImportance = JavaMethod('int')
    setName = JavaMethod('java.lang.CharSequence')
    showBadge = JavaMethod('boolean')

    setVibrationPattern = JavaMethod('J[')


class NotificationChannelManager(SystemService):
    SERVICE_TYPE = Context.NOTIFICATION_SERVICE
    __nativeclass__ = set_default('android.app.NotificationManager')

    # This is not in the docs
    createNotificationChannel = JavaMethod('android.app.NotificationChannel')


# Android really messed this one up
class NotificationManager(JavaBridgeObject):
    __nativeclass__ = set_default(
        'android.support.v4.app.NotificationManagerCompat')

    ACTION_BIND_SIDE_CHANNEL = "android.support.BIND_NOTIFICATION_SIDE_CHANNEL"
    EXTRA_USE_SIDE_CHANNEL = "android.support.useSideChannel"

    IMPORTANCE_NONE = -1000
    IMPORTANCE_MIN = 1
    IMPORTANCE_LOW = 2
    IMPORTANCE_DEFAULT = 3
    IMPORTANCE_HIGH = 4
    IMPORTANCE_MAX = 5

    cancel = JavaMethod('java.lang.String', 'int')
    cancel_ = JavaMethod('int')
    cancelAll = JavaMethod()

    notify = JavaMethod('int', 'android.app.Notification')
    notify_ = JavaMethod('java.lang.String', 'int', 'android.app.Notification')

    from_ = JavaStaticMethod(
        'android.content.Context',
        returns='android.support.v4.app.NotificationManagerCompat')

    @classmethod
    def create_channel(cls, channel_id, name, importance=IMPORTANCE_DEFAULT,
                       description=""):
        """ Before you can deliver the notification on Android 8.0 and higher, 
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
        if app.api_level >= 26:
            channel = NotificationChannel(channel_id, name, importance)
            channel.setDescription(description)

            NotificationChannelManager.get().then(
                lambda mgr: mgr.createNotificationChannel(channel))

            return channel

    @classmethod
    def show_notification(cls, channel_id, title, text,
                          importance=IMPORTANCE_DEFAULT,
                          small_icon="@mipmap/ic_launcher",
                          auto_cancel=True):
        """ Show a simple notification
        
        Parameters
        ----------
        channel_id: String
            The id of the channel this notification is displayed on
        title: String
            The title text
        text: String
            The description text
        importance: Int
            The importance or priority of the notification
        small_icon: String
            A resource identifier
        auto_cancel: Bool
            Close automatically when tapped
        actions: List
            A list of actions to handle

        """
        app = AndroidApplication.instance()
        f = app.create_future()
        b = Notification.Builder(app, channel_id)
        b.setContentTitle(title)
        b.setContentText(text)
        b.setPriority(importance)
        b.setSmallIcon(small_icon)
        if auto_cancel:
            b.setAutoCancel(auto_cancel)
        # for (action_icon, action_text, action_callback) in actions:
        #     intent = Intent()
        #     intent.setAction()
        #     pending_intent = PendingIntent.getBroadcast(app, 0, intent, 0)
        #     b.addAction(action_icon, action_text, pending_intent)

        # Build and show it
        def on_ready(__id__, notification):
            mgr = NotificationManager(__id__=__id__)
            mgr.notify(notification.__id__, notification)
            f.set_result(True)

        def on_built(__id__):
            n = Notification(__id__=__id__)
            cls.from_(app).then(
                lambda __id__, n=n: on_ready(__id__, n))
        b.build().then(on_built)
        return f
