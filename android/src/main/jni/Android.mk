LOCAL_PATH := $(call my-dir)
CRYSTAX_PATH := $(HOME)/Android/Crystax/crystax-ndk-10.3.2


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
LOCAL_SRC_FILES := $(CRYSTAX_PATH)/sources/python/2.7/libs/$(TARGET_ARCH_ABI)/libpython2.7.so
LOCAL_EXPORT_CFLAGS := -I $(CRYSTAX_PATH)/sources/python/2.7/include/python/
include $(PREBUILT_SHARED_LIBRARY)
