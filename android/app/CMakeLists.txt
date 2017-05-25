# Sets the minimum version of CMake required to build your native library.
# This ensures that a certain set of CMake features is available to
# your build.

cmake_minimum_required(VERSION 3.4.1)

if (ANDROID AND NOT CRYSTAX)
    message(FATAL_ERROR "This example requires CrystaX NDK for Android build")
endif()

if (ANDROID)
    # Example of filtering of target ABIs
    if (ANDROID_NDK_ABI_NAME STREQUAL "armeabi")
        message(FATAL_ERROR "'${ANDROID_NDK_ABI_NAME}' target is not supported due to lack of the lock-free atomics")
    endif()
    if (NOT ANDROID_NDK_ABI_NAME MATCHES "^(armeabi-v7a|armeabi-v7a-hard|arm64-v8a|x86|x86_64|mips|mips64)$")
        message(FATAL_ERROR "Unsupported ABI: '${ANDROID_NDK_ABI_NAME}'")
    endif()
endif()

if (ANDROID)
    # Copy additional libraries to the target folder
    foreach(__extLibrary ${ANDROID_LIBCRYSTAX_FILE} ${ANDROID_LIBSTDCXX_FILE})
        add_custom_command(TARGET ${TARGET} PRE_LINK
            COMMAND ${CMAKE_COMMAND} -E copy_if_different ${__extLibrary} $<TARGET_FILE_DIR:${TARGET}>)
    endforeach()
endif()

unset(LAUNCHER)
if (ANDROID AND DEFINED ADBRUNNER)
    set(LAUNCHER ${ADBRUNNER})
    list(APPEND LAUNCHER --log=$<TARGET_FILE_DIR:${TARGET}>/adbrunner.log)
endif()

add_custom_target(run COMMAND ${LAUNCHER} $<TARGET_FILE:${TARGET}> )
add_dependencies(run ${TARGET})

set( CRYSTAX_PATH /home/jrm/Android/Crystax/crystax-ndk )

#set( JNI_LIBS_DIR libs )
#set( JNI_LIBS_DEST ${CMAKE_CURRENT_SOURCE_DIR}/src/main/libs/${ANDROID_ABI}/ )
#set( PYTHON_ASSETS_DIR python)
#file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/src/main/libs)
#file(MAKE_DIRECTORY ${JNI_LIBS_DEST})

# Adds the CMakeLists.txt file located in the specified directory
# as a build dependency.
add_subdirectory( # Specifies the directory of the CMakeLists.txt file.
                  src/main/jni

                  # Specifies the directory for the build outputs.
                  ${JNI_LIBS_DIR} )

# Adds the CMakeLists.txt file located in the specified directory
# as a build dependency.
#add_subdirectory( # Specifies the directory of the CMakeLists.txt file.
#                  src/main/python
#
#                  # Specifies the directory for the build outputs.
#                  ${PYTHON_ASSETS_DIR} )