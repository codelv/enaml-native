"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import set_default
from .app import AndroidApplication
from .bridge import JavaMethod, JavaBridgeObject, JavaStaticMethod
from .android_content import SystemService, Context


class ArrayList(JavaBridgeObject):
    __nativeclass__ = set_default('java.util.ArrayList')
    add = JavaMethod('int', 'java.lang.Object')
    addAll = JavaMethod('java.util.Collection')
    remove = JavaMethod('int')
    removeAll = JavaMethod('java.util.Collection')
    clear = JavaMethod()


class Executor(JavaBridgeObject):
    __nativeclass__ = set_default('java.util.concurrent.Executor')
    execute = JavaMethod('java.lang.Runnable')


class Executors(JavaBridgeObject):
    __nativeclass__ = set_default('java.util.concurrent.Executors')
    newSingleThreadExecutor = JavaStaticMethod(
        returns='java.util.concurrent.Executor')


class ColorDrawable(JavaBridgeObject):
    __nativeclass__ = set_default('android.graphics.drawable.ColorDrawable')
    __signature__ = set_default(('android.graphics.Color',))


class InputMethodManager(SystemService):
    SERVICE_TYPE = Context.INPUT_METHOD_SERVICE
    __nativeclass__ = set_default(
        'android.view.inputmethod.InputMethodManager')

    toggleSoftInput = JavaMethod('int', 'int', returns='boolean')
    hideSoftInputFromWindow = JavaMethod('android.os.IBinder', 'int',
                                         returns='boolean')

    HIDE_IMPLICIT_ONLY = 1
    SHOW_FORCED = 2

    @classmethod
    def toggle_keyboard(cls, flag=HIDE_IMPLICIT_ONLY):
        """ Toggle the keyboard on and off
         
        Parameters
        ----------
            flag: int
                Flag to send to toggleSoftInput
         
        Returns
        --------
            result: future
                Resolves when the toggle is complete
        
        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_ready(ims):
            ims.toggleSoftInput(flag, 0)
            f.set_result(True)

        cls.get().then(on_ready)
        return f

    @classmethod
    def hide_keyboard(cls):
        """ Hide keyboard if it's open
         
        Returns
        --------
            result: future
                Resolves when the hide is complete
        
        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_ready(ims):
            view = app.view.proxy.widget

            def on_token(__id__):
                ims.hideSoftInputFromWindow(
                    JavaBridgeObject(__id__=__id__), 0).then(f.set_result)
            view.getWindowToken().then(on_token)

        cls.get().then(on_ready)
        return f


class Uri(JavaBridgeObject):
    __nativeclass__ = set_default('android.net.Uri')
    parse = JavaStaticMethod('java.lang.String', returns='android.net.Uri')


class Handler(JavaBridgeObject):
    __nativeclass__ = set_default('android.os.Handler')
    __signature__ = set_default(('android.os.Looper',))


class HandlerThread(JavaBridgeObject):
    __nativeclass__ = set_default('android.os.HandlerThread')
    __signature__ = set_default(('java.lang.String',))
    getLooper = JavaMethod(returns='android.os.Looper')
    getThreadId = JavaMethod('int')
    quit = JavaMethod(returns='boolean')
    quitSafely = JavaMethod(returns='boolean')
    run = JavaMethod()
    join = JavaMethod()
    interrupt = JavaMethod()
    start = JavaMethod()
