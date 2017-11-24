"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Nov 18, 2017

@author: jrm
"""
from atom.api import List, set_default

from .bridge import JavaBridgeObject, JavaMethod, JavaField
from .android_activity import Activity
from .android_content import BroadcastReceiver, IntentFilter
from .app import AndroidApplication


class WifiConfiguration(JavaBridgeObject):
    __nativeclass__ = set_default('android.net.wifi.WifiConfiguration')
    BSSID = JavaField('java.lang.String')
    FQDN = JavaField('java.lang.String')
    SSID = JavaField('java.lang.String')
    hiddenSSID = JavaField('boolean')
    networkId = JavaField('int')
    preSharedKey = JavaField('java.lang.String')
    status = JavaField('int')

    STATUS_CURRENT = 0x0
    STATUS_DISABLED = 0x1
    STATUS_ENABLED = 0x2


class WifiManager(JavaBridgeObject):
    """ Access android's WifiManager. Use the static class methods.
    
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
    _instance = None
    __nativeclass__ = set_default('android.new.wifi.WifiManager')

    PERMISSION_ACCESS_FINE_LOCATION = 'android.permission.' \
                                      'ACCESS_FINE_LOCATION'
    PERMISSION_ACCESS_COARSE_LOCATION = 'android.permission.' \
                                        'ACCESS_COARSE_LOCATION'
    PERMISSION_ACCESS_WIFI_STATE = 'android.permission.ACCESS_WIFI_STATE'
    PERMISSION_CHANGE_WIFI_STATE = 'android.permission.CHANGE_WIFI_STATE'

    PERMISSIONS_REQUIRED = [
        #PERMISSION_ACCESS_FINE_LOCATION,
        PERMISSION_ACCESS_COARSE_LOCATION,
        PERMISSION_ACCESS_WIFI_STATE,
        PERMISSION_CHANGE_WIFI_STATE
    ]

    SCAN_RESULTS_AVAILABLE_ACTION = 'android.net.wifi.SCAN_RESULTS'

    getScanResults = JavaMethod(returns='java.util.List')
    setWifiEnabled = JavaMethod('boolean', returns='boolean')
    isWifiEnabled = JavaMethod(returns='boolean')
    startScan = JavaMethod(returns='boolean')
    reassociate = JavaMethod(returns='boolean')
    reconnect = JavaMethod(returns='boolean')
    removeNetwork = JavaMethod('int', returns='boolean')
    addNetwork = JavaMethod('android.net.wifi.WifiConfiguration',
                            returns='int')
    enableNetwork = JavaMethod('int', 'boolean', returns='boolean')
    _disconnect = JavaMethod(returns='boolean')
    getConnectionInfo = JavaMethod(returns='android.net.wifi.WifiInfo')
    getDhcpInfo = JavaMethod(returns='android.net.DhcpInfo')

    #: List of receivers
    _receivers = List(BroadcastReceiver)

    @classmethod
    def instance(cls):
        """ Get an instance of this service if it was already requested.

        You should request it first using `WifiManager.get()`

        __Example__

            :::python

            def on_manager(m):
                #: Do stuff with it
                assert m == WifiManager.instance()

            WifiManager.get().then(on_manager)


        """
        if cls._instance:
            return cls._instance

    @classmethod
    def get(cls):
        """ Acquires the WifiManager service async. """

        app = AndroidApplication.instance()
        f = app.create_future()

        if cls._instance:
            app.set_future_result(f, cls._instance)
            return f

        def on_service(obj_id):
            #: Create the manager
            if not WifiManager.instance():
                m = WifiManager(__id__=obj_id)
            else:
                m = WifiManager.instance()
            app.set_future_result(f, m)

        app.get_system_service(Activity.WIFI_SERVICE).then(on_service)

        return f

    def __init__(self,*args, **kwargs):
        if WifiManager._instance is not None:
            raise RuntimeError("Only one instance of WifiManager can exist! "
                               "Use WifiManager.instance() instead!")
        super(WifiManager, self).__init__(*args, **kwargs)

        #: Change the name of the _disconnect JavaMethod
        WifiManager._disconnect.set_name('disconnect')

        WifiManager._instance = self

    # -------------------------------------------------------------------------
    # Public api
    # -------------------------------------------------------------------------
    @classmethod
    def is_wifi_enabled(cls):
        """ Check if wifi is currently enabled.
        
        Returns
        --------
            result: future
              A future that resolves with the value.

        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_permission_result(result):
            if not result:
                f.set_result(None)
                return

            def on_ready(m):
                m.isWifiEnabled().then(f.set_result)

            WifiManager.get().then(on_ready)

        #: Check permission
        cls.request_permission([
            WifiManager.PERMISSION_ACCESS_WIFI_STATE
        ]).then(on_permission_result)
        return f

    @classmethod
    def set_wifi_enabled(cls, state=True):
        """ Set the wifi enabled state.
        
        Returns
        --------
            result: future
              A future that resolves with whether the operation succeeded.

        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_permission_result(result):
            if not result:
                #: Permission denied
                f.set_result(None)
                return

            def on_ready(m):
                m.setWifiEnabled(state).then(f.set_result)

            WifiManager.get().then(on_ready)

        #: Check permission
        cls.request_permission([
            WifiManager.PERMISSION_CHANGE_WIFI_STATE
        ]).then(on_permission_result)
        return f

    @classmethod
    def get_networks(cls):
        """ Get the wifi networks currently available. 
        
        Returns
        --------
            result: future
                A future that resolves with the list of networks available
                or None if wifi could not be enabled (permission denied,
                etc...)

        """
        app = AndroidApplication.instance()
        activity = app.widget
        f = app.create_future()

        def on_permission_result(result):
            if not result:
                f.set_result(None)
                return

            def on_ready(mgr):
                #: Register a receiver so we know when the scan
                #: is complete
                receiver = BroadcastReceiver()
                receiver.setReceiver(receiver.getId())

                def on_scan_complete(context, intent):
                    #: Finally, pull the scan results
                    mgr.getScanResults().then(f.set_result)

                    #: Cleanup receiver
                    mgr._receivers.remove(receiver)
                    activity.unregisterReceiver(receiver)

                def on_wifi_enabled(enabled):
                    if not enabled:
                        #: Access denied or failed to enable
                        f.set_result(None)

                        #: Cleanup receiver
                        mgr._receivers.remove(receiver)
                        activity.unregisterReceiver(receiver)
                        return

                    #: Hook up a callback that's fired when the scan
                    #: results are ready
                    receiver.onReceive.connect(on_scan_complete)

                    #: Save a reference as this must stay alive
                    mgr._receivers.append(receiver)

                    #: Register the receiver
                    intent_filter = IntentFilter(
                        WifiManager.SCAN_RESULTS_AVAILABLE_ACTION)
                    activity.registerReceiver(receiver,
                                              intent_filter)

                    #: Trigger a scan (which "should" eventually
                    #: call the on on_scan_complete)
                    mgr.startScan()

                #: Enable if needed
                mgr.setWifiEnabled(True).then(on_wifi_enabled)

            #: Get the service
            WifiManager.get().then(on_ready)

        #: Request permissions
        cls.request_permission(
            WifiManager.PERMISSIONS_REQUIRED).then(on_permission_result)

        return f

    @classmethod
    def disconnect(cls):
        """ Disconnect from the current network (if connected).
         
         Returns
         --------
             result: future
                 A future that resolves to true if the disconnect was 
                 successful. Will be set to None if the change network 
                 permission is denied.
 
        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_permission_result(result):
            if not result:
                f.set_result(None)
                return

            def on_ready(mgr):
                mgr.disconnect().then(f.set_result)

            #: Get the service
            WifiManager.get().then(on_ready)

        #: Request permissions
        cls.request_permission([
            WifiManager.PERMISSION_CHANGE_WIFI_STATE
        ]).then(on_permission_result)

        return f

    @classmethod
    def connect(cls, ssid, key=None, **kwargs):
        """ Connect to the given ssid using the key (if given).
        
        Returns
        --------
            result: future
                A future that resolves with the result of the connect

        """
        app = AndroidApplication.instance()
        f = app.create_future()

        config = WifiConfiguration()
        config.SSID = '"{}"'.format(ssid)
        if key is not None:
            config.preSharedKey = '"{}"'.format(key)

        #: Set any other parameters
        for k, v in kwargs.items():
            setattr(config, k, v)

        def on_permission_result(result):
            if not result:
                f.set_result(None)
                return

            def on_ready(mgr):

                def on_disconnect(result):
                    if not result:
                        f.set_result(None)
                        return  #: Done
                    mgr.setWifiEnabled(True).then(on_wifi_enabled)

                def on_wifi_enabled(enabled):
                    if not enabled:
                        #: Access denied or failed to enable
                        f.set_result(None)
                        return
                    mgr.addNetwork(config).then(on_network_added)

                def on_network_added(net_id):
                    if net_id == -1:
                        f.set_result(False)
                        print("Warning: Invalid network "
                              "configuration id {}".format(net_id))
                        return
                    mgr.enableNetwork(net_id, True).then(on_network_enabled)

                def on_network_enabled(result):
                    if not result:
                        #: TODO: Should probably say
                        #: which state it failed at...
                        f.set_result(None)
                        return

                    mgr.reconnect().then(f.set_result)

                #: Enable if needed
                mgr._disconnect().then(on_disconnect)

            #: Get the service
            WifiManager.get().then(on_ready)

        #: Request permissions
        cls.request_permission(
            WifiManager.PERMISSIONS_REQUIRED).then(on_permission_result)
        return f

    @classmethod
    def get_connection_info(cls):
        """ Get info about current wifi connection (if any). Returns
        info such as the IP address, BSSID, link speed, signal, etc.. 
         
         Returns
         --------
             result: future
                 A future that resolves with a dict of the connection info
                 or None if an error occurred (ie permission denied).s
 
         """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_permission_result(result):
            if not result:
                f.set_result(None)
                return

            def on_ready(mgr):
                mgr.getConnectionInfo().then(f.set_result)

            #: Get the service
            WifiManager.get().then(on_ready)

        #: Request permissions
        cls.request_permission([
            WifiManager.PERMISSION_ACCESS_WIFI_STATE
        ]).then(on_permission_result)

        return f

    @classmethod
    def get_dhcp_info(cls):
        """ Get info about current DHCP configuration such as DNS servers,
        IP address, and lease duration.
         
        Returns
        --------
             result: future
                 A future that resolves with a dict of the DHCP info
                 or None if an error occured (ie permission denied).s
 
        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_permission_result(result):
            if not result:
                f.set_result(None)
                return

            def on_ready(mgr):
                mgr.getDhcpInfo().then(f.set_result)

            #: Get the service
            WifiManager.get().then(on_ready)

        #: Request permissions
        cls.request_permission([
            WifiManager.PERMISSION_ACCESS_WIFI_STATE
        ]).then(on_permission_result)

        return f

    @classmethod
    def request_permission(cls, permissions):
        """ Requests permission and returns an future result that returns a 
        boolean indicating if all the given permission were granted or denied.
         
        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_result(perms):
            allowed = True
            for p in permissions:
                allowed = allowed and perms.get(p, False)
            f.set_result(allowed)

        app.request_permissions(permissions).then(on_result)

        return f

    def __del__(self):
        """ Remove any receivers before destroying """
        app = AndroidApplication.instance()
        activity = app.widget
        for r in self._receivers:
            activity.unregisterReceiver(r)
        super(WifiManager, self).__del__()

