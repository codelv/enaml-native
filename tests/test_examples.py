"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Oct 4, 2017

@author: jrm
"""
import enaml
import pytest
import nativehooks
from glob import glob
from pydoc import locate, ErrorDuringImport
from enaml.application import Application
from enamlnative.android.app import AndroidApplication

try:
    import iconify
except ImportError:
    iconify = None

try:
    import googlemaps
except ImportError:
    googlemaps = None

try:
    import charts.android
except ImportError:
    charts = None

from utils import load

with enaml.imports():
    from activity import ExampleActivity


@pytest.fixture
def native_app():
    yield
    nativehooks.messages = []
    Application._instance = None  # Clear after every run


@pytest.mark.parametrize("path", glob("examples/*.enaml"))
async def test_examples(native_app, path):
    example = path[:-6].replace("/", ".")  # Remove example/ and .enaml

    if "thermostat" in example:
        return pytest.skip("thermostat example needs updated")

    app = AndroidApplication(debug=True)
    with enaml.imports():
        try:
            ContentView = locate(f"{example}.ContentView")
        except ErrorDuringImport as e:
            msg = f"{e}"
            if iconify is None and "iconify" in msg:
                return pytest.skip("enaml-native-icons is not installed")
            if googlemaps is None and "googlemaps" in msg:
                return pytest.skip("enaml-native-maps is not installed")
            if charts is None and "charts" in msg:
                return pytest.skip("enaml-native-charts is not installed")
            raise

    app.activity = ExampleActivity(example=ContentView())
    f = nativehooks.shown = app.create_future()

    def on_error(event):
        f.set_exception(event["value"])

    app.observe("error_occurred", on_error)

    # f.add_done_callback(lambda f: app.stop())
    # Add fail timeout
    app.timed_call(5 * 1000, lambda: f.set_result(False))
    app.deferred_call(app.activity.start)
    assert await f


@pytest.mark.skip(reason="Disabled")
def test_demo_app(enamlnative_app):
    app = AndroidApplication(debug=True)
    with open("examples/demo/view.enaml") as f:
        ContentView = load(f.read())
    app.activity = ExampleActivity(example=ContentView())
    app.run()


@pytest.mark.skip(reason="Disabled")
def test_playground_app(enamlnative_app):
    app = AndroidApplication(debug=True)

    with open("examples/playground/view.enaml") as f:
        ContentView = load(f.read())

    app.activity = ExampleActivity(example=ContentView())
    app.run()
