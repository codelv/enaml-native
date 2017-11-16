"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 24, 2017

@author: jrm
"""

from atom.api import Atom, Int, set_default
from .bridge import JavaMethod, JavaCallback
from .android_content import Context


class Activity(Context):
    """ Access to the activity over the bridge """
    #: As long as the user subclasses the EnamlActivity
    #: everything in this class will work
    __nativeclass__ = set_default('com.codelv.enamlnative.EnamlActivity')

    #: ID of -1 is a special reference on the bridge to the activity.
    __id__ = Int(-1)

    #: Tracing methods
    startTrace = JavaMethod('java.lang.String')
    stopTrace = JavaMethod('java.lang.String')
    resetBridgeStats = JavaMethod()

    setView = JavaMethod('android.view.View')
    showLoading = JavaMethod('java.lang.String')
    setActionBar = JavaMethod('android.widget.Toolbar')
    setSupportActionBar = JavaMethod('android.support.v7.widget.Toolbar')
    setContentView = JavaMethod('android.view.View')
    getWindow = JavaMethod(returns='android.view.Window')

    getSupportFragmentManager = JavaMethod(
        returns='android.support.v4.app.FragmentManager')
    getBuildInfo = JavaMethod(returns='java.lang.HashMap')

    #: Permissions
    checkSelfPermission = JavaMethod('java.lang.String', returns='int')
    requestPermissions = JavaMethod('[Ljava.lang.String;', 'int')
    onRequestPermissionsResult = JavaCallback('int', '[Ljava.lang.String;',
                                              '[Lint;')

    #: Method added so we can listen externally
    setPermissionResultListener = JavaMethod(
        'com.codelv.enamlnative.EnamlActivity$PermissionResultListener')

    PERMISSION_GRANTED = 0
    PERMISSION_DENIED = -1

    #: Activity results
    addActivityResultListener = JavaMethod(
        'com.codelv.enamlnative.EnamlActivity$ActivityResultListener')
    removeActivityResultListener = JavaMethod(
        'com.codelv.enamlnative.EnamlActivity$ActivityResultListener')
    onActivityResult = JavaCallback('int', 'int', 'android.content.Intent',
                                    returns='boolean')

    #: Activity lifecycle listener
    addActivityLifecycleListener = JavaMethod(
        'com.codelv.enamlnative.EnamlActivity$ActivityLifecycleListener')
    removeActivityLifecycleListener = JavaMethod(
        'com.codelv.enamlnative.EnamlActivity$ActivityLifecycleListener')
    #: Called with the lifecycle state like 'pause', 'resume', etc...
    onActivityLifecycleChanged = JavaCallback('java.lang.String')

