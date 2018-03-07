LOCAL_PATH := $(call my-dir)
#: Set by build script to <app>/build/python/
#: If unchanged it assumes enaml-native is installed
#: under venv/android/enaml-native/
APP_ENV := $(call my-dir)/../../../../../
# You can replace APP_ENV with CONDA_PREFIX if the var is set
APP_PREFIX := $(APP_ENV)/android/$(TARGET_ARCH)
# Build libpybridge.so

include $(CLEAR_VARS)
LOCAL_MODULE    := pybridge
LOCAL_SRC_FILES := pybridge.c
LOCAL_LDLIBS := -llog
LOCAL_CFLAGS := -I$(APP_PREFIX)/include/python2.7
LOCAL_LDFLAGS := -L$(APP_PREFIX)/lib/ -lpython2.7
#LOCAL_SHARED_LIBRARIES := python2.7
include $(BUILD_SHARED_LIBRARY)


# Include libpython2.7.so
include $(CLEAR_VARS)
LOCAL_MODULE    := python2.7
LOCAL_SRC_FILES := $(APP_PREFIX)/lib/libpython2.7.so
LOCAL_EXPORT_CFLAGS := -I$(APP_PREFIX)/include/python2.7
include $(PREBUILT_SHARED_LIBRARY)