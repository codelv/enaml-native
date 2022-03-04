""" Mock nativehooks for testing purposes

"""

import msgpack
from enaml.application import Application

MOCK_BUILD_INFO = {
    "DISPLAY_DENSITY": 2.65,
    "DISPLAY_WIDTH": 790,
    "DISPLAY_HEIGHT": 400,
    "DISPLAY_ORIENTATION": 1,
    "SDK_INT": 32,
}

#: List of messages, saved so tests can access them
messages = []

#: Event set when the view has been called
shown = None


def publish(data: str):
    from enamlnative.android.app import AndroidApplication
    from enamlnative.ios.app import IPhoneApplication

    app = Application.instance()
    events = msgpack.loads(data)
    messages.extend(events)
    print("------------ Start processing --------------")
    if isinstance(app, AndroidApplication):
        publish_android(app, events)
    elif isinstance(app, IPhoneApplication):
        publish_ios(app, events)
    print("------------ Done processing --------------")


def publish_android(app: Application, events: list):
    for cmd, args in events:
        response = None
        if cmd == "m":
            obj, result_id, cache_id, fname, fargs = args
            if fname == "getBuildInfo":
                response = (0, result_id, "set_result", [("_", MOCK_BUILD_INFO)])
            elif fname == "getWindow":
                response = (0, result_id, "set_result", [("window", result_id)])
            elif obj == -1 and fname == "setView":
                shown.set_result(True)
        if cmd == "sm":
            cls, result_id, cache_id, fname, fargs = args
            if cls == "android.widget.Toast" and fname == "makeText":
                response = (0, result_id, "set_result", [("toast", result_id)])
        if response:
            # Simulate android/ios bridge sending response back
            events = [("event", response)]
            app.on_events(msgpack.dumps(events))
    print("------------ Native done processing --------------")


def publish_ios(app: Application, evens: list):
    pass
