LOCAL_PATH := $(call my-dir)
#: Set by build script to <app>/build/python/
PYTHON_PATH := ../../../../../../build/python


# Build libpybridge.so

include $(CLEAR_VARS)
LOCAL_MODULE    := pybridge
LOCAL_SRC_FILES := pybridge.c
LOCAL_LDLIBS := -llog
LOCAL_SHARED_LIBRARIES := python2.7
include $(BUILD_SHARED_LIBRARY)


# Include libpython2.7.so

include $(CLEAR_VARS)
LOCAL_MODULE    := python2.7
LOCAL_SRC_FILES := $(PYTHON_PATH)/$(TARGET_ARCH_ABI)/modules/libpython2.7.so
LOCAL_EXPORT_CFLAGS := -I $(PYTHON_PATH)/$(TARGET_ARCH_ABI)/include/
include $(PREBUILT_SHARED_LIBRARY)
