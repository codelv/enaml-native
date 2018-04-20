LOCAL_PATH := $(call my-dir)
#: Set by build script to <app>/build/python/
#: If unchanged it assumes enaml-native is installed
#: under venv/android/enaml-native/
APP_ENV := $(call my-dir)/../../../../../
# You can replace APP_ENV with CONDA_PREFIX if the var is set
APP_PREFIX := $(APP_ENV)/android/$(TARGET_ARCH)
PY_LIB_VER := 2.7
# Build libpybridge.so

include $(CLEAR_VARS)
LOCAL_MODULE    := pybridge
LOCAL_SRC_FILES := pybridge.c
LOCAL_LDLIBS := -llog
LOCAL_CFLAGS := -I$(APP_PREFIX)/include/python$(PY_LIB_VER)
LOCAL_LDFLAGS := -L$(APP_PREFIX)/lib/ -lpython$(PY_LIB_VER)
#LOCAL_SHARED_LIBRARIES := python2.7
include $(BUILD_SHARED_LIBRARY)


# Include libpython
include $(CLEAR_VARS)
LOCAL_MODULE    := python$(PY_LIB_VER)
LOCAL_SRC_FILES := $(APP_PREFIX)/lib/libpython$(PY_LIB_VER).so
LOCAL_EXPORT_CFLAGS := -I$(APP_PREFIX)/include/python$(PY_LIB_VER)
include $(PREBUILT_SHARED_LIBRARY)
