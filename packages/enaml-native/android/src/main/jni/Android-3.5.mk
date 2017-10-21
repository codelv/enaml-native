LOCAL_PATH := $(call my-dir)
CRYSTAX_PATH := $(HOME)/Android/Crystax/crystax-ndk-10.3.2


# Build libpybridge.so

include $(CLEAR_VARS)
LOCAL_MODULE    := pybridge
LOCAL_SRC_FILES := pybridge.c
LOCAL_LDLIBS := -llog
LOCAL_SHARED_LIBRARIES := python3.5m
include $(BUILD_SHARED_LIBRARY)


# Include libpython3.5m.so

include $(CLEAR_VARS)
LOCAL_MODULE    := python3.5m
LOCAL_SRC_FILES := $(CRYSTAX_PATH)/sources/python/3.5/libs/$(TARGET_ARCH_ABI)/libpython3.5m.so
LOCAL_EXPORT_CFLAGS := -I $(CRYSTAX_PATH)/sources/python/3.5/include/python/
include $(PREBUILT_SHARED_LIBRARY)
