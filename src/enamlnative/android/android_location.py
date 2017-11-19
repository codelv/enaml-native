"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Sept 5, 2017

@author: jrm
"""
import re
from atom.api import Atom, List, Float, Unicode, set_default

from .bridge import JavaBridgeObject, JavaCallback, JavaMethod, JavaProxy
from .android_activity import Activity
from .app import AndroidApplication


class LocationAccessDenied(RuntimeError):
    """ User denied access or it's disabled by the system """


class Location(Atom):
    """ A helper class for parsing locations from a string """
    lat = Float()
    lng = Float()
    accuracy = Float()
    altitude = Float()
    time = Unicode()

    source = Unicode()

    def _observe_source(self, change):
        """ Parse source into the fields """
        src = self.source
        m = re.search(
            r'Location\[gps (-?\d+\.?\d*),(-?\d+\.?\d*)'
            r' acc=(\d+\.?\d*) et=(.+) alt=(\d+\.?\d*) ',
            src
        )
        if m:
            lat, lng, acc, et, alt = m.groups()
            self.lat, self.lng, self.accuracy, self.altitude = (
                float(lat), float(lng), float(acc), float(alt)
            )
            self.time = et


class LocationManager(JavaBridgeObject):
    _instance = None
    __nativeclass__ = set_default('android.location.LocationManager')

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

    requestLocationUpdates = JavaMethod('java.lang.String', 'long', 'float',
                                        'android.location.LocationListener')

    removeUpdates = JavaMethod('android.location.LocationListener')

    class LocationListener(JavaProxy):
        __nativeclass__ = set_default('android.location.LocationListener')

    # -------------------------------------------------------------------------
    # LocationListener API
    # -------------------------------------------------------------------------
    onLocationChanged = JavaCallback('android.location.Location')
    onProviderDisabled = JavaCallback('java.lang.String')
    onProviderEnabled = JavaCallback('java.lang.String')
    onStatusChanged = JavaCallback('java.lang.String', 'int',
                                   'android.os.Bundle')

    #: Active listeners
    listeners = List(LocationListener)

    @classmethod
    def instance(cls):
        """ Get an instance of this service if it was already requested.

        You should request it first using `LocationManager.request()`

        __Example__

            :::python

            def on_manager(lm):
                #: Do stuff with it
                assert lm == LocationManager.instance()

            LocationManager.get().then(on_manager)


        """
        if cls._instance:
            return cls._instance

    @classmethod
    def get(cls):
        """ Acquires the LocationManager service async. 
        
        """

        app = AndroidApplication.instance()
        f = app.create_future()

        if cls._instance:
            app.set_future_result(f, cls._instance)
            return f

        def on_service(obj_id):
            #: Create the manager
            if not LocationManager.instance():
                lm = LocationManager(__id__=obj_id)
            else:
                lm = LocationManager.instance()
            app.set_future_result(f, lm)

        app.get_system_service(Activity.LOCATION_SERVICE).then(on_service)

        return f

    def __init__(self,*args, **kwargs):
        if LocationManager._instance is not None:
            raise RuntimeError(
                "Only one instance of LocationManager can exist! "
                "Use LocationManager.instance() instead!")
        super(LocationManager, self).__init__(*args, **kwargs)
        LocationManager._instance = self

    @classmethod
    def start(cls, callback, provider='gps', min_time=1000, min_distance=0):
        """ Convenience method that checks and requests permission if necessary
        and if successful calls the callback with a populated `Location` 
        instance on updates.

        Note you must have the permissions in your manifest or requests 
        will be denied immediately.

        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_location(loc):
            #: Invoke the callback with the parsed location
            callback(Location(source=loc))

        def on_success(lm):
            #: When we have finally have permission
            lm.onLocationChanged.connect(on_location)

            #: Save a reference to our listener
            #: because we may want to stop updates
            listener = LocationManager.LocationListener(lm)
            lm.listeners.append(listener)

            lm.requestLocationUpdates(provider, min_time, min_distance,
                                      listener)
            app.set_future_result(f, True)

        def on_perm_request_result(allowed):
            #: When our permission request is accepted or decliend.
            if allowed:
                LocationManager.get().then(on_success)
            else:
                #: Access denied
                app.set_future_result(f, False)

        def on_perm_check(allowed):
            if allowed:
                LocationManager.get().then(on_success)
            else:
                LocationManager.request_permission(
                    fine=provider == 'gps').then(on_perm_request_result)

        #: Check permission
        LocationManager.check_permission(
            fine=provider == 'gps').then(on_perm_check)

        return f

    @classmethod
    def stop(cls):
        """ Stops location updates if currently updating.

        """
        manager = LocationManager.instance()
        if manager:
            for l in manager.listeners:
                manager.removeUpdates(l)
            manager.listeners = []


    @classmethod
    def check_permission(cls, fine=True):
        """ Returns a future that returns a boolean indicating if permission 
        is currently granted or denied. If permission is denied, you can 
        request using `LocationManager.request_permission()` below.

        """
        app = AndroidApplication.instance()
        permission = (cls.ACCESS_FINE_PERMISSION
                      if fine else cls.ACCESS_COARSE_PERMISSION)
        return app.has_permission(permission)

    @classmethod
    def request_permission(cls, fine=True):
        """ Requests permission and returns an async result that returns 
        a boolean indicating if the permission was granted or denied. 
        
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
        super(LocationManager, self).__del__()

