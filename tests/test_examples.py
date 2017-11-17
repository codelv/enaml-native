'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 4, 2017

@author: jrm
'''
import os
import enaml
import pytest
from app import MockApplication
from utils import load

@pytest.mark.parametrize("platforms, path", [
    (["android", "ios"], 'activity_indicator.enaml'),
    (["android"], 'auto_complete_text_view.enaml'),
    (["android"], 'block.enaml'),
    (["android", "ios"], 'button.enaml'),
    (["android"], 'calendar_view.enaml'),
    (["android"], 'card_view.enaml'),
    (["android"], 'clocks.enaml'),
    #(["android"], 'charts.enaml'), # now requires enaml-native-charts
    (["android"], 'checkbox.enaml'),
    (["android"], 'chronometer.enaml'),
    (["android"], 'date_picker.enaml'),
    (["android"], 'dialog.enaml'),
    (["android"], 'drawer_layout.enaml'),
    (["android", "ios"], 'edit_text.enaml'),
    (["android"], 'flexbox.enaml'),
    (["android"], 'icon.enaml'),
    (["android"], 'keyboard.enaml'),
    #(["android"], 'mapview.enaml'),# now requires enaml-native-maps
    (["android"], 'pager_tab_strip.enaml'),
    (["android"], 'picker.enaml'),
    (["android", "ios"], 'progress_bar.enaml'),
    (["android"], 'radio_buttons.enaml'),
    (["android"], 'rating_bar.enaml'),
    (["android"], 'seekbar.enaml'),
    (["android"], 'snackbar.enaml'),
    (["android"], 'spacer.enaml'),
    (["android"], 'spinner.enaml'),
    (["android", "ios"], 'switch.enaml'),
    (["android"], 'swipe_refresh.enaml'),
    (["android"], 'tabs.enaml'),
    (["android"], 'toast.enaml'),
    (["android"], 'view_pager.enaml'),
    (["android"], 'webview.enaml'),
])
def test_examples(platforms, path):
    #: Load
    dir_path = os.path.abspath(os.path.split(os.path.dirname(__file__))[0])
    enaml_file = os.path.join(dir_path, 'examples', os.path.normpath(path))

    with enaml.imports():
        with open(enaml_file,'rb') as f:
            ContentView = load(f.read())

    #: Run for each platform
    for platform in platforms:
        app = MockApplication.instance(platform)
        app.view = ContentView()
        app.run()


def test_demo_app():
    with enaml.imports():
        with open('src/apps/view.enaml','rb') as f:
            ContentView = load(f.read())

        app = MockApplication.instance('android')
        app.view = ContentView()
        app.run()



