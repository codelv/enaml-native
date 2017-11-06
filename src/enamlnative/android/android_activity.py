'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on July 24, 2017

@author: jrm
'''

from atom.api import Atom, Int, set_default
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class Activity(JavaBridgeObject):
    """ Access to the activity over the bridge """
    __nativeclass__ = set_default('com.codelv.enamlnative.EnamlActivity')
    __id__ = Int(-1) #: ID of -1 is a special reference on the bridge to the activity.

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

    getSupportFragmentManager = JavaMethod(returns='android.support.v4.app.FragmentManager')
    getBuildInfo = JavaMethod(returns='java.lang.HashMap')

    #: Permissions
    checkSelfPermission = JavaMethod('java.lang.String', returns='int')
    requestPermissions = JavaMethod('[Ljava.lang.String;', 'int')
    onRequestPermissionsResult = JavaCallback('int', '[Ljava.lang.String;', '[Lint;')

    #: Method added so we can listen externally
    setPermissionResultListener = JavaMethod('com.codelv.enamlnative.EnamlActivity$PermissionResultListener')

    PERMISSION_GRANTED = 0
    PERMISSION_DENIED = -1

    #: Activity results
    addActivityResultListener = JavaMethod('com.codelv.enamlnative.EnamlActivity$ActivityResultListener')
    removeActivityResultListener = JavaMethod('com.codelv.enamlnative.EnamlActivity$ActivityResultListener')
    onActivityResult = JavaCallback('int', 'int', 'android.content.Intent', returns='boolean')


    #: Get system services
    getSystemService = JavaMethod('java.lang.String', returns='java.lang.Object')

    ACCESSIBILITY_SERVICE = 'accessibility'
    ACCOUNT_SERVICE = 'account'
    ACTIVITY_SERVICE = 'activity'
    ALARM_SERVICE = 'alarm'
    APPWIDGET_SERVICE = 'appwidget'
    APP_OPS_SERVICE = 'appops'
    AUDIO_SERVICE = 'audio'
    BATTERY_SERVICE = 'battery'
    BLUETOOTH_SERVICE = 'bluetooth'
    CAMERA_SERVICE = 'camera'
    CAPTIONING_SERVICE = 'captioning'
    CARRIER_CONFIG_SERVICE = 'carrier_config'
    CLIPBOARD_SERVICE = 'clipboard'
    CONNECTIVITY_SERVICE = 'connectivity'
    CONSUMER_IR_SERVICE = 'consumer_ir'
    DEVICE_POLICY_SERVICE = 'device_policy'
    DISPLAY_SERVICE = 'display'
    DOWNLOAD_SERVICE = 'download'
    DROPBOX_SERVICE = 'dropbox'
    FINGERPRINT_SERVICE = 'fingerprint'
    HARDWARE_PROPERTIES_SERVICE = 'hardware_properties'
    INPUT_METHOD_SERVICE = 'input_method'
    INPUT_SERVICE = 'input'
    JOB_SCHEDULER_SERVICE = 'jobscheduler'
    KEYGUARD_SERVICE = 'keyguard'
    LAUNCHER_APPS_SERVICE = 'launcherapps'
    LAYOUT_INFLATER_SERVICE = 'layout_inflater'
    LOCATION_SERVICE = 'location'
    MEDIA_PROJECTION_SERVICE = 'media_projection'
    MEDIA_ROUTER_SERVICE = 'media_router'
    MEDIA_SESSION_SERVICE = 'media_session'
    MIDI_SERVICE = 'midi'
    NETWORK_STATS_SERVICE = 'netstats'
    NFC_SERVICE = 'nfc'
    NOTIFICATION_SERVICE = 'notification'
    NSD_SERVICE = 'servicediscovery'
    POWER_SERVICE = 'power'
    PRINT_SERVICE = 'print'
    RESTRICTIONS_SERVICE = 'restrictions'
    SEARCH_SERVICE = 'search'
    SENSOR_SERVICE = 'sensor'
    SHORTCUT_SERVICE = 'shortcut'
    STORAGE_SERVICE = 'storage'
    SYSTEM_HEALTH_SERVICE = 'systemhealth'
    TELECOM_SERVICE = 'telecom'
    TELEPHONY_SERVICE = 'telephony'
    TELEPHONY_SUBSCRIPTION_SERVICE = 'telephony_subscription_service'
    TEXT_SERVICES_MANAGER_SERVICE = 'textservices'
    TV_INPUT_SERVICE = 'tv_input'
    UI_MODE_SERVICE = 'uimode'
    USAGE_STATS_SERVICE = 'usagestats'
    USB_SERVICE = 'usb'
    USER_SERVICE = 'user'
    VIBRATOR_SERVICE = 'vibrator'
    WALLPAPER_SERVICE = 'wallpaper'
    WIFI_P2P_SERVICE = 'wifi_p2p'
    WIFI_SERVICE = 'wifi'
    WINDOW_SERVICE = 'window'

    SERVICES = {
        'accessibility': ACCESSIBILITY_SERVICE,
        'account': ACCOUNT_SERVICE,
        'activity': ACTIVITY_SERVICE,
        'alarm': ALARM_SERVICE,
        'appwidget': APPWIDGET_SERVICE,
        'appops': APP_OPS_SERVICE,
        'audio': AUDIO_SERVICE,
        'battery': BATTERY_SERVICE,
        'bluetooth': BLUETOOTH_SERVICE,
        'camera': CAMERA_SERVICE,
        'captioning': CAPTIONING_SERVICE,
        'carrier_config': CARRIER_CONFIG_SERVICE,
        'clipboard': CLIPBOARD_SERVICE,
        'connectivity': CONNECTIVITY_SERVICE,
        'consumer_ir': CONSUMER_IR_SERVICE,
        'device_policy': DEVICE_POLICY_SERVICE,
        'display': DISPLAY_SERVICE,
        'download': DOWNLOAD_SERVICE,
        'dropbox': DROPBOX_SERVICE,
        'fingerprint': FINGERPRINT_SERVICE,
        'hardware_properties': HARDWARE_PROPERTIES_SERVICE,
        'input_method': INPUT_METHOD_SERVICE,
        'input': INPUT_SERVICE,
        'jobscheduler': JOB_SCHEDULER_SERVICE,
        'keyguard': KEYGUARD_SERVICE,
        'launcherapps': LAUNCHER_APPS_SERVICE,
        'layout_inflater': LAYOUT_INFLATER_SERVICE,
        'location': LOCATION_SERVICE,
        'media_projection': MEDIA_PROJECTION_SERVICE,
        'media_router': MEDIA_ROUTER_SERVICE,
        'media_session': MEDIA_SESSION_SERVICE,
        'midi_service': MIDI_SERVICE,
        'netstats': NETWORK_STATS_SERVICE,
        'nfc': NFC_SERVICE,
        'notification': NOTIFICATION_SERVICE,
        'servicediscovery': NSD_SERVICE,
        'power': POWER_SERVICE,
        'print': PRINT_SERVICE,
        'restrictions': RESTRICTIONS_SERVICE,
        'search': SEARCH_SERVICE,
        'sensor': SENSOR_SERVICE,
        'shortcut': SHORTCUT_SERVICE,
        'storage': STORAGE_SERVICE,
        'systemhealth': SYSTEM_HEALTH_SERVICE,
        'telecom': TELECOM_SERVICE,
        'telephony': TELEPHONY_SERVICE,
        'telephony_subscription_service': TELEPHONY_SUBSCRIPTION_SERVICE,
        'textservices': TEXT_SERVICES_MANAGER_SERVICE,
        'tv_input': TV_INPUT_SERVICE,
        'uimode': UI_MODE_SERVICE,
        'usagestats': USAGE_STATS_SERVICE,
        'usb': USB_SERVICE,
        'user': USER_SERVICE,
        'vibrator': VIBRATOR_SERVICE,
        'wallpaper': WALLPAPER_SERVICE,
        'wifip2p': WIFI_P2P_SERVICE,
        'wifi': WIFI_SERVICE,
        'window': WINDOW_SERVICE
    }