import sh
import pytest
from os.path import exists


def cleanup():
    if exists('tmp/cli/'):
        sh.rm('-R', 'tmp/cli/')


def test_init_build_run():
    """ Make sure init works"""
    try:
        return  #: Doesn't work on travis
        en_cli = sh.Command('./enaml-native')
        en_cli('init', 'MyApp', 'com.mycompany.myapp', 'tmp/cli/MyApp')
        assert exists('tmp/cli/MyApp/android/app/src/main/java/com/mycompany/myapp/MainActivity.java')
        assert exists('tmp/cli/MyApp/android/app/src/main/java/com/mycompany/myapp/MainApplication.java')
    finally:
        cleanup()