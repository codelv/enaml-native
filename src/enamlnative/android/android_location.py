"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Sept 5, 2017

@author: jrm
"""
from atom.api import List
from .android_content import Context, SystemService
from .app import AndroidApplication
from .bridge import JavaCallback, JavaMethod, JavaProxy


class LocationAccessDenied(RuntimeError):
    """User denied access or it's disabled by the system"""


class LocationManager(SystemService):
    SERVICE_TYPE = Context.LOCATION_SERVICE
    __nativeclass__ = "android.location.LocationManager"

    ACCESS_FINE_PERMISSION = "android.permission.ACCESS_FINE_LOCATION"
    ACCESS_COARSE_PERMISSION = "android.permission.ACCESS_COARSE_LOCATION"

    GPS_PROVIDER = "gps"
    NETWORK_PROVIDER = "network"
    PASSIVE_PROVIDER = "passive"

    PROVIDERS = {
        "gps": GPS_PROVIDER,
        "network": NETWORK_PROVIDER,
        "passive": PASSIVE_PROVIDER,
    }

    requestLocationUpdates = JavaMethod(
        "java.lang.String", "long", "float", "android.location.LocationListener"
    )

    removeUpdates = JavaMethod("android.location.LocationListener")

    class LocationListener(JavaProxy):
        __nativeclass__ = "android.location.LocationListener"

    # -------------------------------------------------------------------------
    # LocationListener API
    # -------------------------------------------------------------------------
    onLocationChanged = JavaCallback("android.location.Location")
    onProviderDisabled = JavaCallback("java.lang.String")
    onProviderEnabled = JavaCallback("java.lang.String")
    onStatusChanged = JavaCallback("java.lang.String", "int", "android.os.Bundle")

    #: Active listeners
    listeners = List(LocationListener)

    @classmethod
    async def start(cls, callback, provider="gps", min_time=1000, min_distance=0):
        """Convenience method that checks and requests permission if necessary
        and if successful calls the callback with a populated `Location`
        instance on updates.

        Note you must have the permissions in your manifest or requests
        will be denied immediately.

        """
        request_fine = provider == "gps"
        has_perm = await LocationManager.check_permission(fine=request_fine)

        if not has_perm:
            has_perm = await LocationManager.request_permission(fine=request_fine)

        if not has_perm:
            raise RuntimeError("Location permission denied")
        mgr = await LocationManager.get()

        #: When we have finally have permission
        mgr.onLocationChanged.connect(callback)

        #: Save a reference to our listener
        #: because we may want to stop updates
        listener = LocationManager.LocationListener(mgr)
        mgr.listeners.append(listener)
        mgr.requestLocationUpdates(provider, min_time, min_distance, listener)

    @classmethod
    def stop(cls):
        """Stops location updates if currently updating."""
        manager = LocationManager.instance()
        if manager is not None:
            for listener in manager.listeners:
                manager.removeUpdates(listener)
            manager.listeners = []

    @classmethod
    async def check_permission(cls, fine=True) -> bool:
        """Returns a future that returns a boolean indicating if permission
        is currently granted or denied. If permission is denied, you can
        request using `LocationManager.request_permission()` below.

        """
        app = AndroidApplication.instance()
        if fine:
            permission = cls.ACCESS_FINE_PERMISSION
        else:
            permission = cls.ACCESS_COARSE_PERMISSION
        return await app.has_permission(permission)

    @classmethod
    async def request_permission(cls, fine=True) -> bool:
        """Requests permission and returns an async result that returns
        a boolean indicating if the permission was granted or denied.

        """
        app = AndroidApplication.instance()
        if fine:
            permission = cls.ACCESS_FINE_PERMISSION
        else:
            permission = cls.ACCESS_COARSE_PERMISSION
        perms = await app.request_permissions(permission)
        return perms.get(permission)

    def __del__(self):
        """Remove any listeners before destroying"""
        self.stop()
        super().__del__()
