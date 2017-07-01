ARCH=armeabi-v7a
SDK_DIR=/home/jrm/Android/Sdk
NDK_DIR=/home/jrm/Android/Crystax/crystax-ndk-10.3.2
BUNDLE_ID=com.jventura.pyapp
REQS=python2crystax,pyjnius,atom,ply,enaml,msgpack-python
#,tornado
#,twisted,incremental,constantly

clean-python:
	cd python-for-android/ && python p4a.py clean_dists
	cd python-for-android/ && python p4a.py clean_builds

build-python:
	cd android/app/src/main/jni && $(NDK_DIR)/ndk-build
	cd python-for-android/ && python p4a.py apk --arch=$(ARCH) --private=../src --package=$(BUNDLE_ID) --name="Enaml Native Application" --dist-name="enaml-native" --version=0.1 --requirements=$(REQS) --android-api=25 --bootstrap=enaml --sdk-dir=$(SDK_DIR) --ndk-dir=$(NDK_DIR) --ndk-platform=21 --copy-libs
	
copy-python:
	cp -R ~/.local/share/python-for-android/dists/enaml-native/libs/$(ARCH) android/app/src/main/libs
	cp -R ~/.local/share/python-for-android/dists/enaml-native/python/modules android/app/src/main/python/$(ARCH)
	cp -R ~/.local/share/python-for-android/dists/enaml-native/python/site-packages android/app/src/main/python/$(ARCH)
	
pull-cache:
	#: Pull cache file from device
	adb root
	cd android/app/src/main/assets/python/ && adb pull /data/user/0/$(BUNDLE_ID)/assets/python/site-packages/jnius/reflect.javac

install-cache:
	cp android/app/src/main/assets/python/reflect.javac android/app/src/main/assets/python/site-packages/jnius/
	
install-assets:
	#: Install assets for a specific arch
	#: Remove old
	cd android/app/src/main/assets/python/ && rm -R modules && rm -R site-packages
	#: Install new 
	cp -R android/app/src/main/python/$(ARCH)/modules android/app/src/main/assets/python/
	cp -R android/app/src/main/python/$(ARCH)/site-packages android/app/src/main/assets/python/ 
	#: Copy cache to correct place
	cp android/app/src/main/assets/python/reflect.javac android/app/src/main/assets/python/site-packages/jnius/

clean-assets:
	#: Remove any unused modules
	#cd android/app/src/main/assets/python/site-packages && 	find . -type f -name '*.py' -delete
	#cd android/app/src/main/assets/python/site-packages && 	find . -type f -name '*.pyc' -delete
	cd android/app/src/main/assets/python/site-packages && 	find . -type f -name '*.pyo' -delete
	cd android/app/src/main/assets/python/site-packages && 	rm -R enaml/qt
	cd android/app/src/main/assets/python/site-packages && 	rm -R *.egg-info
	cd android/app/src/main/assets/python/site-packages && 	rm -R *.dist-info
	cd android/app/src/main/assets/python/site-packages && 	rm -R tests
	cd android/app/src/main/assets/python/site-packages && 	rm -R usr

all-python: clean-python build-python copy-python install-assets clean-assets

run-android:
	adb install -r EnamlNativeApplication-0.1-debug.apk
	adb shell am start -n org.example.enamlnative/org.kivy.android.PythonActivity
	adb logcat
