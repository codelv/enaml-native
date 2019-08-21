"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 10, 2018

@author: jrm
"""
from libc.stdint cimport uint8_t, uint32_t, int32_t, int64_t
from libcpp cimport bool
from libcpp.string cimport string
from libcpp.map cimport map
from enamlnative.android.jni cimport (
    jint, jobject, JNIEnv
)
from enamlnative.android.ndk cimport (
    ACameraManager, ACameraDevice, ACaptureSessionOutputContainer, 
    ACameraManager_create, ACameraCaptureSession, CaptureSessionState,
    acamera_metadata_enum_android_lens_facing_t
)

cdef const uint64_t kMinExposureTime = 1000000
cdef const uint64_t kMaxExposureTime = 250000000


cdef enum CaptureSessionState:
  READY = 0 # session is ready
  ACTIVE   # session is busy
  CLOSED   # session is closed(by itself or a new session evicts)
  MAX_STATE


ctypedef struct ImageFormat:
  int32_t width
  int32_t heigh
  int32_t format
  
  
ctypedef fused intrange_t:
    int64_t
    int32_t


cdef class RangeValue:
    cdef intrange_t min
    cdef intrange_t max
    
    cpdef intrange_t value(int percent):
        return (self.min + (self.max-self.min) * percent/100)
    

cdef enum PREVIEW_INDICES:
    PREVIEW_REQUEST_IDX = 0
    JPG_CAPTURE_REQUEST_IDX
    CAPTURE_REQUEST_COUNT


ctypedef struct CaptureRequestInfo:
    ANativeWindow* output_native_window
    ACaptureSessionOutput* session_output
    ACameraOutputTarget* target
    ACaptureRequest* request
    ACameraDevice_request_template template
    int session_sequence_id


cdef class DisplayDimension:
    cdef public int32_t width
    cdef public int32_t height
    cdef public bool portrait
    
    def __cinit__(self, int32_t w, int32_t h):
        self.width = w
        self.height = h
        self.portrait = False
        
    cdef void flip(self):
        self.portrait = not self.portrait
    
    cdef bool is_portrait(self):
        return self.portrait
    
    cdef bool is_same_ratio(self, DisplayDimension& other):
        return (self.width * other.height == self.height * other.width)
    
    cdef int __cmp__(self, DisplayDimension& other):
        if (self.width >= other.width and self.height >= other.height):
            return 1
        elif (self.width == other.width and 
              self.height == other.height && self.portrait == other.portrait):
            return 0
        return -1
    
    

cdef class CameraId:
    cdef ACameraDevice* device
    cdef string id
    cdef acamera_metadata_enum_android_lens_facing_t facing
    cdef bool owner # free to use ( no other apps are using
    cdef bool available # we are the owner of the camera
    
    def __cinit__(self, const char* id):
        self.device = ACameraManager_create()
        self.id = id
        self.facing = ACAMERA_LENS_FACING_FRONT
        self.available = False
        self.owner = False
    

cdef class CameraManager:
    cdef ACameraManager* camera_mgr
    cdef string active_camera_id
    cameras = {}
    requests = []
    cdef uint32_t camera_facing;
    cdef uint32_t camera_orientation;
    cdef ACaptureSessionOutputContainer* output_container
    cdef ACameraCaptureSession* capture_session
    cdef CaptureSessionState capture_session_state
    
    #// set up exposure control
    cdef int64_t exposure_time
    cdef RangeValue exposure_range
    cdef int32_t sensitivity
    cdef RangeValu sensitivity_range
    cdef bool valid
    
    def __cinit__(self):
        self.valid = False
        self.active_camera_id = ""
        self.output_container = NULL
        self.capture_session_state = CaptureSessionState.MAX_STATE
        self.camera_facing = ACAMERA_LENS_FACING_BACK
        self.camera_orientation = 0
        self.exposure_time = 0
        self.camera_mgr = ACameraManager_create()
        assert self.camera_mgr is not NULL, "Failed to create camera manager"
        
        # Pick up a back-facing camera to preview
        self.enumerate_cameras()
        assert self.active_camera_id, "Unknown camera id"
        
        # Create back facing camera device
        cdef camera_status_t status = ACameraManager_openCamera(
            self.camera_mgr, self.active_camera_id.c_str(), 
            self.get_device_listener(), 
            self.cameras[self.active_camera_id].device
        ) # TODO: Check status
        
        status = ACameraManager_registerAvailabilityCallback(
            self.camera_mgr, self.get_manager_listener()
        ) # TODO: Check status
        
        cdef ACameraMetadata* metadata;
        status = ACameraManager_getCameraCharacteristics(
            self.camera_mgr, self.active_camera_id.c_str(), &metadata
        ) # TODO: Check status
        
        cdef ACameraMetadata_const_entry val
        status = ACameraMetadata_getConstEntry(
            metadata, ACAMERA_SENSOR_INFO_EXPOSURE_TIME_RANGE, &val)
        assert (status == ACAMERA_OK, 
                "Unsupported ACAMERA_SENSOR_INFO_EXPOSURE_TIME_RANGE")
        
        er = self.exposure_range = RangeValue()
        er.min = val.data.i64[0]
        if er.min < kMinExposureTime:
            er.min = kMinExposureTime
        
        er.max = val.data.i64[1]
        if er.max > kMaxExposureTime:
            er.max = kMaxExposureTime
            
        sr = self.sensitivity_range = RangeValue()
        status = ACameraMetadata_getConstEntry(
                metadata, ACAMERA_SENSOR_INFO_SENSITIVITY_RANGE, &val)
        assert (status == ACAMERA_OK,
                    "failed for ACAMERA_SENSOR_INFO_SENSITIVITY_RANGE")
        sr.min = val.data.i32[0];
        sr.max = val.data.i32[1];
        self.sensitivity = sr.value(2)
        self.valid = True
            
    
    cdef enumerate_cameras(self):
        # Enumerate cameras
        cdef ACameraIdList* cameraIds;
        cdef camera_status_t status;
        status = ACameraManager_getCameraIdList(
            self.camera_mgr, &cameraIds) 
        # TODO: Check status
        
        for i in range(cameras.numCameras):
            cdef const char* id = cameraIds.cameraIds[i];
            cdef ACameraMetadata* metadata;
            status = ACameraManager_getCameraCharacteristics(
                    self.camera_mgr, id, &metadata)
            # TODO: Check status
            
            cdef int32_t count = 0
            cdef int i = 0
            cdef const uint32_t* tags = NULL
            ACameraMetadata_getAllTags(metadata, &count, &tags)
            while i < count:
                i += 1
                if ACAMERA_LENS_FACING == tags[i]:
                    ACameraMetadata_const_entry lensInfo
                status = ACameraMetadata_getConstEntry(metadata, tags[i], 
                                                       &lens_info)
                # TODO: Check status
                
                cam = CameraId(id)
                cam.facing = lensInfo.data.u8[0]
                cam.owner = False
                cam.device = NULL
                self.cameras[cam.id] = cam
                if cam.facing == ACAMERA_LENS_FACING_BACK:
                    self.active_camera_id = cam.id
                    break
            
            ACameraMetadata_free(metadata);
        
        assert self.cameras, "No Camera Available on the device"
        if not self.active_camera_id:
            self.active_camera_id = self.cameras[0].id
        
        ACameraManager_deleteCameraIdList(cameraIds);
        
        
    def __dealloc__(self):
        self.valid = false;
        # stop session if it is on:
        if self.capture_session_state == CaptureSessionState.ACTIVE:
            ACameraCaptureSession_stopRepeating(self.capture_session)
        ACameraCaptureSession_close(self.capture_session)
    
    # --------------------------------------------------------------------------
    # Public members
    # --------------------------------------------------------------------------
    cdef ACameraManager_AvailabilityCallbacks* get_manager_listener(self):
        return pass
    
    cdef ACameraDevice_stateCallbacks* get_device_listener(self):
        pass 
    
    cdef ACameraCaptureSession_stateCallbacks* get_session_listener(self):
        pass
    
    cdef ACameraCaptureSession_captureCallbacks* get_capture_callback(self):
        pass

    # --------------------------------------------------------------------------
    # Private members
    # --------------------------------------------------------------------------
    cdef bool match_capture_size_request(self, int32_t width, int32_t height, 
                                     ImageFormat* view):
        return self.match_capture_size_request(width, height, view, NULL)
    
    cdef bool match_capture_size_request(self, int32_t width, int32_t height, 
                                     ImageFormat* view, ImageFormat* format):
        disp = DisplayDimension(width, height)
        if self.camera_orientation == 90 or self.camera_orientation == 270:
            disp.flip()
        cdef ACameraMetadata* metadata
        camera_status_t status = ACameraManager_getCameraCharacteristics(
                self.camera_mgr, self.active_camera_id.c_str(), &metadata
        )
        
        cdef ACameraMetadata_const_entry entry;
        status = ACameraMetadata_getConstEntry(
            metadata, ACAMERA_SCALER_AVAILABLE_STREAM_CONFIGURATIONS, &entry
        )
        
        cdef bool found = False
        foundRes = DisplayDimension(4000, 4000)
        maxJPG = DisplayDimension(0, 0)
        
        cdef int i = 0
        while i < entry.count:
            i += 4
            int32_t input = entry.data.i32[i + 3];
            int32_t format = entry.data.i32[i + 0];
            if input:
                continue
            if (format == AIMAGE_FORMAT_YUV_420_888 or 
                    format == AIMAGE_FORMAT_JPEG):
                res = DisplayDimension(entry.data.i32[i + 1],
                                       entry.data.i32[i + 2]);
                if not disp.is_same_ratio(res):
                    continue
                if (format == AIMAGE_FORMAT_YUV_420_888 && foundRes > res) {
                    foundIt = true;
                    foundRes = res;
                } else if (format == AIMAGE_FORMAT_JPEG && res > maxJPG) {
                    maxJPG = res;
                }
            }
    
    cpdef void create_session(ANativeWindow* preview_window, 
                         ANativeWindow* jpg_window,
                         bool manual_preview, int32_t image_rotation):
        # Create output from this app's ANativeWindow, and add into output container
        r = self.requests
        r[PREVIEW_REQUEST_IDX].output_native_window = preview_window
        r[PREVIEW_REQUEST_IDX].template = TEMPLATE_PREVIEW
        r[JPG_CAPTURE_REQUEST_IDX].output_nativewindow = jpgWindow
        r[JPG_CAPTURE_REQUEST_IDX].template = TEMPLATE_STILL_CAPTURE
    
    cpdef void create_session(ANativeWindow* preview_window):
        self.create_session(preview_window, NULL, False, 0)
        
    cdef get_sensor_orientation(int32_t* facing, int32_t* angle):
        pass
    
    cdef void on_camera_status_changed(const char* id, bool available):
        pass
    
    cdef void on_device_state(ACameraDevice* dev):
        pass
    
    cdef void on_device_error(ACameraDevice* dev, int err):
        pass
    
    cdef void on_session_state(ACameraCaptureSession* ses, 
                               CaptureSessionState state):
        pass
    
    cdef void on_capture_sequence_end(ACameraCaptureSession* session, 
                                      int sequenceId, int64_t frameNumber):
        pass
    
    cdef void on_capture_failed(ACameraCaptureSession* session, 
                                ACaptureRequest* request,
                                ACameraCaptureFailure* failure):
        pass
        
    cpdef void start_preview(self):
        camera_status_t status = ACameraCaptureSession_setRepeatingRequest(
            self.capture_session, NULL, 1, 
            &self.requests[PREVIEW_REQUEST_IDX].request,
            NULL
        )
    
    cpdef void stop_preview(self):
        if self.capture_session_state == CaptureSessionState.ACTION:
            ACameraCaptureSession_stopRepeating(self.capture_session)
    
    cpdef bool take_photo(self):
        if self.caputre_session_state == CaptureSessionState.ACTIVE:
            ACameraCaptureSession_stopRepeating(self.capture_session)
        camera_status_t status = ACameraCaptureSession_capture(
                self.capture_session, self.get_capture_callback(), 1
                self.requests[JPG_CAPTURE_REQUEST_IDX].request,
                self.requests[JPG_CAPTURE_REQUEST_IDX].session_sequence_id
        )
        return True
    
 
    cpdef get_exposure_range(int64_t* min, int64_t* max, int64_t* cur_val):
        pass
    
    cpdef get_sensitivity_range(int64_t* min, int64_t* max, int64_t* cur_val):
        if not self._sensitivity or !min or !max or !cur_val:
            return False
        *min = static_cast<int64_t>(_sensitivity_range._min);
        *max = static_cast<int64_t>(_sensitivity_range._max);
        *cur_val = _sensitivity;
        return True
    
    cpdef update_camera_request_parameter(int32_t code, int64_t val):
        pass
    



cdef class CameraAppEngine:
    JNIEnv* env;
    jobject java_instance;
    int32_t request_width;
    int32_t request_height;
    jobject surface;
    CameraManager* camera;
    ImageFormat compatible_camera_res;

    def __cinit__(self, JNIEnv* env, jobject instance, jint w, jint h):
        self.env = env
        self.java_instance = instance
        self.request_width = w
        self.request_height = h
        self.camera = CameraManager()
        
    def __dealloc__(self):
        if self.camera is not NULL:
            self.camera = NULL
        if self.surface is not NULL:
            self.env->DeleteGlobalRef(self.surface);
            self.surface = NULL
    
    cpdef create_camera_session(self, jobject surface):
        self.surface = self.env->NewGlobalRef(surface);
        self.camera.create_session(
            ANativeWindow_fromSurface(self.env, surface));
    
    cpdef get_camera_sensor_orientation(self, int32_t request_facing):
        cdef int32_t facing = 0
        cdef int32_t angle = 0
        if (self.camera.get_sensor_orientation(&facing, &angle) or
                facing==request_facing):
            return angle
        return 0
    
    cpdef start_preview(self):
        self.camera.start_preview()
    
    cpdef stop_preview(self):
        self.camera.stop_preview()
    
    cpdef get_surface_object(self):
        return self.surface
    
    cpdef get_compatible_camera_res(self):
        return self.compatible_camera_res
