"""
Copyright (c) 2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on March 4, 2022
"""

from typing import Optional, Union
from .android_content import Context, SystemService
from .bridge import JavaBridgeObject, JavaMethod, JavaStaticMethod


class VibrationEffect(JavaBridgeObject):
    __nativeclass__ = "android.os.VibrationEffect"
    DEFAULT_AMPLITUDE = -1
    EFFECT_CLICK = 0
    EFFECT_DOUBLE_CLICK = 1
    EFFECT_TICK = 2
    EFFECT_HEAVY_CLICK = 5

    createOneShot = JavaStaticMethod("long", int, returns="android.os.VibrationEffect")
    createPredefined = JavaStaticMethod(int, returns="android.os.VibrationEffect")
    createWaveform = JavaStaticMethod(
        "[long", list[int], int, returns="android.os.VibrationEffect"
    )


class Vibrator(SystemService):
    __nativeclass__ = "android.os.Vibrator"

    SERVICE_TYPE = Context.VIBRATOR_SERVICE

    cancel = JavaMethod()

    vibrate_ = JavaMethod("long")
    vibrate__ = JavaMethod(VibrationEffect)

    def vibrate(
        self,
        duration: int,
        effect: Optional[Union[int, VibrationEffect]] = None,
        amplitude: int = VibrationEffect.DEFAULT_AMPLITUDE,
    ):
        app = self.__app__
        assert app is not None
        activity = app.activity
        assert activity is not None
        api_level = activity.api_level
        if api_level >= 26:
            if effect is None:
                effect = VibrationEffect.createOneShot(duration, amplitude)
            elif isinstance(effect, int):
                effect = VibrationEffect.createPredefined(effect)
            self.vibrate__(effect)
        else:
            self.vibrate_(duration)
