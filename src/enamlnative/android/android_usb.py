"""
Copyright (c) 2017-2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Feb 11, 2018

@author: jrm
"""
from atom.api import Dict
from .android_content import Context, SystemService
from .bridge import JavaBridgeObject, JavaMethod


class UsbDevice(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbDevice"
    info = Dict()
    getDeviceName = JavaMethod(returns="java.lang.String")
    getDeviceId = JavaMethod(returns="int")
    getInterface = JavaMethod("int", returns="android.hardware.usb.UsbInterface")
    getConfiguration = JavaMethod(
        "int", returns="android.hardware.usb.UsbConfiguration"
    )


class UsbDeviceConnection(JavaBridgeObject):
    __nativeclass__ = "android.hardware.usb.UsbDeviceConnection"
    close = JavaMethod()


class UsbManager(SystemService):
    """Use UsbManger.get().then(on_ready) to get an instance."""

    SERVICE_TYPE = Context.USB_SERVICE
    __nativeclass__ = "android.hardware.usb.UsbManager"

    getAccessoryList = JavaMethod(returns="android.hardware.usb.UsbAccessory[")
    getDeviceList = JavaMethod(returns="java.util.HashMap")
    openAccessory = JavaMethod(
        "android.hardware.usb.UsbAccessory", returns="android.os.ParcelFileDescriptor"
    )
    openDevice = JavaMethod(
        "android.hardware.usb.UsbDevice",
        returns="android.hardware.usb.UsbDeviceConnection",
    )
    hasPermission = JavaMethod("android.hardware.usb.UsbDevice", returns="boolean")
    requestPermission = JavaMethod(
        "android.hardware.usb.UsbDevice", "android.app.PendingIntent"
    )

    #: These names are changed to support both signatures
    hasPermission_ = JavaMethod("android.hardware.usb.UsbAccessory", returns="boolean")
    requestPermission_ = JavaMethod(
        "android.hardware.usb.UsbAccessory", "android.app.PendingIntent"
    )
