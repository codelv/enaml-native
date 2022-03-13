"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Nov 18, 2017
"""
from atom.api import List
from .android_activity import Activity
from .android_content import BroadcastReceiver, IntentFilter, SystemService
from .app import AndroidApplication
from .bridge import JavaBridgeObject, JavaField, JavaMethod


class WifiConfiguration(JavaBridgeObject):
    __nativeclass__ = "android.net.wifi.WifiConfiguration"
    BSSID = JavaField(str)
    FQDN = JavaField(str)
    SSID = JavaField(str)
    hiddenSSID = JavaField(bool)
    networkId = JavaField(int)
    preSharedKey = JavaField(str)
    status = JavaField(int)

    STATUS_CURRENT = 0x0
    STATUS_DISABLED = 0x1
    STATUS_ENABLED = 0x2


class WifiManager(SystemService):
    """Access android's WifiManager. Use the static class methods.

    To Get networks use:

        WifiManager.get_networks().then(on_results)

    It will request and enable if wifi allowed. Returns None if access is
    denied otherwise the list of networks.

    To check if wifi is enabled use:

        WifiManager.is_wifi_enabled().then(on_result)

    Returns None if access is denied otherwise the result


    To set wifi enabled use:

        WifiManager.set_wifi_enabled(state=True).then(on_result)

    Returns None if access is denied otherwise the result

    """

    SERVICE_TYPE = Activity.WIFI_SERVICE
    __nativeclass__ = "android.new.wifi.WifiManager"

    PERMISSION_ACCESS_FINE_LOCATION = "android.permission." "ACCESS_FINE_LOCATION"
    PERMISSION_ACCESS_COARSE_LOCATION = "android.permission." "ACCESS_COARSE_LOCATION"
    PERMISSION_ACCESS_WIFI_STATE = "android.permission.ACCESS_WIFI_STATE"
    PERMISSION_CHANGE_WIFI_STATE = "android.permission.CHANGE_WIFI_STATE"

    PERMISSIONS_REQUIRED = [
        # PERMISSION_ACCESS_FINE_LOCATION,
        PERMISSION_ACCESS_COARSE_LOCATION,
        PERMISSION_ACCESS_WIFI_STATE,
        PERMISSION_CHANGE_WIFI_STATE,
    ]

    SCAN_RESULTS_AVAILABLE_ACTION = "android.net.wifi.SCAN_RESULTS"

    getScanResults = JavaMethod(returns="java.util.List")
    setWifiEnabled = JavaMethod(bool, returns=bool)
    isWifiEnabled = JavaMethod(returns=bool)
    startScan = JavaMethod(returns=bool)
    reassociate = JavaMethod(returns=bool)
    reconnect = JavaMethod(returns=bool)
    removeNetwork = JavaMethod(int, returns=bool)
    addNetwork = JavaMethod("android.net.wifi.WifiConfiguration", returns=int)
    enableNetwork = JavaMethod(int, bool, returns=bool)
    disconnect_ = JavaMethod(returns=bool)
    getConnectionInfo = JavaMethod(returns="android.net.wifi.WifiInfo")
    getDhcpInfo = JavaMethod(returns="android.net.DhcpInfo")

    #: List of receivers
    _receivers = List(BroadcastReceiver)

    # -------------------------------------------------------------------------
    # Public api
    # -------------------------------------------------------------------------
    @classmethod
    async def is_wifi_enabled(cls) -> bool:
        """Check if wifi is currently enabled.

        Returns
        --------
            result: bool
              Whether wifi is enabled

        """
        has_perm = await WifiManager.request_permission(
            WifiManager.PERMISSION_ACCESS_WIFI_STATE
        )

        if not has_perm:
            raise RuntimeError("Wifi permission denied")

        mgr = await WifiManager.get()
        return await mgr.isWifiEnabled()

    @classmethod
    async def set_wifi_enabled(cls, state: bool = True) -> bool:
        """Set the wifi enabled state.

        Returns
        --------
            enabled: bool
              Whether the operation succeeded.

        """
        allowed = await WifiManager.request_permission(
            WifiManager.PERMISSION_CHANGE_WIFI_STATE
        )
        if not allowed:
            raise RuntimeError("Permission to change wifi state is not allowed")

        mgr = await WifiManager.get()
        return await mgr.setWifiEnabled(state)

    @classmethod
    async def get_networks(cls):
        """Get the wifi networks currently available.

        Returns
        --------
            result: future
                A future that resolves with the list of networks available
                or None if wifi could not be enabled (permission denied,
                etc...)

        """
        app = AndroidApplication.instance()
        allowed = await WifiManager.request_permission(
            *WifiManager.PERMISSIONS_REQUIRED
        )
        if not allowed:
            raise RuntimeError("Permission to get networks is not allowed")

        mgr = await WifiManager.get()

        # Enable if needed
        enabled = await mgr.setWifiEnabled(True)
        if not enabled:
            raise RuntimeError("Could not enable wifi")

        # Register a receiver so we know when the scan
        # is complete
        receiver = BroadcastReceiver()
        receiver.setReceiver(receiver.getId())

        scan_results = app.create_future()

        def on_scan_ready(f):
            scan_results.set_result(f.result())

        def on_scan_complete(context, intent):
            # Finally, pull the scan results
            mgr.getScanResults().add_done_callback(on_scan_ready)

        # Hook up a callback that's fired when the scan
        # results are ready
        receiver.onReceive.connect(on_scan_complete)

        # Register the receiver
        intent_filter = IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION)
        activity = app.widget
        activity.registerReceiver(receiver, intent_filter)
        try:
            # Trigger a scan which "should" eventually call on_scan_complete
            mgr.startScan()
            return await scan_results
        finally:
            activity.unregisterReceiver(receiver)

    @classmethod
    async def disconnect(cls):
        """Disconnect from the current network (if connected).

        Returns
        --------
            result: future
                A future that resolves to true if the disconnect was
                successful. Will be set to None if the change network
                permission is denied.

        """
        allowed = await WifiManager.request_permission(
            WifiManager.PERMISSION_CHANGE_WIFI_STATE
        )
        if not allowed:
            raise RuntimeError("Permission to toggle wifi state not allowed")
        mgr = await WifiManager.get()
        return await mgr.disconnect()

    @classmethod
    async def connect(cls, ssid, key=None, **kwargs):
        """Connect to the given ssid using the key (if given).

        Returns
        --------
            result: future
                A future that resolves with the result of the connect

        """
        allowed = await WifiManager.request_permission(
            *WifiManager.PERMISSIONS_REQUIRED
        )
        if not allowed:
            raise RuntimeError("Permission to toggle wifi state not allowed")

        config = WifiConfiguration()
        config.SSID = f'"{ssid}"'
        if key is not None:
            config.preSharedKey = f'"{ssid}"'

        #: Set any other parameters
        for k, v in kwargs.items():
            setattr(config, k, v)

        mgr = await WifiManager.get()

        #: Enable if needed
        disconnected = await mgr.disconnect_()
        if not disconnected:
            raise RuntimeError("Could not disconnect wifi")

        enabled = await mgr.setWifiEnabled(True)
        if not enabled:
            raise RuntimeError("Could not enable wifi")

        net_id = await mgr.addNetwork(config)
        if net_id == -1:
            raise ValueError("Warning: Invalid network configuration")

        net_enabled = await mgr.enableNetwork(net_id, True)
        if not net_enabled:
            raise RuntimeError("Could not enable network")
        return await mgr.reconnect()

    @classmethod
    async def get_connection_info(cls):
        """Get info about current wifi connection (if any). Returns
        info such as the IP address, BSSID, link speed, signal, etc..

         Returns
         --------
        result: future
            A future that resolves with a dict of the connection info
            or None if an error occurred (ie permission denied).

        """
        allowed = await WifiManager.request_permission(
            WifiManager.PERMISSION_ACCESS_WIFI_STATE
        )

        if not allowed:
            raise RuntimeError("Access wifi state permission not allowed")
        mgr = await WifiManager.get()
        return await mgr.getConnectionInfo()

    @classmethod
    async def get_dhcp_info(cls):
        """Get info about current DHCP configuration such as DNS servers,
        IP address, and lease duration.

        Returns
        --------
             result: future
                 A future that resolves with a dict of the DHCP info
                 or None if an error occured (ie permission denied).s

        """
        allowed = await WifiManager.request_permission(
            WifiManager.PERMISSION_ACCESS_WIFI_STATE
        )
        if not allowed:
            raise RuntimeError("Access wifi state permission not allowed")
        mgr = await WifiManager.get()
        return await mgr.getDhcpInfo()

    @classmethod
    async def request_permission(cls, *permissions) -> bool:
        """Requests permission and returns an future result that returns a
        boolean indicating if all the given permission were granted or denied.

        """
        app = AndroidApplication.instance()
        perms = await app.request_permissions(*permissions)
        for p in permissions:
            if not perms.get(p, False):
                return False
        return True

    def __del__(self):
        """Remove any receivers before destroying"""
        app = AndroidApplication.instance()
        activity = app.widget
        for r in self._receivers:
            activity.unregisterReceiver(r)
        super().__del__()
