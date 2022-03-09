"""
Copyright (c) 2017-2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 24, 2017


"""

from typing import ClassVar, Union
from atom.api import Str
from .bridge import JavaBridgeObject, JavaCallback, JavaMethod, JavaStaticMethod


class IntentFilter(JavaBridgeObject):
    __nativeclass__ = "android.content.IntentFilter"
    __signature__ = [str]


class Context(JavaBridgeObject):
    __nativeclass__ = "android.content.Context"

    #: Broadcast receiver
    registerReceiver = JavaMethod("android.content.BroadcastReceiver", IntentFilter)
    sendBroadcast = JavaMethod("")
    unregisterReceiver = JavaMethod("android.content.BroadcastReceiver")

    startService = JavaMethod("android.content.Intent")
    stopService = JavaMethod("android.content.Intent")
    unbindService = JavaMethod(
        "android.content.Intent", "android.content.ServiceConnection", int
    )
    unbindService = JavaMethod("android.content.ServiceConnection")

    #: Get system services
    getSystemService = JavaMethod(str, returns=object)

    ACCESSIBILITY_SERVICE = "accessibility"
    ACCOUNT_SERVICE = "account"
    ACTIVITY_SERVICE = "activity"
    ALARM_SERVICE = "alarm"
    APPWIDGET_SERVICE = "appwidget"
    APP_OPS_SERVICE = "appops"
    AUDIO_SERVICE = "audio"
    BATTERY_SERVICE = "battery"
    BLUETOOTH_SERVICE = "bluetooth"
    CAMERA_SERVICE = "camera"
    CAPTIONING_SERVICE = "captioning"
    CARRIER_CONFIG_SERVICE = "carrier_config"
    CLIPBOARD_SERVICE = "clipboard"
    CONNECTIVITY_SERVICE = "connectivity"
    CONSUMER_IR_SERVICE = "consumer_ir"
    DEVICE_POLICY_SERVICE = "device_policy"
    DISPLAY_SERVICE = "display"
    DOWNLOAD_SERVICE = "download"
    DROPBOX_SERVICE = "dropbox"
    FINGERPRINT_SERVICE = "fingerprint"
    HARDWARE_PROPERTIES_SERVICE = "hardware_properties"
    INPUT_METHOD_SERVICE = "input_method"
    INPUT_SERVICE = "input"
    JOB_SCHEDULER_SERVICE = "jobscheduler"
    KEYGUARD_SERVICE = "keyguard"
    LAUNCHER_APPS_SERVICE = "launcherapps"
    LAYOUT_INFLATER_SERVICE = "layout_inflater"
    LOCATION_SERVICE = "location"
    MEDIA_PROJECTION_SERVICE = "media_projection"
    MEDIA_ROUTER_SERVICE = "media_router"
    MEDIA_SESSION_SERVICE = "media_session"
    MIDI_SERVICE = "midi"
    NETWORK_STATS_SERVICE = "netstats"
    NFC_SERVICE = "nfc"
    NOTIFICATION_SERVICE = "notification"
    NSD_SERVICE = "servicediscovery"
    POWER_SERVICE = "power"
    PRINT_SERVICE = "print"
    RESTRICTIONS_SERVICE = "restrictions"
    SEARCH_SERVICE = "search"
    SENSOR_SERVICE = "sensor"
    SHORTCUT_SERVICE = "shortcut"
    STORAGE_SERVICE = "storage"
    SYSTEM_HEALTH_SERVICE = "systemhealth"
    TELECOM_SERVICE = "telecom"
    TELEPHONY_SERVICE = "telephony"
    TELEPHONY_SUBSCRIPTION_SERVICE = "telephony_subscription_service"
    TEXT_SERVICES_MANAGER_SERVICE = "textservices"
    TV_INPUT_SERVICE = "tv_input"
    UI_MODE_SERVICE = "uimode"
    USAGE_STATS_SERVICE = "usagestats"
    USB_SERVICE = "usb"
    USER_SERVICE = "user"
    VIBRATOR_SERVICE = "vibrator"
    WALLPAPER_SERVICE = "wallpaper"
    WIFI_P2P_SERVICE = "wifi_p2p"
    WIFI_SERVICE = "wifi"
    WINDOW_SERVICE = "window"

    SERVICES = {
        "accessibility": ACCESSIBILITY_SERVICE,
        "account": ACCOUNT_SERVICE,
        "activity": ACTIVITY_SERVICE,
        "alarm": ALARM_SERVICE,
        "appwidget": APPWIDGET_SERVICE,
        "appops": APP_OPS_SERVICE,
        "audio": AUDIO_SERVICE,
        "battery": BATTERY_SERVICE,
        "bluetooth": BLUETOOTH_SERVICE,
        "camera": CAMERA_SERVICE,
        "captioning": CAPTIONING_SERVICE,
        "carrier_config": CARRIER_CONFIG_SERVICE,
        "clipboard": CLIPBOARD_SERVICE,
        "connectivity": CONNECTIVITY_SERVICE,
        "consumer_ir": CONSUMER_IR_SERVICE,
        "device_policy": DEVICE_POLICY_SERVICE,
        "display": DISPLAY_SERVICE,
        "download": DOWNLOAD_SERVICE,
        "dropbox": DROPBOX_SERVICE,
        "fingerprint": FINGERPRINT_SERVICE,
        "hardware_properties": HARDWARE_PROPERTIES_SERVICE,
        "input_method": INPUT_METHOD_SERVICE,
        "input": INPUT_SERVICE,
        "jobscheduler": JOB_SCHEDULER_SERVICE,
        "keyguard": KEYGUARD_SERVICE,
        "launcherapps": LAUNCHER_APPS_SERVICE,
        "layout_inflater": LAYOUT_INFLATER_SERVICE,
        "location": LOCATION_SERVICE,
        "media_projection": MEDIA_PROJECTION_SERVICE,
        "media_router": MEDIA_ROUTER_SERVICE,
        "media_session": MEDIA_SESSION_SERVICE,
        "midi_service": MIDI_SERVICE,
        "netstats": NETWORK_STATS_SERVICE,
        "nfc": NFC_SERVICE,
        "notification": NOTIFICATION_SERVICE,
        "servicediscovery": NSD_SERVICE,
        "power": POWER_SERVICE,
        "print": PRINT_SERVICE,
        "restrictions": RESTRICTIONS_SERVICE,
        "search": SEARCH_SERVICE,
        "sensor": SENSOR_SERVICE,
        "shortcut": SHORTCUT_SERVICE,
        "storage": STORAGE_SERVICE,
        "systemhealth": SYSTEM_HEALTH_SERVICE,
        "telecom": TELECOM_SERVICE,
        "telephony": TELEPHONY_SERVICE,
        "telephony_subscription_service": TELEPHONY_SUBSCRIPTION_SERVICE,
        "textservices": TEXT_SERVICES_MANAGER_SERVICE,
        "tv_input": TV_INPUT_SERVICE,
        "uimode": UI_MODE_SERVICE,
        "usagestats": USAGE_STATS_SERVICE,
        "usb": USB_SERVICE,
        "user": USER_SERVICE,
        "vibrator": VIBRATOR_SERVICE,
        "wallpaper": WALLPAPER_SERVICE,
        "wifip2p": WIFI_P2P_SERVICE,
        "wifi": WIFI_SERVICE,
        "window": WINDOW_SERVICE,
    }


