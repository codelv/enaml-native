import os
import sh
import time
import pytest
from os.path import exists
from utils import cd, source_activated


def cleanup():
    if exists('tmp/test_cli/'):
        sh.rm('-R', 'tmp/test_cli/')


def test_init_build():
    """ Tests that the CLI can properly init a new project install packages and build it
        1. `enaml-native init` works to create a new project
        2. `enaml-native install <package>` properly installs and links modules
        3. `enaml-native build-python` succeeds
        4. `enaml-native build-android` succeeds
    """
    if 'TRAVIS' in os.environ:
        return  #: Doesn't work on travis
    try:
        enamlnative = sh.Command('enaml-native')
        bundle_id = 'com.mycompany.myapp'
        print(enamlnative('init', 'MyApp', bundle_id, 'tmp/test_cli/'))
        with cd('tmp/test_cli/MyApp'):
            #: Make sure files are moved to the correct package
            with cd("android/app/src/"):
                for source in ['main/java/com/mycompany/myapp/MainActivity.java',
                               'main/java/com/mycompany/myapp/MainApplication.java']:
                    assert exists(source), "MainActivity and MainApplication" \
                                           "weren't moved to the correct package."

                    found = False
                    with open(source) as f:
                        for line in f:
                            if line.rstrip() == "package {};".format(bundle_id):
                                found = True
                                break
                    assert found, "Init didn't properly rename the java package in {}".format(source)

                #: Check that the manifest was updated properly
                assert exists("main/AndroidManifest.xml"), "AndroidManifest was not copied"
                found = False
                with open("main/AndroidManifest.xml") as f:
                    for line in f:
                        if 'package="{}"'.format(bundle_id) in line:
                            found = True
                            break
                assert found, "Bundle Id was not updated in the Android manifest"

            #: Now activate the venv and try to build
            with source_activated('venv', 'enaml-native') as enamlnative:
                print(enamlnative('install', 'p4a-nucleic'))
                print(enamlnative('install', 'p4a-msgpack'))
                print(enamlnative('list'))

                #: TODO: Should not have to build twice!
                #: Now build python
                print(enamlnative('build-python'))

                #: Build and do a gradle sync, this will NOT include jni and native libs!
                print(enamlnative('build-android'))

                #: Now build python (again) to put them in the correct spot
                print(enamlnative('build-python'))

                #: Now try to run it and see if it crashes
                #: Requires emulator or device
                assert len(sh.adb('devices').strip().split("\n")) > 0, "No device is connected, " \
                                                                       "can't test the build!"
                #: Flush logcat
                sh.adb('logcat', '--clear')

                #: Do a build and run
                print(enamlnative('run-android'))
                #: Wait a few seconds
                time.sleep(5)

                #: See if python exited (it shouldn't)
                output = sh.bash('-c', 'adb logcat -d | grep pybridge')
                print(output)
                assert "Finalizing the Python interpreter" not in output, "run-android failed:"\
                                                                              "{}".format(output)

    finally:
        cleanup()


# def test_init_install_link():
#     if 'TRAVIS' in os.environ:
#         return  #: Doesn't work on travis
#     try:
#         en_cli = sh.Command('./enaml-native')
#         en_cli('init', 'MyApp', 'com.mycompany.myapp', 'tmp/cli/MyApp')
#         with cd('tmp/cli'):
#             en_cli('install', 'enaml-native-maps')
#
#     finally:
#         cleanup()