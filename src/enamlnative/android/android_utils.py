"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017


"""
from .android_content import Context, SystemService
from .app import AndroidApplication
from .bridge import JavaBridgeObject, JavaMethod, JavaStaticMethod


class HashMap(JavaBridgeObject):
    __nativeclass__ = "java.util.HashMap"
    get = JavaMethod(object, returns=object)
    set = JavaMethod(object, object)


class AttributeSet(JavaBridgeObject):
    __nativeclass__ = "android.util.AttributeSet"


class ArrayList(JavaBridgeObject):
    __nativeclass__ = "java.util.ArrayList"
    add = JavaMethod(int, object)
    addAll = JavaMethod("java.util.Collection")
    remove = JavaMethod(int)
    removeAll = JavaMethod("java.util.Collection")
    clear = JavaMethod()


class Executor(JavaBridgeObject):
    __nativeclass__ = "java.util.concurrent.Executor"
    execute = JavaMethod("java.lang.Runnable")


class Executors(JavaBridgeObject):
    __nativeclass__ = "java.util.concurrent.Executors"
    newSingleThreadExecutor = JavaStaticMethod(returns="java.util.concurrent.Executor")


class ColorDrawable(JavaBridgeObject):
    __nativeclass__ = "android.graphics.drawable.ColorDrawable"
    __signature__ = ["android.graphics.Color"]


class InputMethodManager(SystemService):
    SERVICE_TYPE = Context.INPUT_METHOD_SERVICE
    __nativeclass__ = "android.view.inputmethod.InputMethodManager"

    toggleSoftInput = JavaMethod(int, int, returns=bool)
    hideSoftInputFromWindow = JavaMethod("android.os.IBinder", int, returns=bool)

    HIDE_IMPLICIT_ONLY = 1
    SHOW_FORCED = 2

    @classmethod
    async def toggle_keyboard(cls, flag=HIDE_IMPLICIT_ONLY):
        """Toggle the keyboard on and off

        Parameters
        ----------
            flag: int
                Flag to send to toggleSoftInput

        Returns
        --------
            result: future
                Resolves when the toggle is complete

        """
        ims = await cls.get()
        return ims.toggleSoftInput(flag, 0)

    @classmethod
    async def hide_keyboard(cls):
        """Hide keyboard if it's open

        Returns
        --------
            result: future
                Resolves when the hide is complete

        """
        ims = await cls.get()
        app = AndroidApplication.instance()
        view = app.activity.proxy.view
        obj_id = await view.getWindowToken()
        token = JavaBridgeObject(__id__=obj_id)
        return await ims.hideSoftInputFromWindow(token, 0)


class Uri(JavaBridgeObject):
    __nativeclass__ = "android.net.Uri"
    parse = JavaStaticMethod(str, returns="android.net.Uri")


class Handler(JavaBridgeObject):
    __nativeclass__ = "android.os.Handler"
    __signature__ = ["android.os.Looper"]


class HandlerThread(JavaBridgeObject):
    __nativeclass__ = "android.os.HandlerThread"
    __signature__ = [str]
    getLooper = JavaMethod(returns="android.os.Looper")
    getThreadId = JavaMethod(int)
    quit = JavaMethod(returns=bool)
    quitSafely = JavaMethod(returns=bool)
    run = JavaMethod()
    join = JavaMethod()
    interrupt = JavaMethod()
    start = JavaMethod()
