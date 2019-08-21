"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 9, 2018

@author: jrm
"""
from atom.api import Typed, List, Bool, set_default

from .bridge import (
    JavaBridgeObject, JavaMethod, JavaCallback, JavaStaticMethod
)
from .android_activity import Activity
from .android_content import SystemService
from .app import AndroidApplication
from enamlnative.widgets.camera_view import ProxyCameraView

from .android_texture_view import (
    AndroidTextureView, TextureView, AndroidView
)


# class ImageReader(JavaBridgeObject):
#     __nativeclass__ = set_default('android.media.ImageReader')
#     newInstance = JavaStaticMethod('int', 'int', 'int', 'int',
#                                    returns='android.media.ImageReader')
#     setOnImageAvailableListener = JavaMethod(
#         'android.media.ImageReader$OnImageAvailableListener',
#         'android.os.Handler')
#     onImageAvailable = JavaCallback('android.media.ImageReader')
#
#
# class CameraCaptureSession(JavaBridgeObject):
#     __nativeclass__ = set_default(
#         'android.hardware.camera2.CameraCaptureSession')
#     close = JavaMethod()
#     setRepeatingRequest = JavaMethod(
#         'android.hardware.camera2.CaptureRequest',
#         'android.hardware.camera2.CameraCaptureSession$CaptureCallback',
#         'android.os.Handler')
#
#     onActive = JavaCallback(
#         'android.hardware.camera2.CameraCaptureSession')
#     onCaptureQueueEmpty = JavaCallback(
#         'android.hardware.camera2.CameraCaptureSession')
#     onClosed = JavaCallback(
#         'android.hardware.camera2.CameraCaptureSession')
#     onConfigureFailed = JavaCallback(
#         'android.hardware.camera2.CameraCaptureSession')
#     onConfigured = JavaCallback(
#         'android.hardware.camera2.CameraCaptureSession')
#     onReady = JavaCallback(
#         'android.hardware.camera2.CameraCaptureSession')
#     onSurfacePrepared = JavaCallback(
#         'android.hardware.camera2.CameraCaptureSession',
#         'android.view.Surface')
#
#     # We use our concrete CameraCaptureSession.StateCallback adapter
#     class StateCallback(JavaBridgeObject):
#         __nativeclass__ = set_default(
#             'com.codelv.enamlnative.adapters.'
#             'BridgedCameraAdapter$CameraSessionCallback')
#         setListener = JavaMethod('com.codelv.enamlnative.adapters.'
#                                  'BridgedCameraAdapter$CameraSessionListener')
#
#     # We use our concrete CameraCaptureSession.CaptureCallback adapter
#     class CaptureCallback(JavaBridgeObject):
#         __nativeclass__ = set_default(
#             'com.codelv.enamlnative.adapters.'
#             'BridgedCameraAdapter$CaptureCallback')
#         setListener = JavaMethod('com.codelv.enamlnative.adapters.'
#                                  'BridgedCameraAdapter$CaptureListener')
#
# class CaptureRequest(JavaBridgeObject):
#     __nativeclass__ = set_default(
#         'android.hardware.camera2.CaptureRequest')
#
#     #CONTROL_AE_MODE =
#
#
#     class Builder(JavaBridgeObject):
#         __nativeclass__ = set_default(
#             'android.hardware.camera2.CaptureRequest$Builder')
#         addTarget = JavaMethod('android.view.Surface')
#         build = JavaMethod(returns='android.hardware.camera2.CaptureRequest')
#         set = JavaMethod('android.hardware.camera2.CaptureRequest.Key',
#                          'java.lang.Object')
#
#
# class CameraDevice(JavaBridgeObject):
#     __nativeclass__ = set_default('android.hardware.camera2.CameraDevice')
#     close = JavaMethod()
#     getId = JavaMethod(returns='java.lang.String')
#     createCaptureRequest = JavaMethod(
#         'int', returns='android.hardware.camera2.CaptureRequest$Builder')
#     createCaptureSession = JavaMethod(
#         'java.util.List',
#         'android.hardware.camera2.CameraCaptureSession$StateCallback',
#         'android.os.Handler')
#
#     TEMPLATE_PREVIEW = 1
#     TEMPLATE_STILL_CAPTURE = 2
#     TEMPLATE_RECORD = 3
#     TEMPLATE_VIDEO_SNAPSHOT = 4
#     TEMPLATE_ZERO_SHUTTER_LAG = 5
#     TEMPLATE_MANUAL = 6
#
#     opened = Bool()
#
#     # CameraDevice.StateCallback API
#     onOpened = JavaCallback('android.hardware.camera2.CameraDevice')
#     onDisconnected = JavaCallback('android.hardware.camera2.CameraDevice')
#     onError = JavaCallback('android.hardware.camera2.CameraDevice', 'int')
#
#     # We use our concrete CameraDevice.StateCallback adapter
#     class StateCallback(JavaBridgeObject):
#         __nativeclass__ = set_default('com.codelv.enamlnative.adapters.'
#                                       'BridgedCameraAdapter$CameraCallback')
#
#         setListener = JavaMethod('com.codelv.enamlnative.adapters.'
#                                  'BridgedCameraAdapter$CameraListener')
#

class CameraManager(SystemService):
    """ Access android's CameraManager. Use the static class methods.
    
    """
    SERVICE_TYPE = Activity.CAMERA_SERVICE
    __nativeclass__ = set_default('android.hardware.camera2.CameraManager')
    
    getCameraCharacteristics = JavaMethod(
        'java.lang.String', 
        returns='android.hardware.camera2.CameraCharacteristics')
    getCameraIdList = JavaMethod(returns='[java.lang.String;')
    openCamera = JavaMethod(
        'java.lang.String', 
        'android.hardware.camera2.CameraDevice$StateCallback',
        'android.os.Handler'
    )
    setTorchMode = JavaMethod('java.lang.String', 'boolean')

    CAMERA_PERMISSION = 'android.permission.CAMERA'
    
    permissions = (CAMERA_PERMISSION,)
    
    # -------------------------------------------------------------------------
    # Public api
    # -------------------------------------------------------------------------
    @classmethod
    def request_permission(cls):
        """ Requests permission and returns an future result that returns a 
        boolean indicating if all the given permission were granted or denied.
         
        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_result(perms):
            f.set_result(perms.get(cls.CAMERA_PERMISSION, False))

        def on_has_perm(result):
            if result:
                f.set_result(True)
            else:
                app.request_permissions(
                    (cls.CAMERA_PERMISSION,)).then(on_result)
        app.has_permission(cls.CAMERA_PERMISSION).then(on_has_perm)

        return f
    
    @classmethod
    def get_cameras(cls):
        """ Return the list of cameras this device supports
        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_result(mgr):
            mgr.getCameraIdList().then(f.set_result)

        cls.get().then(on_result)
        return f

# class Surface(JavaBridgeObject):
#     __nativeclass__ = set_default('android.view.Surface')
#     __signature__ = set_default(('android.graphics.SurfaceTexture',))
#
#
# class Matrix(JavaBridgeObject):
#     __nativeclass__ = set_default('android.graphics.Matrix')
#     setPolyToPoly = JavaMethod('[f', 'int', '[f', 'int', 'int')
#     posteRotate = JavaMethod('float', 'float', 'float')
#
#class Camera:
#    #: TODO: Create a cython wrapper for the Android NDK camera


class CameraPackage(JavaBridgeObject):
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.packages.CameraPackage')
    getInstance = JavaStaticMethod(
        returns='com.codelv.enamlnative.packages.CameraPackage')
    startCapturePreview = JavaMethod(
        'android.view.TextureView',
        'com.codelv.enamlnative.packages.CameraPackage$CameraListener')
    stopCapturePreview = JavaMethod()
    takePicture = JavaMethod('java.lang.String')


class AndroidCameraView(AndroidTextureView, ProxyCameraView):
    """ An Android implementation of an Enaml ProxySurfaceView

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TextureView)

    #: CameraPackage api
    api = Typed(CameraPackage)

    #: Permission granted
    allowed = Bool()
    
    def init_widget(self):
        # Skip the Texture view
        super(AndroidView, self).init_widget()
        d = self.declaration
        if d.preview:
            self.set_preview(d.preview)

    def destroy(self):
        super(AndroidCameraView, self).destroy()
        if self.api:
            self.stop_camera_preview()

    def set_preview(self, show):
        if show:
            self.start_camera_preview()
        else:
            self.stop_camera_preview()

    def start_camera_preview(self):
        def on_allowed(camera):
            if camera is None:
                raise RuntimeError("You must add the CameraPackage to your "
                                   "apps MainActiviy")
            api = self.api = CameraPackage(__id__=camera)
            api.startCapturePreview(self.widget, camera)

        def on_result(allowed):
            self.allowed = allowed
            if allowed:
                CameraPackage.getInstance().then(on_allowed)

        CameraManager.request_permission().then(on_result)

    def stop_camera_preview(self):
        if self.api:
            self.api.stopCapturePreview()

    def take_picture(self):
        if self.api:
            self.api.takePicture("test.jpg")

    #     app = self.get_context()
    #     app.unobserve('state', self.on_activity_lifecycle_changed)
    # # -------------------------------------------------------------------------
    # # SurfaceTextureListener API
    # # -------------------------------------------------------------------------
    # def on_surface_texture_available(self, surface, width, height):
    #     """ Based on the android NDK camera example
    #     """
    #     super(AndroidCameraView, self).on_surface_texture_available(
    #         surface, width, height)
    #     if self.allowed:
    #         self.start_camera_preview()
    #
    # def on_surface_texture_destroyed(self, surface):
    #     super(AndroidCameraView, self).on_surface_texture_destroyed(surface)
    #     del self.camera
    #     del self.surface
    #     return True
    #
    # # -------------------------------------------------------------------------
    # # CameraDevice API
    # # -------------------------------------------------------------------------
    # def on_camera_opened(self, camera):
    #     self.camera.opened = True
    #     self.start_capture_session()
    #
    # def on_camera_disconnected(self, camera):
    #     if self.camera and self.camera.opened:
    #         self.camera.close()
    #         self.camera.opened = False
    #
    # def on_camera_error(self, camera, error):
    #     if self.camera and self.camera.opened:
    #         self.camera.close()
    #         self.camera.opened = False
    #
    # def on_activity_lifecycle_changed(self, change):
    #     if change['type'] != 'update':
    #         return
    #     if change['value'] in ('created', 'resumed'):
    #         self.start_camera_preview()
    #     elif change['value'] in ('paused', ):
    #         self.stop_camera_preview()
    #
    # def start_camera_preview(self):
    #     if not self.allowed:
    #         return
    #     self._start_background_handler()
    #
    #     def on_cameras(cameras, manager):
    #         if cameras:
    #             # Create a camera reference to handle the callbacks
    #             cid = bridge.generate_id()
    #             camera = self.camera = CameraDevice(__id__=cid)
    #
    #             camera.onOpened.connect(self.on_camera_opened)
    #             camera.onError.connect(self.on_camera_error)
    #             camera.onDisconnected.connect(self.on_camera_disconnected)
    #
    #             # A CameraDevice.StateCallback that lets us delegate
    #             # handling to a listener
    #             callback = CameraDevice.StateCallback()
    #             callback.setListener(cid)
    #
    #             manager.openCamera(cameras[0],
    #                                callback, self.handler)
    #
    #     def on_ready(manager):
    #         manager.getCameraIdList().then(
    #             lambda r, m=manager: on_cameras(r, m))
    #
    #     CameraManager.get().then(on_ready)
    #
    # def stop_camera_preview(self):
    #     self._stop_background_handler()
    #     if self.camera:
    #         self.camera.close()
    #     if self.session:
    #         self.session.close()
    #     if self.reader:
    #         self.reader.close()
    #
    # def _start_background_handler(self):
    #     t = self._handler_thread = HandlerThread("CameraHandler")
    #     t.start()
    #     self.handler = Handler(t.getLooper())
    #
    # def _stop_background_handler(self):
    #     if self._handler_thread:
    #         self._handler_thread.quitSafely()
    #         del self._handler_thread
    #     if self.handler:
    #         del self.handler
    #
    # # -------------------------------------------------------------------------
    # # CameraCaptureSession API
    # # -------------------------------------------------------------------------
    # def start_capture_session(self):
    #     texture = self.texture
    #     texture.setDefaultBufferSize(self.width, self.height)
    #     self.surface = Surface(texture)
    #     builder = self.builder = CaptureRequest.Builder(
    #         __id__=self.camera.createCaptureRequest(
    #             CameraDevice.TEMPLATE_PREVIEW))
    #     builder.addTarget(self.surface)
    #
    #     # Create a camera reference to handle the callbacks
    #     sid = bridge.generate_id()
    #     session = self.session = CameraCaptureSession(__id__=sid)
    #     session.onConfigureFailed.connect(self.on_session_configure_error)
    #     session.onConfigured.connect(self.on_session_configured)
    #
    #     callback = CameraCaptureSession.StateCallback()
    #     callback.setListener(sid)
    #     self.camera.createCaptureSession([bridge.encode(self.surface)],
    #                                      callback, None)
    #
    # def on_session_configured(self, session):
    #     # Auto focus should be continuous for camera preview.
    #     #self.builder.set(CaptureRequest.CONTROL_AF_MODE,
    #     #                 CaptureRequest.CONTROL_AF_MODE_CONTINUOUS_PICTURE)
    #
    #     #  Flash is automatically enabled when necessary.
    #     #self.builder.set(CaptureRequest.CONTROL_AF_MODE,
    #     #                 CaptureRequest.CONTROL_AE_MODE_ON_AUTO_FLASH)
    #
    #     # Finally, we start displaying the camera preview.
    #     self.session.setRepeatingRequest(self.builder.build(),
    #                                      self.session, self.handler)
    #
    #
    # def on_session_configure_error(self, session):
    #     pass
    #
    #
    # # def start_ndk_preview(self):
    # #     w, h = self.width, self.height
    # #     app = self.get_context()
    # #
    # #     m = Matrix()
    # #     if app.orientation == 'landscape':
    # #         m.setPolyToPoly(
    # #             (0.0, 0.0, float(w), 0.0, 0.0, float(h), float(w), float(h)),
    # #             0,
    # #             (0.0, float(h), 0.0, 0.0, float(w), float(h), float(w), 0.0),
    # #             0,
    # #             4
    # #         )
    # #     else:
    # #         m.postRotate(180, w/2.0, h/2.0)
    # #     self.texture.setTransform(m)
    # #
    # #     self.camera = Camera(w, h)
    # #     self.texture.setDefaultBufferSize(w, h)
    # #     self.surface = Surface(self.texture)
    #
    #
    #

