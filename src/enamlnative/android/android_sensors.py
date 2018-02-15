"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Jan 28, 2018

@author: jrm
"""
from atom.api import ForwardInstance, Int, set_default

from .bridge import JavaBridgeObject, JavaCallback, JavaMethod
from .android_content import Context, SystemService
from .app import AndroidApplication


class Sensor(JavaBridgeObject):
    """ A wrapper for an Android sensor. This should be retrieved using
    the `Sensor.get(sensor_type)` method.
    
    Examples
    --------
    
    # In a function with an @inlineCallbacks or @coroutine decorator
    def on_data(data):
        # Handle data here...
        # data is a dict with keys
        # {'acc': <accuracy>, 'data': [v1, v2, ...], 'sensor': id, 'time': t}
    
    def on_ready(sensor):
        if sensor is not None:
            sensor.start(callback=on_data)
            # ...
            sensor.stop()
    
    """
    __nativeclass__ = set_default('android.hardware.Sensor')

    #: Reference to the sensor manager
    manager = ForwardInstance(lambda: SensorManager)

    #: Sensor type
    type = Int()

    TYPE_ACCELEROMETER = 1
    TYPE_MAGNETIC_FIELD = 2
    TYPE_ORIENTATION = 3  # Depreciated
    TYPE_GYROSCOPE = 4
    TYPE_LIGHT = 5
    TYPE_PRESSURE = 6
    TYPE_TEMPERATURE = 7  # Depreciated Use ambient temp instead
    TYPE_PROXIMITY = 8
    TYPE_GRAVITY = 9
    TYPE_LINEAR_ACCELERATION = 10
    TYPE_ROTATION_VECTOR = 11
    TYPE_RELATIVE_HUMIDITY = 12
    TYPE_AMBIENT_TEMPERATURE = 13
    TYPE_MAGNETIC_FIELD_UNCALIBRATED = 14
    TYPE_GAME_ROTATION_VECTOR = 15
    TYPE_GYROSCOPE_UNCALIBRATED = 16
    TYPE_SIGNIFICANT_MOTION = 17
    TYPE_STEP_DETECTOR = 18
    TYPE_STEP_COUNTER = 19
    TYPE_GEOMAGNETIC_ROTATION_VECTOR = 20
    TYPE_HEART_RATE = 21
    TYPE_POSE_6DOF = 28  # Requires API 24+
    TYPE_STATIONARY_DETECT = 29 # Requires API 24+
    TYPE_MOTION_DETECT = 30  # Requires API 24+
    TYPE_HEART_BEAT = 31  # Requires API 24+
    TYPE_LOW_LATENCY_OFFBODY_DETECT = 34  # Requires API 26+

    SENSOR_DELAY_NORMAL = 3
    SENSOR_DELAY_UI = 2
    SENSOR_DELAY_GAME = 1
    SENSOR_DELAY_FASTEST = 0

    getFifoMaxEventCount = JavaMethod(returns='int')
    getFifoReservedEventCount = JavaMethod(returns='int')
    getMaximumRange = JavaMethod(returns='float')
    getMaxDelay = JavaMethod(returns='int')
    getMinDelay = JavaMethod(returns='int')
    getName = JavaMethod(returns='java.lang.String')
    getPower = JavaMethod(returns='float')
    getReportingMode = JavaMethod(returns='int')
    getResolution = JavaMethod(returns='float')
    getVendor = JavaMethod(returns='java.lang.String')
    getVersion = JavaMethod(returns='int')
    getType = JavaMethod(returns='int')
    getStringType = JavaMethod(returns='java.lang.String')
    isWakeUpSensor = JavaMethod(returns='boolean')

    # -------------------------------------------------------------------------
    # SensorEventListener API
    # -------------------------------------------------------------------------
    onSensorChanged = JavaCallback('android.hardware.SensorEvent')
    onAccuracyChanged = JavaCallback('android.hardware.Sensor', 'int')

    @classmethod
    def get(cls, sensor_type):
        """ Shortcut that acquires the default Sensor of a given type. 
        
        Parameters
        ----------
            sensor_type: int
                Type of sensor to get.
        
        Returns
        -------
            result: Future 
                A future that resolves to an instance of the Sensor or None
                if the sensor is not present or access is not allowed.
        
        """
        app = AndroidApplication.instance()
        f = app.create_future()

        def on_sensor(sid, mgr):
            if sid is None:
                f.set_result(None)
            else:
                f.set_result(Sensor(__id__=sid, manager=mgr, type=sensor_type))

        SensorManager.get().then(
            lambda sm: sm.getDefaultSensor(sensor_type).then(
                lambda sid, sm=sm:on_sensor(sid, sm)))

        return f

    def start(self, callback, rate=SENSOR_DELAY_NORMAL):
        """ Start listening to sensor events. Sensor event data depends
        on the type of sensor that was given to 
        
        Parameters
        ----------
            callback: Callable
                A callback that takes one argument that will be passed
                the sensor data. Sensor data is a dict with data based on
                the type of sensor.
            rate: Integer
                How fast to update. One of the Sensor.SENSOR_DELAY values   
        
        Returns
        -------
            result: Future
                A future that resolves to whether the register call
                completed.
        
        """
        if not self.manager:
            raise RuntimeError(
                "Cannot start a sensor without a SensorManager!")
        self.onSensorChanged.connect(callback)
        return self.manager.registerListener(self.getId(), self, rate)

    def stop(self):
        """ Stop listening to sensor events. This should be done in
        on resume.
        """
        self.manager.unregisterListener(self.getId(), self)


class SensorManager(SystemService):
    SERVICE_TYPE = Context.SENSOR_SERVICE
    __nativeclass__ = set_default('android.hardware.SensorManager')

    registerListener = JavaMethod('android.hardware.SensorEventListener',
                                  'android.hardware.Sensor', 'int',
                                  returns='boolean')
    unregisterListener = JavaMethod('android.hardware.SensorEventListener',
                                    'android.hardware.Sensor')

    getDefaultSensor = JavaMethod('int', returns='android.hardware.Sensor')
    getSensorList = JavaMethod('int', returns='java.util.List')

