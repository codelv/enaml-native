'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 4, 2017

@author: jrm
'''

import re
import os
import sh
import time
import pytest
import json
import requests
from os.path import exists, join
from utils import cd, source_activated

#: Stats
config = {
    'app_built':False,
    'stats': {},
}



def prepare_new_app(config):
    """ Init a new app, build it, and launch it on a connected device.
    
    :param config: 
    :return: 
    """
    app_dir = 'tmp/test_benchmarks/'
    config['app_dir'] = app_dir
    #: Create an app to to test
    if exists(app_dir):
        #: If using an emulator enable forwarding
        if "emulator-" in sh.adb('devices'):
            sh.adb("forward", "tcp:8888", "tcp:8888")

        return  # App already made
    #if config['app_built']:
    #    return  # App already made
    #else:
    #    #: Cleanup the old app
    #    cleanup_app(config)

    enamlnative = sh.Command('./enaml-native')
    print(enamlnative('init', 'Benchmarks', 'com.codelv.enamlnative.benchmarks',
                      'tmp/test_benchmarks/'))

    config['app_built'] = True

    with cd(join(app_dir,'Benchmarks')):
        with source_activated('venv', 'enaml-native') as enamlnative:
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

            #: If using an emulator enable forwarding
            if "emulator-" in sh.adb('devices'):
                sh.adb("forward", "tcp:8888", "tcp:8888")


def cleanup_app(config):
    if os.path.exists(config['app_dir']):
        sh.rm('-R', config['app_dir'])


@pytest.mark.parametrize("platforms, path", [
    (["android"], 'activity_indicator.enaml'),
    (["android"], 'auto_complete_text_view.enaml'),
    (["android"], 'block.enaml'),
    (["android"], 'button.enaml'),
    (["android"], 'calendar_view.enaml'),
    (["android"], 'card_view.enaml'),
    (["android"], 'clocks.enaml'),
    (["android"], 'checkbox.enaml'),
    (["android"], 'chronometer.enaml'),
    (["android"], 'date_picker.enaml'),
    (["android"], 'dialog.enaml'),
    (["android"], 'drawer_layout.enaml'),
    (["android"], 'edit_text.enaml'),
    (["android"], 'flexbox.enaml'),
    (["android"], 'icon.enaml'),
    (["android"], 'mapview.enaml'),
    (["android"], 'pager_tab_strip.enaml'),
    (["android"], 'picker.enaml'),
    (["android"], 'progress_bar.enaml'),
    (["android"], 'radio_buttons.enaml'),
    (["android"], 'rating_bar.enaml'),
    (["android"], 'seekbar.enaml'),
    (["android"], 'snackbar.enaml'),
    (["android"], 'spacer.enaml'),
    (["android"], 'spinner.enaml'),
    (["android"], 'switch.enaml'),
    (["android"], 'swipe_refresh.enaml'),
    (["android"], 'tabs.enaml'),
    (["android"], 'toast.enaml'),
    (["android"], 'view_pager.enaml'),
    (["android"], 'webview.enaml'),
])
def test_examples_for_real(platforms, path):
    """ This builds an actuall app and does full system benchmarks on loading app examples 
    
    
    """
    if 'TRAVIS' in os.environ:
        return  #: Doesn't work on travis

    #: Pretty hackish but whatever
    prepare_new_app(config)

    #: Load the code
    dir_path = os.path.abspath(os.path.split(os.path.dirname(__file__))[0])
    enaml_file = os.path.join(dir_path, 'examples', os.path.normpath(path))

    with open(enaml_file, 'rb') as f:
        source = f.read()

    #: Trigger a reload
    r = requests.post("http://localhost:8888/", json={
        "type": "reload",
        "files": {'view.enaml': source},
    }).json()
    assert r['ok'], "Failed to reload {}!".format(enaml_file)

    #: TODO need a way to know when everything is done...
    #: should read the log unil it stops
    time.sleep(5)
    #: Flush logcat

    #: Save it
    stats = parse_stats(sh.adb('logcat', '-d'))
    config['stats'][enaml_file] = stats

    #: Save it
    data = json.dumps(config,indent=2)
    with open('tmp/stats.json', 'w') as f:
        f.write(data)

    #: TODO: Now compare it to the baseline



def parse_stats(output):
    """ Parses logcat output and returns the stats """
    lines = [line for line in output if "[Stats]" in line]
    stats = {
        'totals': {'time': 0, 'tasks': 0, 'avg': 0}
    }
    for line in lines:
        m = re.search(r'\((\d+) ms\).+\((\d+)\).+\((\d+) us.+\)', line)
        if not m:
            continue
        dt, tasks, avg = map(int, m.groups())
        if 'totals' in line:
            stats['totals'] = {'time': dt, 'tasks': tasks, 'avg': avg}
    return stats




