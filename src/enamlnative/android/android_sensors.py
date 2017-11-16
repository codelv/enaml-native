"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Sept 24, 2017

@author: jrm
"""
import re
from atom.api import Atom, List, Float, Unicode, set_default

from .bridge import JavaBridgeObject, JavaCallback, JavaMethod, JavaProxy
from .android_activity import Activity
from .app import AndroidApplication


class SensorAccessDenied(RuntimeError):
    """ User denied acccess or it's disabled by the system """


class Sensor(Atom):
    """ A helper class for parsing locations from a string """
    pass

class SensorManager(JavaBridgeObject):
    _instance = None
    __nativeclass__ = set_default('android.location.SensorManager')

    ACCESS_FINE_PERMISSION = 'android.permission.ACCESS_FINE_LOCATION'
    ACCESS_COARSE_PERMISSION = 'android.permission.ACCESS_COARSE_LOCATION'

    GPS_PROVIDER = 'gps'
    NETWORK_PROVIDER = 'network'
    PASSIVE_PROVIDER = 'passive'

    PROVIDERS = {
        'gps': GPS_PROVIDER,
        'network': NETWORK_PROVIDER,
        'passive': PASSIVE_PROVIDER,
    }

    requestSensorUpdates = JavaMethod('java.lang.String', 'long', 'float',
                                        'android.location.SensorListener')

    removeUpdates = JavaMethod('android.location.SensorListener')

    class SensorListener(JavaProxy):
        __nativeclass__ = set_default('android.location.SensorListener')

    onSensorChanged = JavaCallback('android.location.Sensor')
    onProviderDisabled = JavaCallback('java.lang.String')
    onProviderEnabled = JavaCallback('java.lang.String')
    onStatusChanged = JavaCallback('java.lang.String', 'int', 'android.os.Bundle')

    #: Active listeners
    listeners = List(SensorListener)


    @classmethod
    def instance(cls):
        """ Get an instance of this service if it was already requested.

        You should request it first using `SensorManager.request()`

        __Example__

            :::python

            def on_manager(lm):
                #: Do stuff with it
                assert lm == SensorManager.instance()

            SensorManager.get().then(on_manager)


        """
        if cls._instance:
            return cls._instance

    @classmethod
    def get(cls):
        """ Acquires the SensorManager service async. """

        app = AndroidApplication.instance()
        f = app.create_future()

        if cls._instance:
            app.set_future_result(f, cls._instance)
            return f

        def on_service(obj_id):
            #: Create the manager
            if not SensorManager.instance():
                lm = SensorManager(__id__=obj_id)
            else:
                lm = SensorManager.instance()
            app.set_future_result(f, lm)

        app.get_system_service(Activity.LOCATION_SERVICE).then(on_service)

        return f

    def __init__(self,*args, **kwargs):
        if SensorManager._instance is not None:
            raise RuntimeError("Only one instance of SensorManager can exist! "
                               "Use SensorManager.instance() instead!")
        super(SensorManager, self).__init__(*args, **kwargs)
        SensorManager._instance = self

    @classmethod
    def start(cls, callback, provider='gps', min_time=1000, min_distance=0):
        """ Convenience method that checks and requests permission if necessary
        and if successful calls the callback with a populated `Sensor` 
        instance on updates.

        Note you must have the permissions in your manifest or requests 
        will be denied immediately.

        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_location(loc):
            #: Invoke the callback with the parsed location
            callback(Sensor(source=loc))

        def on_success(lm):
            #: When we have finally have permission
            lm.onSensorChanged.connect(on_location)

            #: Save a reference to our listener
            #: because we may want to stop updates
            listener = SensorManager.SensorListener(lm)
            lm.listeners.append(listener)

            lm.requestSensorUpdates(provider, min_time, min_distance, listener)
            app.set_future_result(f, True)

        def on_perm_request_result(allowed):
            #: When our permission request is accepted or decliend.
            if allowed:
                SensorManager.get().then(on_success)
            else:
                #: Access denied
                app.set_future_result(f, False)

        def on_perm_check(allowed):
            if allowed:
                SensorManager.get().then(on_success)
            else:
                SensorManager.request_permission(
                    fine=provider == 'gps').then(on_perm_request_result)

        #: Check permission
        SensorManager.check_permission(
            fine=provider == 'gps').then(on_perm_check)

        return f

    @classmethod
    def stop(self):
        """ Stops location updates if currently updating.

        """
        manager = SensorManager.instance()
        if manager:
            for l in manager.listeners:
                manager.removeUpdates(l)
            manager.listeners = []


    @classmethod
    def check_permission(cls, fine=True):
        """ Returns a future that returns a boolean indicating if permission 
        is currently granted or denied. If permission is denied, you can 
        request using`SensorManager.request_permission()` below.

        """
        app = AndroidApplication.instance()
        permission = (cls.ACCESS_FINE_PERMISSION
                      if fine else cls.ACCESS_COARSE_PERMISSION)
        return app.has_permission(permission)

    @classmethod
    def request_permission(cls, fine=True):
        """ Requests permission and returns an async result that returns a 
        boolean indicating if the permission was granted or denied. 
        
        """
        app = AndroidApplication.instance()
        permission = (cls.ACCESS_FINE_PERMISSION
                      if fine else cls.ACCESS_COARSE_PERMISSION)
        f = app.create_future()

        def on_result(perms):
            app.set_future_result(f, perms[permission])

        app.request_permissions([permission]).then(on_result)

        return f

    def __del__(self):
        """ Remove any listeners before destroying """
        self.stop()
        super(SensorManager, self).__del__()

