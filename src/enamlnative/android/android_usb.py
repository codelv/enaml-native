"""
Copyright (c) 2017-2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Feb 11, 2018

@author: jrm
"""
from asyncio import Future
from atom.api import Dict, List, Typed, Event
from .android_content import (
    BroadcastReceiver,
    Context,
    SystemService,
    PendingIntent,
    IntentFilter,
    Intent,
)
from .android_utils import HashMap
from .bridge import JavaBridgeObject, JavaMethod


class UsbInterface(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbInterface"


class UsbConfiguration(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbConfiguration"


class UsbDevice(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbDevice"
    info = Dict()
    getDeviceName = JavaMethod(returns=str)
    getDeviceId = JavaMethod(returns=int)
    getInterface = JavaMethod(int, returns=UsbInterface)
    getConfiguration = JavaMethod(int, returns=UsbConfiguration)


class UsbDeviceConnection(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbDeviceConnection"
    close = JavaMethod()


class UsbAccessory(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbAccessory"


class UsbManager(SystemService):
    """Use UsbManger.get().then(on_ready) to get an instance."""

    __nativeclass__ = "android.hardware.usb.UsbManager"

    EXTRA_PERMISSION_GRANTED = "permission"
    EXTRA_DEVICE = "device"
    ACTION_USB_PERMISSION = "com.codelv.enamlnative.USB_PERMISSION"
    SERVICE_TYPE = Context.USB_SERVICE

    getAccessoryList = JavaMethod(returns="android.hardware.usb.UsbAccessory[")
    getDeviceList = JavaMethod(returns=HashMap)
    openAccessory = JavaMethod(UsbAccessory, returns="android.os.ParcelFileDescriptor")
    openDevice = JavaMethod(UsbDevice, returns=UsbDeviceConnection)
    hasPermission = JavaMethod(UsbDevice, returns=bool)
    requestPermission = JavaMethod(UsbDevice, PendingIntent)

    #: These names are changed to support both signatures
    hasPermission_ = JavaMethod(UsbAccessory, returns=bool)
    requestPermission_ = JavaMethod(UsbAccessory, PendingIntent)

    receiver = Typed(BroadcastReceiver)
    permission_intent = Typed(PendingIntent)
    allowed_devices = Dict(int, UsbDevice)
    pending_requests = List(Future)

    #: You can listen for this
    device_connected = Event(UsbDevice)

    def _default_receiver(self):
        return BroadcastReceiver.for_action(
            UsbManager.ACTION_USB_PERMISSION, self.on_device_connected
        )

    def _default_permission_intent(self):
        app = self.__app__
        assert app is not None
        d = app.activity
        assert d is not None
        proxy = d.proxy
        assert proxy is not None
        activity = proxy.widget
        assert activity is not None
        intent_filter = IntentFilter(UsbManager.ACTION_USB_PERMISSION)
        intent = Intent(UsbManager.ACTION_USB_PERMISSION)
        intent_id = PendingIntent.getBroadcast(activity, 0, intent, 0)
        activity.registerReceiver(self.receiver, intent_filter)
        return PendingIntent(__id__=intent_id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Overridden to make sure it's listening
        assert self.permission_intent is not None

    async def on_device_connected(self, ctx, intent):
        """Invoked when the receiver fires"""
        app = self.__app__
        assert app is not None
        action = await intent.getAction()
        if action != UsbManager.ACTION_USB_PERMISSION:
            return

        dev_id = await intent.getParcelableExtra(UsbManager.EXTRA_DEVICE)
        allowed = await intent.getBooleanExtra(
            UsbManager.EXTRA_PERMISSION_GRANTED, False
        )
        print("USB Device connected")
        try:
            if allowed and dev_id:
                device = UsbDevice(__id__=dev_id)
                self.device_connected(device)
                for f in self.pending_requests:
                    f.set_result(device)
            else:
                err = PermissionError("Access to USB device denied")
                for f in self.pending_requests:
                    f.set_exception(err)
        finally:
            self.clean_pending()

    def clean_pending(self):
        pending = self.pending_requests
        for f in pending[:]:
            if f.done():
                try:
                    pending.remove(f)
                except ValueError:
                    pass

    async def request_permission(self, device: UsbDevice) -> bool:
        if device.__id__ in self.allowed_devices:
            return True
        permission_intent = self.permission_intent
        assert permission_intent is not None
        app = self.__app__
        assert app is not None
        f = app.create_future()
        self.pending_requests.append(f)
        self.requestPermission(device, permission_intent)
        return await f