class Intent(JavaBridgeObject):
    __nativeclass__ = "android.content.Intent"
    action = Str()
    context = Str()
    setAction = JavaMethod(str)
    getAction = JavaMethod(returns=str)
    setClass = JavaMethod(Context, "java.lang.Class")
    putExtra = JavaMethod(str, str)
    getParcelableExtra = JavaMethod(str, returns=object)
    getBooleanExtra = JavaMethod(str, bool, returns=bool)


class PendingIntent(JavaBridgeObject):
    __nativeclass__ = "android.app.PendingIntent"
    getActivity = JavaStaticMethod(
        Context,
        int,
        Intent,
        int,
        returns="android.app.PendingIntent",
    )
    getService = JavaStaticMethod(
        Context,
        int,
        Intent,
        int,
        returns="android.app.PendingIntent",
    )
    getBroadcast = JavaStaticMethod(
        Context,
        int,
        Intent,
        int,
        returns="androind.app.PendingIntent",
    )

    cancel = JavaMethod()
    describeContents = JavaMethod(returns=int)


class BroadcastReceiver(JavaBridgeObject):
    """A BroadcastReceiver that delegates to a listener"""

    __nativeclass__ = "com.codelv.enamlnative.adapters.BridgeBroadcastReceiver"

    setReceiver = JavaMethod(
        "com.codelv.enamlnative.adapters.BridgeBroadcastReceiver$Receiver"
    )

    #: Delegate receiver callback
    onReceive = JavaCallback(Context, Intent)

    @classmethod
    def for_action(
        cls, actions: Union[str, list[str]], callback, single_shot: bool = True
    ):
        """Create a BroadcastReceiver that is invoked when the given
        action is received.

        Parameters
        ----------
        action: Union[str, list[str]]
            Action or list of actions to receive
        callback: Callable
            Callback to invoke when the action is received
        single_shot: Bool
            Cleanup after one callback

        Returns
        -------
            receiver: BroadcastReceiver
                The receiver that was created. You must hold on to this
                or the GC will clean it up.

        """
        receiver = cls()
        receiver.setReceiver(receiver.getId())

        app = receiver.__app__
        assert app is not None
        d = app.activity
        assert d is not None
        proxy = d.proxy
        assert proxy is not None
        activity = proxy.widget
        assert activity is not None

        def on_receive(ctx, data: dict):
            # The bridge sends the intent as a dict with keys id, action, and url
            if single_shot:
                activity.unregisterReceiver(receiver)
            intent = Intent(
                __id__=data["id"],
                action=data["action"],
                context=data["context"],
            )
            assert app is not None
            app.deferred_call(callback, ctx, intent)

        receiver.onReceive.connect(on_receive)
        if isinstance(actions, str):
            actions = [actions]
        for action in actions:
            activity.registerReceiver(receiver, IntentFilter(action))
        return receiver

    def __del__(self):
        """Unregister automatically"""
        activity = self.__app__.activity.proxy.widget
        activity.unregisterReceiver(self)
        super().__del__()


class SystemService(JavaBridgeObject):
    """A common api for system services as singletons"""

    SERVICE_TYPE: ClassVar[str] = ""
    _instance = None

    @classmethod
    def instance(cls):
        """Get an instance of this service if it was already requested.

        You should request it first using `UsbManager.get()`

        __Example__

            :::python

            mgr = await UsbManager.get()


        """
        return cls._instance

    @classmethod
    async def get(cls):
        """Acquires the WifiManager service async."""
        from .app import AndroidApplication

        app = AndroidApplication.instance()
        return await app.get_system_service(cls)

    def __init__(self, *args, **kwargs):
        """Force only one instance to exist"""
        cls = self.__class__
        if cls._instance is not None:
            service_name = cls.__name__
            raise RuntimeError(
                f"Only one instance of {service_name} can exist! "
                f"Use {service_name}.instance() instead!"
            )
        super().__init__(*args, **kwargs)
        cls._instance = self
