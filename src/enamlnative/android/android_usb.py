"""
Copyright (c) 2017-2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Feb 11, 2018

@author: jrm
"""
import os
from asyncio import Future
from atom.api import Dict, Int, List, Typed, Event, Value
from .android_content import (
    BroadcastReceiver,
    Context,
    SystemService,
    PendingIntent,
    Intent,
)
from .android_utils import HashMap
from .bridge import JavaBridgeObject, JavaMethod


def find_library(lib: str) -> str:
    """ Locate a library with of the given name """
    lib_dir = os.environ['PY_LIB_DIR']
    path = f'{lib_dir}/{lib}.so'
    if os.path.exists(path):
        return path
    return ''


def libusb_init(self, lib):
    """ Patch pyusb's libusb1 backend to work on android """
    from usb.backend import IBackend, libusb1
    from ctypes import POINTER, c_void_p, c_int, byref
    IBackend.__init__(self)
    self.lib = lib
    self.ctx = c_void_p()
    NO_DEVICE_DISCOVERY = 2
    try:
        _check = libusb1._check
        lib.libusb_wrap_sys_device.argtypes = [
            c_void_p, c_void_p, POINTER(c_void_p)
        ]
        lib.libusb_wrap_sys_device.restype = c_int
        lib.libusb_get_device.argtypes = [c_void_p]
        lib.libusb_get_device.restype = c_void_p

        _check(self.lib.libusb_set_option(None, NO_DEVICE_DISCOVERY, None))
        _check(self.lib.libusb_init(byref(self.ctx)))
        assert self.ctx
    except Exception as e:
        print(e)
        raise


def load_libusb():
    """ Apply a patch to pyusb and load the libusb1 backend

    """
    # Patch ctypes find_library to look in the correct location
    # import ctypes.util
    # ctypes.util.find_library = find_library

    # Patch the LibUSB init to disable device discovery
    from usb.backend import libusb1
    libusb1._LibUSB.__init__ = libusb_init
    return libusb1.get_backend(find_library)


