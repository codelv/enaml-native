
clean-python:
	cd android/python && rm -R build && rm -R install

build-python-old:
	cd android/python && mkdir -p build && mkdir -p install
	#-cd android/python/build && /home/jrm/Android/Sdk/cmake/3.6.3155560/bin/cmake ../ -G"Android Gradle - Ninja" -DANDROID_ABI=armeabi-v7a -DANDROID_NDK=/home/jrm/Android/Sdk/ndk-bundle -DCMAKE_BUILD_TYPE=Release -DCMAKE_MAKE_PROGRAM=/home/jrm/Android/Sdk/cmake/3.6.3155560/bin/ninja -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_TOOLCHAIN_FILE=/home/jrm/Android/Sdk/ndk-bundle/build/cmake/android.toolchain.cmake -DANDROID_NATIVE_API_LEVEL=21 -DCMAKE_CXX_FLAGS=-std=c++11 -DPYTHON_VERSION=2.7.13 -DENABLE_CODECS_JP=OFF -DENABLE_CODECS_KR=OFF -DENABLE_CODECS_TW=OFF -DENABLE_MULTIBYTECODEC=OFF -DENABLE_CODECS_CN=OFF -DENABLE_CODECS_HK=OFF -DENABLE_CODECS_ISO2022=OFF -DINSTALL_TEST=OFF -DBUILD_LIBPYTHON_SHARED=ON
	#cd android/python/build && /home/jrm/Android/Sdk/cmake/3.6.3155560/bin/cmake ../ -G"Android Gradle - Ninja" -DANDROID_ABI=armeabi-v7a -DANDROID_NDK=/home/jrm/Android/Sdk/ndk-bundle -DCMAKE_BUILD_TYPE=Release -DCMAKE_MAKE_PROGRAM=/home/jrm/Android/Sdk/cmake/3.6.3155560/bin/ninja -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_TOOLCHAIN_FILE=/home/jrm/Android/Sdk/ndk-bundle/build/cmake/android.toolchain.cmake -DANDROID_NATIVE_API_LEVEL=21 -DCMAKE_CXX_FLAGS=-std=c++11 -DPYTHON_VERSION=2.7.13 -DENABLE_CODECS_JP=OFF -DENABLE_CODECS_KR=OFF -DENABLE_CODECS_TW=OFF -DENABLE_MULTIBYTECODEC=OFF -DENABLE_CODECS_CN=OFF -DENABLE_CODECS_HK=OFF -DENABLE_CODECS_ISO2022=OFF -DINSTALL_TEST=OFF -DBUILD_LIBPYTHON_SHARED=ON -DBUILD_EXTENSIONS_AS_BUILTIN=ON -DENABLE_CTYPES_TEST=OFF -DENABLE_TESTCAPI=OFF
	#cd android/python/ && cp TryRunResults.cmake build/TryRunResults.cmake
	#cd android/python/build && /home/jrm/Android/Sdk/cmake/3.6.3155560/bin/ninja -v
	# -DBUILD_EXTENSIONS_AS_BUILTIN=ON -DENABLE_CTYPES_TEST=OFF -DENABLE_TESTCAPI=OFF
	# -DHAVE_SSIZE_T -DPY_FORMAT_SIZE_T="l" -DPY_FORMAT_LONG_LONG="ll"

clean-android:
	cd python-for-android/ && python p4a.py clean_dists
	cd python-for-android/ && python p4a.py clean_builds

run-android:
	cd python-for-android/ && python p4a.py apk --arch=armeabi-v7a --private ../src --package=org.example.demoapp --name "Demo Application" --dist-name="Demo" --version 0.1 --requirements=python2crystax,pyjnius,atom,ply,enaml --android-api=25 --bootstrap=enaml --sdk-dir=/home/jrm/Android/Sdk --ndk-dir=/home/jrm/Android/Crystax/crystax-ndk-10.3.2/ --ndk-platform=21 --copy-libs
	adb install -r DemoApplication-0.1-debug.apk
	adb shell am start -n org.example.demoapp/org.kivy.android.PythonActivity
	adb logcat
