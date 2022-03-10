"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.
"""
import nativehooks
from asyncio import Future
from atom.api import Dict, Int
from enaml.application import ProxyResolver
from enamlnative.android import factories
from enamlnative.core.app import BridgedApplication


class AndroidApplication(BridgedApplication):
    """An Android implementation of an Enaml Native BridgedApplication.

    A AndroidApplication uses the native Android widget toolkit to implement
    an Enaml UI that runs in the local process.

    """

    #: Permission code increments on each request
    _permission_code = Int()

    #: Pending permission request listeners
    _permission_requests = Dict(int, Future)

    # -------------------------------------------------------------------------
    # Defaults
    # -------------------------------------------------------------------------
    def _default_resolver(self):
        """Return a bridge object reference to the MainActivity"""
        return ProxyResolver(factories=factories.ANDROID_FACTORIES)

    # -------------------------------------------------------------------------
    # App API Implementation
    # -------------------------------------------------------------------------
    async def has_permission(self, permission: str) -> bool:
        """Return a future that resolves with the result of the permission"""
        # Old versions of android did permissions at install time
        d = self.activity
        assert d is not None
        if d.api_level < 23:
            return True
        proxy = d.proxy
        assert proxy is not None
        activity = proxy.widget
        assert activity is not None
        result = await activity.checkSelfPermission(permission)
        return result == activity.PERMISSION_DENIED

    async def request_permissions(self, *permissions) -> dict[str, bool]:
        """Return a future that resolves with the results
        of the permission requests

        """
        # Old versions of android did permissions at install time
        d = self.activity
        assert d is not None
        if d.api_level < 23:
            return {p: True for p in permissions}

        request_code = self._permission_code
        self._permission_code += 1  #: So next call has a unique code

        # On first request, setup our listener, and request the permission
        proxy = d.proxy
        assert proxy is not None
        activity = proxy.widget
        assert activity is not None
        if request_code == 0:
            activity.setPermissionResultListener(activity.getId())
            activity.onRequestPermissionsResult.connect(self._on_permission_result)

        #: Save a reference
        f = self.create_future()
        activity.requestPermissions(permissions, request_code)
        self._permission_requests[request_code] = f

        #: Send out the request
        code, perms, results = await f
        granted = activity.PERMISSION_GRANTED
        return {p: r == granted for p, r in zip(perms, results)}

    def show_toast(self, msg: str, long: bool = True):
        """Show a toast message for the given duration.
        This is an android specific api.

        Parameters
        -----------
        msg: str
            Text to display in the toast message
        long: bool
            Display for a long or short (system defined) duration

        """
        if not msg:
            return
        from .android_toast import Toast

        async def show_toast():
            toast_id = await Toast.makeText(self, msg, 1 if long else 0)
            t = Toast(__id__=toast_id)
            t.show()

        self.deferred_call(show_toast)

    # --------------------------------------------------------------------------
    # Bridge API Implementation
    # --------------------------------------------------------------------------
    def dispatch_events(self, data):
        """Send the data to the Native application for processing"""
        nativehooks.publish(data)

    # -------------------------------------------------------------------------
    # Android utilities API Implementation
    # -------------------------------------------------------------------------
    def _on_permission_result(self, code, perms, results):
        """Handles a permission request result by passing it to the
        handler with the given code.

        """
        #: Get the handler for this request
        f = self._permission_requests.pop(code, None)
        if f is not None:
            #: Invoke that handler with the permission request response
            f.set_result((code, perms, results))

    async def get_system_service(self, cls):
        """Wrapper for getSystemService. You MUST
        wrap the class with the appropriate object.

        """
        service = cls.instance()
        if service:
            return service
        d = self.activity
        assert d is not None
        proxy = d.proxy
        assert proxy is not None
        activity = proxy.widget
        assert activity is not None
        service_id = await activity.getSystemService(cls.SERVICE_TYPE)
        return cls(__id__=service_id)

    # -------------------------------------------------------------------------
    # Plugin API Implementation
    # -------------------------------------------------------------------------
    def load_plugin_factories(self):
        """Add any plugin toolkit widgets to the ANDROID_FACTORIES"""
        for plugin in self.get_plugins(group="enaml_native_android_factories"):
            get_factories = plugin.load()
            PLUGIN_FACTORIES = get_factories()
            factories.ANDROID_FACTORIES.update(PLUGIN_FACTORIES)
