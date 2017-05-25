# Sets the minimum version of CMake required to build your native library.
# This ensures that a certain set of CMake features is available to
# your build.

cmake_minimum_required(VERSION 3.4.1)

add_library( # Specifies the name of the library.
             pybridge

             # Sets the library as a shared library.
             SHARED

             # Provides a relative path to your source file(s).
             pybridge.c pyjnius.c )

add_library( python2.7 SHARED IMPORTED )

set( LIBPYTHON_SO ${CRYSTAX_PATH}/sources/python/2.7/libs/${ANDROID_ABI}/libpython2.7.so)
set( LIBCRYSTAX_SO ${CRYSTAX_PATH}/sources/crystax/libs/${ANDROID_ABI}/libcrystax.so)

set_target_properties( # Specifies the target library.
                       python2.7

                       # Specifies the parameter you want to define.
                       PROPERTIES IMPORTED_LOCATION

                       # Provides the path to the library you want to import.
                       ${LIBPYTHON_SO})
include_directories( ${CRYSTAX_PATH}/sources/python/2.7/include/python/ )
target_link_libraries( pybridge log android python2.7 ${log-lib})


# Copy libpython2.7.so
#file(COPY ${LIBPYTHON_SO} DESTINATION ${JNI_LIBS_DEST})

# Copy libcrystax.so
#file(COPY ${LIBCRYSTAX_SO} DESTINATION ${JNI_LIBS_DEST})