class UsbEndpoint(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbEndpoint"
    getAddress = JavaMethod(returns=int)
    getAttributes = JavaMethod(returns=int)
    getDirection = JavaMethod(returns=int)
    getEndpointNumber = JavaMethod(returns=int)
    getInterval = JavaMethod(returns=int)
    getMaxPacketSize = JavaMethod(returns=int)


class UsbInterface(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbInterface"
    getAlternateSetting = JavaMethod(returns=int)
    getEndpoint = JavaMethod(int, returns=UsbEndpoint)
    getEndpointCount = JavaMethod(returns=int)
    getId = JavaMethod(returns=int)
    getInterfaceClass = JavaMethod(returns=int)
    getInterfaceProtocol = JavaMethod(returns=int)
    getInterfaceSubclass = JavaMethod(returns=int)
    getName = JavaMethod(returns=str)


class UsbConfiguration(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbConfiguration"


class UsbRequest(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbRequest"
    cancel = JavaMethod()
    close = JavaMethod()
    getClientData = JavaMethod(returns=object)
    getEndpoint = JavaMethod(returns=UsbEndpoint)
    initialize = JavaMethod(lambda: UsbDeviceConnection, UsbEndpoint)
    queue = JavaMethod("java.nio.ByteBuffer")
    setClientData = JavaMethod(object)


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
    getFileDescriptor = JavaMethod(returns=int)
    getSerial = JavaMethod(returns=str)
    claimInterface = JavaMethod(UsbInterface, bool, returns=bool)
    releaseInterface = JavaMethod(UsbInterface, returns=bool)
    setInterface = JavaMethod(UsbInterface, returns=bool)
    setConfiguration = JavaMethod(UsbConfiguration, returns=bool)
    bulkTransfer = JavaMethod(UsbEndpoint, "[B", int, int)
    bulkTransfer_ = JavaMethod(UsbEndpoint, "[B", int, int, int)
    getRawDescriptors = JavaMethod(returns="[B")

    requestWait = JavaMethod("long", returns=UsbRequest)

    # Internal ctypes handles so this can be used with pyusb
    devid = Value()
    handle = Value()

    async def acquire(self):
        """ Acquire a pyusb device for this connection.

        """
        from ctypes import c_void_p, byref
        from usb.core import Device
        from usb.backend import libusb1

        fd = await self.getFileDescriptor()

        backend = load_libusb()
        self.handle = c_void_p()
        libusb1._check(backend.lib.libusb_wrap_sys_device(
            backend.ctx, fd, byref(self.handle)
        ))
        self.devid = backend.lib.libusb_get_device(self.handle)
        return Device(self, backend)


class UsbAccessory(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbAccessory"


class UsbManager(SystemService):
    """Use UsbManger.get().then(on_ready) to get an instance."""

    __nativeclass__ = "android.hardware.usb.UsbManager"

    EXTRA_PERMISSION_GRANTED = "permission"
    EXTRA_DEVICE = "device"
    ACTION_USB_PERMISSION = "com.codelv.enamlnative.USB_PERMISSION"
    ACTION_USB_DEVICE_ATTACHED = "android.hardware.usb.action.USB_DEVICE_ATTACHED"
    ACTION_USB_DEVICE_DETACHED = "android.hardware.usb.action.USB_DEVICE_DETACHED"
    ACTION_USB_ACCESSORY_ATTACHED = (
        "android.hardware.usb.action.ACTION_USB_ACCESSORY_ATTACHED"
    )
    ACTION_USB_ACCESSORY_DETACHED = (
        "android.hardware.usb.action.ACTION_USB_ACCESSORY_DETACHED"
    )
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
    device_attached = Event(UsbDevice)
    device_detached = Event(UsbDevice)

    def _default_receiver(self):
        return BroadcastReceiver.for_action(
            [
                UsbManager.ACTION_USB_PERMISSION,
                UsbManager.ACTION_USB_DEVICE_ATTACHED,
                UsbManager.ACTION_USB_DEVICE_DETACHED,
            ],
            self.on_device_action_received,
            single_shot=False,
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
        intent = Intent(UsbManager.ACTION_USB_PERMISSION)
        intent_id = PendingIntent.getBroadcast(activity, 0, intent, 0)
        return PendingIntent(__id__=intent_id)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Overridden to make sure it's listening
        assert self.receiver is not None
        assert self.permission_intent is not None

    async def on_device_action_received(self, ctx, intent: Intent):
        """Invoked when the receiver fires"""
        app = self.__app__
        assert app is not None
        # The bridge sends the intent as a dict
        action = intent.action
        if action == UsbManager.ACTION_USB_PERMISSION:
            await self.on_device_permssion_result(ctx, intent)
        elif action == UsbManager.ACTION_USB_DEVICE_ATTACHED:
            await self.on_device_attached(ctx, intent)
        elif action == UsbManager.ACTION_USB_DEVICE_DETACHED:
            await self.on_device_detached(ctx, intent)

    async def on_device_permssion_result(self, ctx, intent: Intent):
        info = await intent.getParcelableExtra(UsbManager.EXTRA_DEVICE)
        allowed = await intent.getBooleanExtra(
            UsbManager.EXTRA_PERMISSION_GRANTED, False
        )
        try:
            if allowed and info:
                device = UsbDevice(__id__=info["id"], info=info)
                for f in self.pending_requests:
                    f.set_result(device)
            else:
                err = PermissionError("Access to USB device denied")
                for f in self.pending_requests:
                    f.set_exception(err)
        finally:
            self.clean_pending()

    async def on_device_attached(self, ctx, intent: Intent):
        info = await intent.getParcelableExtra(UsbManager.EXTRA_DEVICE)
        if info:
            dev = UsbDevice(__id__=info["id"], info=info)
            self.device_attached(dev)  # type: ignore

    async def on_device_detached(self, ctx, intent: Intent):
        info = await intent.getParcelableExtra(UsbManager.EXTRA_DEVICE)
        if info:
            dev = UsbDevice(__id__=info["id"], info=info)
            self.device_detached(dev)  # type: ignore

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
