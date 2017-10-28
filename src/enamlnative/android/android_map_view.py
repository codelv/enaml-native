'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 10, 2017

@author: jrm
'''
from atom.api import Typed, Instance, Dict, Bool, set_default

from enamlnative.widgets.map_view import (
    ProxyMapView, ProxyMapMarker, ProxyMapCircle, ProxyMapPolyline, ProxyMapPolygon
)
from enamlnative.core import bridge

from .android_toolkit_object import AndroidToolkitObject
from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .android_fragment import FragmentTransaction, FragmentManager
from .android_utils import ArrayList
from .bridge import JavaBridgeObject, JavaMethod, JavaStaticMethod, JavaCallback, JavaProxy
from .api import LocationManager


class ConnectionResult:
    SUCCESS = 0
    API_UNAVAILABLE = 16
    CANCELED = 13
    DEVELOPER_ERROR = 10
    DRIVE_EXTERNAL_STORAGE_REQUIRED = 1500
    INTERNAL_ERROR = 8
    INTERRUPTED = 15
    INVALID_ACCOUNT = 5
    LICENSE_CHECK_FAILED = 11
    NETWORK_ERROR = 7
    RESOLUTION_REQUIRED = 6
    RESTRICTED_PROFILE = 20
    SERVICE_DISABLED = 3
    SERVICE_INVALID = 9
    SERVICE_MISSING = 1
    SERVICE_MISSING_PERMISSION = 19
    SERVICE_UPDATING = 18
    SERVICE_VERSION_UPDATE_REQUIRED = 2
    SIGN_IN_FAILED = 17
    SIGN_IN_REQUIRED = 4
    TIMEOUT = 14


class LatLngList(ArrayList):
    """ A ArrayList<LatLng> that handles changes from an atom ContainerList"""

    def refresh_points(self, points):
        coordinates = [LatLng(*p) for p in points]
        self.clear()

        #: Must manually encode these the bridge currently doesnt try as it's slower
        self.addAll([bridge.encode(c) for c in coordinates])

    def handle_change(self, change):
        """ Handle changes from atom ContainerLists """
        op = change['operation']
        if op in 'append':
            self.add(len(change['value']), LatLng(*change['item']))
        elif op == 'insert':
            self.add(change['index'], LatLng(*change['item']))
        elif op == 'extend':
            points = [LatLng(*p) for p in change['items']]
            self.addAll([bridge.encode(c) for c in points])
        elif op == '__setitem__':
            self.set(change['index'], LatLng(*change['newitem']))
        elif op == 'pop':
            self.remove(change['index'])
        else:
            raise NotImplementedError("Unsupported change operation {}".format(op))


class GoogleMap(JavaBridgeObject):

    addCircle = JavaMethod('com.google.android.gms.maps.model.CircleOptions',
                       returns='com.google.android.gms.maps.model.Circle')
    addMarker = JavaMethod('com.google.android.gms.maps.model.MarkerOptions',
                           returns='com.google.android.gms.maps.model.Marker')
    addPolyline = JavaMethod('com.google.android.gms.maps.model.PolylineOptions',
                           returns='com.google.android.gms.maps.model.Polyline')
    addPolygon = JavaMethod('com.google.android.gms.maps.model.PolygonOptions',
                             returns='com.google.android.gms.maps.model.Polygon')
    onMapReady = JavaCallback('com.google.android.gms.maps.GoogleMap')

    animateCamera = JavaMethod('com.google.android.gms.maps.CameraUpdate')

    setLatLngBoundsForCameraTarget = JavaMethod('com.google.android.gms.maps.model.LatLngBounds')
    setMapType = JavaMethod('int')
    setMaxZoomPreference = JavaMethod('float')
    setMinZoomPreference = JavaMethod('float')
    setMyLocationEnabled = JavaMethod('boolean')
    setBuildingsEnabled = JavaMethod('boolean')
    setIndoorEnabled = JavaMethod('boolean')
    setTrafficEnabled = JavaMethod('boolean')

    setOnCameraChangeListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnCameraChangeListener')
    onCameraChange = JavaCallback('com.google.android.gms.maps.model.CameraPosition')
    setOnCameraMoveStartedListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnCameraMoveStartedListener')
    onCameraMoveStarted = JavaCallback('int')
    setOnCameraMoveStartedListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnCameraMoveStartedListener')
    setOnCameraMoveCanceledListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnCameraMoveCanceledListener')
    onCameraMoveCanceled = JavaCallback()
    setOnCameraIdleListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnCameraIdleListener')
    onCameraIdle = JavaCallback()

    CAMERA_REASON_GESTURE = 1
    CAMERA_REASON_API_ANIMATION = 2
    CAMERA_REASON_DEVELOPER_ANIMATION = 3


    setOnMarkerClickListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnMarkerClickListener')
    onMarkerClick = JavaCallback('com.google.android.gms.maps.model.Marker', returns='boolean')

    setOnMarkerDragListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnMarkerDragListener')
    onMarkerDrag = JavaCallback('com.google.android.gms.maps.model.Marker')
    onMarkerDragEnd = JavaCallback('com.google.android.gms.maps.model.Marker')
    onMarkerDragStart = JavaCallback('com.google.android.gms.maps.model.Marker')

    #: Info windows
    setOnInfoWindowClickListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnInfoWindowClickListener')
    onInfoWindowClick = JavaCallback('com.google.android.gms.maps.model.Marker')
    setOnInfoWindowCloseListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnInfoWindowCloseListener')
    onInfoWindowClose = JavaCallback('com.google.android.gms.maps.model.Marker')
    setOnInfoWindowLongClickListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnInfoWindowLongClickListener')
    onInfoWindowLongClick = JavaCallback('com.google.android.gms.maps.model.Marker')
    setInfoWindowAdapter = JavaMethod('com.google.android.gms.maps.GoogleMap$InfoWindowAdapter')

    class InfoWindowAdapter(JavaProxy):
        __nativeclass__ = set_default('com.google.android.gms.maps.GoogleMap$InfoWindowAdapter')
        getInfoContents = JavaCallback('com.google.android.gms.maps.model.Marker',
                                       returns='android.view.View')
        getInfoWindow = JavaCallback('com.google.android.gms.maps.model.Marker',
                                       returns='android.view.View')

    #: Map clicks
    setOnMapClickListener = JavaMethod('com.google.android.gms.maps.GoogleMap$OnMapClickListener')
    onMapClick = JavaCallback('com.google.android.gms.maps.model.LatLng')
    setOnMapLongClickListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnMapLongClickListener')
    onMapLongClick = JavaCallback('com.google.android.gms.maps.model.LatLng')

    setOnPolylineClickListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnPolylineClickListener')
    onPolylineClick = JavaCallback('com.google.android.gms.maps.model.Polyline')
    setOnPolygonClickListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnPolygonClickListener')
    onPolygonClick = JavaCallback('com.google.android.gms.maps.model.Polygon')

    setOnCircleClickListener = JavaMethod(
        'com.google.android.gms.maps.GoogleMap$OnCircleClickListener')
    onCircleClick = JavaCallback('com.google.android.gms.maps.model.Circle')

    MAP_TYPE_HYBRID = 4
    MAP_TYPE_NONE = 0
    MAP_TYPE_NORMAL = 1
    MAP_TYPE_SATELLITE = 2
    MAP_TYPE_TERRAIN = 3

    MAP_TYPES = {
        'none': MAP_TYPE_NONE,
        'normal': MAP_TYPE_NORMAL,
        'satellite': MAP_TYPE_SATELLITE,
        'terrain': MAP_TYPE_TERRAIN,
        'hybrid': MAP_TYPE_HYBRID,
    }


class MapsInitializer(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.MapsInitializer')
    initialize = JavaStaticMethod('android.content.Context', returns='int')


class MapFragment(JavaBridgeObject):
    """
        Note: You must add "compile 'com.android.support:cardview-v7:21.0.+'"
              to build.gradle for this to work!
    """
    __nativeclass__ = set_default('com.google.android.gms.maps.SupportMapFragment')
    newInstance = JavaStaticMethod('com.google.android.gms.maps.GoogleMapOptions',
        returns='com.google.android.gms.maps.SupportMapFragment')
    getMapAsync = JavaMethod('com.google.android.gms.maps.OnMapReadyCallback')
    getView = JavaMethod(returns='android.view.View')


class MapView(FrameLayout):
    __nativeclass__ = set_default('com.google.android.gms.maps.SupportMapView')


class GoogleMapOptions(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.GoogleMapOptions')
    ambientEnabled = JavaMethod('boolean')
    camera = JavaMethod('com.google.android.gms.maps.model.CameraPosition')
    compassEnabled = JavaMethod('boolean')
    latLngBoundsForCameraTarget = JavaMethod('com.google.android.gms.maps.model.LatLngBounds')
    liteMode = JavaMethod('boolean')
    mapToolbarEnabled = JavaMethod('boolean')
    mapType = JavaMethod('int')
    maxZoomPreference = JavaMethod('float')
    minZoomPreference = JavaMethod('float')
    rotateGesturesEnabled = JavaMethod('boolean')
    scrollGesturesEnabled = JavaMethod('boolean')
    tiltGesturesEnabled = JavaMethod('boolean')
    zoomControlsEnabled = JavaMethod('boolean')
    zoomGesturesEnabled = JavaMethod('boolean')


class CameraPosition(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.CameraPosition')
    __signature__ = set_default(('com.google.android.gms.maps.model.LatLng',
                                 'float', 'float', 'float'))

class CameraUpdate(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.CameraUpdate')


class CameraUpdateFactory(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.CameraUpdateFactory')
    newCameraPosition = JavaStaticMethod('com.google.android.gms.maps.model.CameraPosition',
                 returns='com.google.android.gms.maps.CameraUpdate')


class LatLng(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.LatLng')
    __signature__ = set_default(('double','double'))


class MapItemBase(JavaBridgeObject):
    setTag = JavaMethod("java.lang.Object")
    setVisible = JavaMethod('boolean')
    setZIndex = JavaMethod('float')
    remove = JavaMethod()


class MapItemOptionsBase(JavaBridgeObject):
    visible = JavaMethod('boolean')
    zindex = JavaMethod('float')


class MarkerOptions(MapItemOptionsBase):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.MarkerOptions')
    alpha = JavaMethod('float')
    anchor = JavaMethod('float', 'float')
    draggable = JavaMethod('boolean')
    flat = JavaMethod('boolean')
    icon = JavaMethod('com.google.android.gms.maps.model.BitMapDescriptor')
    position = JavaMethod('com.google.android.gms.maps.model.LatLng')
    rotation = JavaMethod('float')
    snippet = JavaMethod('java.lang.String')
    title = JavaMethod('java.lang.String')


class Marker(MapItemBase):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.Marker')
    setAlpha = JavaMethod('float')
    setAnchor = JavaMethod('float', 'float')
    setDraggable = JavaMethod('boolean')
    setFlat = JavaMethod('boolean')
    setIcon = JavaMethod('com.google.android.gms.maps.model.BitMapDescriptor')
    setPosition = JavaMethod('com.google.android.gms.maps.model.LatLng')
    setRotation = JavaMethod('float')
    setSnippet = JavaMethod('java.lang.String')
    setTitle = JavaMethod('java.lang.String')
    showInfoWindow = JavaMethod()
    hideInfoWindow = JavaMethod()


class CircleOptions(MapItemOptionsBase):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.CircleOptions')
    radius = JavaMethod('double')
    clickable = JavaMethod('boolean')
    center = JavaMethod('com.google.android.gms.maps.model.LatLng')
    fillColor = JavaMethod('android.graphics.Color')
    strokeColor = JavaMethod('android.graphics.Color')
    strokeWidth = JavaMethod('float')


class Circle(MapItemBase):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.Circle')
    setClickable = JavaMethod('boolean')
    setCenter = JavaMethod('com.google.android.gms.maps.model.LatLng')
    setRadius = JavaMethod('double')
    setFillColor = JavaMethod('android.graphics.Color')
    setStrokeColor = JavaMethod('android.graphics.Color')
    setStrokeWidth = JavaMethod('float')


class PolylineOptions(MapItemOptionsBase):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.PolylineOptions')
    #add = JavaMethod('com.google.android.gms.maps.model.LatLng')
    add = JavaMethod('[Lcom.google.android.gms.maps.model.LatLng;')
    addAll = JavaMethod('java.lang.Iterable')
    clickable = JavaMethod('clickable')
    color = JavaMethod('android.graphics.Color')
    endCap = JavaMethod('com.google.android.gms.maps.model.Cap')
    geodesic = JavaMethod('boolean')
    jointType = JavaMethod('int')
    startCap = JavaMethod('com.google.android.gms.maps.model.Cap')
    width = JavaMethod('float')


class ButtCap(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.ButtCap')


class SquareCap(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.SquareCap')


class RoundCap(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.RoundCap')


class Polyline(MapItemBase):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.Polyline')
    setClickable = JavaMethod('boolean')
    setColor = JavaMethod('android.graphics.Color')
    setGeodesic = JavaMethod('boolean')
    setPoints = JavaMethod('java.util.List')
    setEndCap = JavaMethod('com.google.android.gms.maps.model.Cap')
    setStartCap = JavaMethod('com.google.android.gms.maps.model.Cap')
    setJointType = JavaMethod('int')
    setWidth = JavaMethod('float')

    JOINT_TYPE_DEFAULT = 0
    JOINT_TYPE_BEVEL = 1
    JOINT_TYPE_ROUND = 2
    JOINT_TYPES = {
        '': JOINT_TYPE_DEFAULT,
        'bevel': JOINT_TYPE_BEVEL,
        'round': JOINT_TYPE_ROUND
    }

    CAPS = {
        'butt': ButtCap,
        'round': RoundCap,
        'square': SquareCap,
    }


class PolygonOptions(MapItemOptionsBase):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.PolygonOptions')
    clickable = JavaMethod('clickable')
    fillColor = JavaMethod('android.graphics.Color')
    #add = JavaMethod('com.google.android.gms.maps.model.LatLng')
    add = JavaMethod('[Lcom.google.android.gms.maps.model.LatLng;')
    addAll = JavaMethod('java.lang.Iterable')
    addHole = JavaMethod('java.lang.Iterable')
    geodesic = JavaMethod('boolean')
    strokeColor = JavaMethod('android.graphics.Color')
    strokeJointType = JavaMethod('int')
    strokeWidth = JavaMethod('float')


class Polygon(MapItemBase):
    __nativeclass__ = set_default('com.google.android.gms.maps.model.Polygon')
    setClickable = JavaMethod('boolean')
    setFillColor = JavaMethod('android.graphics.Color')
    setGeodesic = JavaMethod('boolean')
    setHoles = JavaMethod('java.util.List')
    setPoints = JavaMethod('java.util.List')
    setStrokeColor = JavaMethod('android.graphics.Color')
    setStrokeJointType = JavaMethod('int')
    setStrokeWidth = JavaMethod('float')


class AndroidMapView(AndroidFrameLayout, ProxyMapView):
    """ An Android implementation of an Enaml ProxyMapView.

    """

    #: Holder
    widget = Typed(FrameLayout)

    #: A reference to the widget created by the proxy.
    fragment = Typed(MapFragment)

    #: Map options
    options = Typed(GoogleMapOptions)

    #: Map instance
    map = Typed(GoogleMap)

    #: TODO: Lookup table for markers
    markers = Dict()

    #: Camera updating
    _update_blocked = Bool()

    #: Info window adapter
    adapter = Typed(GoogleMap.InfoWindowAdapter)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.init_options()

        #: Retrieve the actual map
        MapFragment.newInstance(self.options).then(self.on_map_fragment_created)

        #: Holder for the fragment
        self.widget = FrameLayout(self.get_context())

        #: I wrote this a few days ago and already forget how this hack works... lol
        #: We can't simply get a map reference using getMapAsync in the return value like we
        #: normally do with a normal call function return value.
        #: The bridge design was modified to store an object that cannot be decoded normally (via a
        #: standard Bridge.Packer) by saving the new object in the cache returning the id of the
        #: handler or proxy that invoked it. This way we can manually create a new id and
        #: pass that "future reference-able" object as our listener. At which point the bridge will
        #: create a reference entry in the cache for us with the of the object we gave it. Once in
        #: the cache we can use it like any bridge object we created.
        self.map = GoogleMap(__id__=bridge.generate_id())

    def init_options(self):
        """ Initialize the underlying map options.

        """
        self.options = GoogleMapOptions()
        d = self.declaration
        self.set_map_type(d.map_type)
        if d.ambient_mode:
            self.set_ambient_mode(d.ambient_mode)
        if d.camera_position or d.camera_zoom or d.camera_tilt or d.camera_bearing:
            self.update_camera()
        if d.map_bounds:
            self.set_map_bounds(d.map_bounds)
        if not d.show_compass:
            self.set_show_compass(d.show_compass)
        if not d.show_zoom_controls:
            self.set_show_zoom_controls(d.show_zoom_controls)
        if not d.show_toolbar:
            self.set_show_toolbar(d.show_toolbar)
        if d.lite_mode:
            self.set_lite_mode(d.lite_mode)
        if not d.rotate_gestures:
            self.set_rotate_gestures(d.rotate_gestures)
        if not d.scroll_gestures:
            self.set_scroll_gestures(d.scroll_gestures)
        if not d.tilt_gestures:
            self.set_tilt_gestures(d.tilt_gestures)
        if not d.zoom_gestures:
            self.set_zoom_gestures(d.zoom_gestures)
        if d.min_zoom:
            self.set_min_zoom(d.min_zoom)
        if d.max_zoom:
            self.set_max_zoom(d.max_zoom)

    def init_map(self):
        """ Add markers, polys, callouts, etc.."""
        d = self.declaration
        if d.show_location:
            self.set_show_location(d.show_location)
        if d.show_traffic:
            self.set_show_traffic(d.show_traffic)
        if d.show_indoors:
            self.set_show_indoors(d.show_indoors)
        if d.show_buildings:
            self.set_show_buildings(d.show_buildings)

        #: Local ref access is faster
        mapview = self.map
        mid = mapview.getId()

        #: Connect signals
        #: Camera
        mapview.onCameraChange.connect(self.on_camera_changed)
        mapview.onCameraMoveStarted.connect(self.on_camera_move_started)
        mapview.onCameraMoveCanceled.connect(self.on_camera_move_stopped)
        mapview.onCameraIdle.connect(self.on_camera_move_stopped)
        mapview.setOnCameraChangeListener(mid)
        mapview.setOnCameraMoveStartedListener(mid)
        mapview.setOnCameraMoveCanceledListener(mid)
        mapview.setOnCameraIdleListener(mid)

        #: Clicks
        mapview.onMapClick.connect(self.on_map_clicked)
        mapview.setOnMapClickListener(mid)
        mapview.onMapLongClick.connect(self.on_map_long_clicked)
        mapview.setOnMapLongClickListener(mid)

        #: Markers
        mapview.onMarkerClick.connect(self.on_marker_clicked)
        mapview.setOnMarkerClickListener(self.map.getId())
        mapview.onMarkerDragStart.connect(self.on_marker_drag_start)
        mapview.onMarkerDrag.connect(self.on_marker_drag)
        mapview.onMarkerDragEnd.connect(self.on_marker_drag_end)
        mapview.setOnMarkerDragListener(mid)

        #: Info window
        mapview.onInfoWindowClick.connect(self.on_info_window_clicked)
        mapview.onInfoWindowLongClick.connect(self.on_info_window_long_clicked)
        mapview.onInfoWindowClose.connect(self.on_info_window_closed)
        mapview.setOnInfoWindowClickListener(mid)
        mapview.setOnInfoWindowCloseListener(mid)
        mapview.setOnInfoWindowLongClickListener(mid)

        #: Polys
        mapview.onPolygonClick.connect(self.on_poly_clicked)
        mapview.onPolylineClick.connect(self.on_poly_clicked)
        mapview.setOnPolygonClickListener(mid)
        mapview.setOnPolylineClickListener(mid)

        #: Circle
        mapview.onCircleClick.connect(self.on_circle_clicked)
        mapview.setOnCircleClickListener(mid)


    def init_info_window_adapter(self):
        """ Initialize the info window adapter. Should only be done if one of the
            markers defines a custom view.
        """
        if self.adapter:
            return  #: Already initialized
        self.adapter = GoogleMap.InfoWindowAdapter()
        self.adapter.getInfoContents.connect(self.on_info_window_contents_requested)
        self.adapter.getInfoWindow.connect(self.on_info_window_requested)
        self.map.setInfoWindowAdapter(self.adapter)

    # --------------------------------------------------------------------------
    # Google Maps API
    # --------------------------------------------------------------------------
    def on_map_fragment_created(self, obj_id):
        """ Create the fragment and pull the map reference when it's loaded. """
        self.fragment = MapFragment(__id__=obj_id)

        #: Setup callback so we know when the map is ready
        self.map.onMapReady.connect(self.on_map_ready)
        self.fragment.getMapAsync(self.map.getId())

        context = self.get_context()

        def on_transaction(id):
            trans = FragmentTransaction(__id__=id)
            trans.add(self.widget.getId(), self.fragment)
            trans.commit()

        def on_fragment_manager(id):
            fm = FragmentManager(__id__=id)
            fm.beginTransaction().then(on_transaction)

        context.widget.getSupportFragmentManager().then(on_fragment_manager)
        # #: Get GoogleMap instance when ready
        # #: Doesn't work...
        # def get_map(result):
        #     print("Maps initializer result: {}".format(result))
        #     if result==ConnectionResult.SUCCESS:
        #         self.fragment.onMapReady.connect(self.on_map_ready)
        #         self.fragment.getMapAsync(self.fragment.getId())
        #     else:
        #         app = self.get_context()
        #         app.show_error("Error getting map: {}".format(result))
        # MapsInitializer.initialize(self.get_context()).then(get_map)

    def on_map_ready(self, map_id):
        #: At this point the map is valid
        self.init_map()

        #: Reload markers
        for child in self.children():
            if isinstance(child, AndroidMapItemBase):
                child.add_to_map(self.map)

    def child_added(self, child):
        if isinstance(child, AndroidMapItemBase):
            child.add_to_map(self.map)
        else:
            super(AndroidMapView, self).child_added(child)

    def child_removed(self, child):
        if isinstance(child, AndroidMapItemBase):
            pass  #: It removes itself
        else:
            super(AndroidMapView, self).child_removed(child)

    def on_map_clicked(self, pos):
        """ Called when the map is clicked """
        d = self.declaration
        d.clicked({
            'click': 'short',
            'position': tuple(pos)
        })

    def on_map_long_clicked(self, pos):
        """ Called when the map is clicked """
        d = self.declaration
        d.clicked({
            'click': 'long',
            'position': tuple(pos)
        })

    # --------------------------------------------------------------------------
    # Camera API
    # --------------------------------------------------------------------------
    def on_camera_move_started(self, reason):
        d = self.declaration
        if reason == GoogleMap.CAMERA_REASON_GESTURE:
            d.dragging = True
        else:
            d.animating = True

    def on_camera_move_stopped(self):
        d = self.declaration
        d.dragging = False
        d.animating = False

    def on_camera_changed(self, camera):
        pos, zoom, tilt, bearing = camera
        d = self.declaration
        #: Don't update
        self._update_blocked = True
        try:
            d.camera_position = tuple(pos)
            d.camera_zoom = zoom
            d.camera_tilt = tilt
            d.camera_bearing = bearing
        finally:
            self._update_blocked = False

    # --------------------------------------------------------------------------
    # Marker API
    # --------------------------------------------------------------------------
    def on_marker_clicked(self, marker):
        mid, pos = marker
        m = self.markers.get(mid)
        if m:
            return m.on_click()
        return False

    def on_marker_drag(self, marker):
        mid, pos = marker
        m = self.markers.get(mid)
        if m:
            m.on_drag(pos)

    def on_marker_drag_start(self, marker):
        mid, pos = marker
        m = self.markers.get(mid)
        if m:
            m.on_drag_start(pos)

    def on_marker_drag_end(self, marker):
        mid, pos = marker
        m = self.markers.get(mid)
        if m:
            m.on_drag_end(pos)

    # --------------------------------------------------------------------------
    # Info window API
    # --------------------------------------------------------------------------
    def on_info_window_requested(self, marker):
        mid, pos = marker
        m = self.markers.get(mid)
        if m:
            return m.on_info_window_requested()

    def on_info_window_contents_requested(self, marker):
        mid, pos = marker
        m = self.markers.get(mid)
        if m:
            return m.on_info_window_contents_requested()

    def on_info_window_clicked(self, marker):
        mid, pos = marker
        m = self.markers.get(mid)
        if m:
            m.on_info_window_clicked('short')

    def on_info_window_long_clicked(self, marker):
        mid, pos = marker
        m = self.markers.get(mid)
        if m:
            m.on_info_window_clicked('long')

    def on_info_window_closed(self, marker):
        mid, pos = marker
        m = self.markers.get(mid)
        #: This can come later when it's removed so check the declaration
        if m and m.declaration:
            m.on_info_window_closed()

    # --------------------------------------------------------------------------
    # Polygon and PolyLine API
    # --------------------------------------------------------------------------
    def on_poly_clicked(self, poly):
        m = self.markers.get(poly)
        if m:
            m.on_click()

    # --------------------------------------------------------------------------
    # Circle API
    # --------------------------------------------------------------------------
    def on_circle_clicked(self, circle):
        m = self.markers.get(circle)
        if m:
            m.on_click()

    # --------------------------------------------------------------------------
    # ProxyMapView API
    # --------------------------------------------------------------------------
    def set_map_bounds(self, bounds):
        raise NotImplementedError

    def set_map_type(self, map_type):
        if self.map:
            self.map.setMapType(GoogleMap.MAP_TYPES[map_type])
        else:
            self.options.mapType(GoogleMap.MAP_TYPES[map_type])

    def set_show_toolbar(self, show):
        if self.map:
            pass
        else:
            self.options.mapToolbarEnabled(show)

    def set_show_compass(self, show):
        if self.map:
            pass
        else:
            self.options.compassEnabled(show)

    def set_show_zoom_controls(self, show):
        if self.map:
            pass
        else:
            self.options.zoomControlsEnabled(show)

    def set_show_location(self, show):
        if self.map:
            if show:
                def on_result(allowed):
                    if allowed:
                        self.map.setMyLocationEnabled(True)
                    else:
                        self.declaration.show_location = False
                LocationManager.check_permission().then(on_result)
            else:
                self.map.setMyLocationEnabled(False)

    def set_show_buildings(self, show):
        if self.map:
            self.map.setBuildingsEnabled(show)

    def set_show_traffic(self, show):
        if self.map:
            self.map.setTrafficEnabled(show)

    def set_show_indoors(self, show):
        if self.map:
            self.map.setBuildingsEnabled(show)

    def update_camera(self):
        if self._update_blocked:
            return
        d = self.declaration
        if self.map:
            #: Bit of a hack but it "should" work hahah
            #: The future created to handle returned values creates an id for itself.
            #: The bridge will save objects created (if they cannot be packed by a specific Packer)
            #: using that ID, hence we can reference it right away without actually waiting
            #: until we get a return value back across the bridge.
            self.map.animateCamera(CameraUpdateFactory.newCameraPosition(
                    CameraPosition(
                        LatLng(*d.camera_position),
                        d.camera_zoom,
                        d.camera_tilt,
                        d.camera_bearing
            )))
        else:
            self.options.camera(CameraPosition(
                LatLng(*d.camera_position),
                d.camera_zoom,
                d.camera_tilt,
                d.camera_bearing
            ))

    def set_camera_zoom(self, zoom):
        self.update_camera()

    def set_camera_position(self, position):
        self.update_camera()

    def set_camera_bearing(self, bearing):
        self.update_camera()

    def set_camera_tilt(self, tilt):
        self.update_camera()

    def set_ambient_mode(self, enabled):
        if self.map:
            pass
        else:
            self.options.ambientEnabled(enabled)

    def set_lite_mode(self, enabled):
        if self.map:
            pass
        else:
            self.options.liteMode(enabled)

    def set_min_zoom(self, zoom):
        if self.map:
            self.map.setMinZoomPreference(zoom)
        else:
            self.options.minZoomPreference(zoom)

    def set_max_zoom(self, zoom):
        if self.map:
            self.map.setMaxZoomPreference(zoom)
        else:
            self.options.maxZoomPreference(zoom)

    def set_rotate_gestures(self, enabled):
        if self.map:
            pass
        else:
            self.options.rotateGesturesEnabled(enabled)

    def set_scroll_gestures(self, enabled):
        if self.map:
            pass
        else:
            self.options.scrollGesturesEnabled(enabled)

    def set_tilt_gestures(self, enabled):
        if self.map:
            pass
        else:
            self.options.tiltGesturesEnabled(enabled)

    def set_zoom_gestures(self, enabled):
        if self.map:
            pass
        else:
            self.options.zoomGesturesEnabled(enabled)


class AndroidMapItemBase(AndroidToolkitObject):
    #: Options for map item constructor
    options = Instance(MapItemOptionsBase)

    #: Actual map intem created
    marker = Instance(MapItemBase)

    def init_widget(self):
        super(AndroidMapItemBase, self).init_widget()
        d = self.declaration
        if not d.visible:
            self.set_visibile(d.visible)
        if d.zindex:
            self.set_zindex(d.zindex)

    def add_to_map(self):
        """ Add this item to the map """
        raise NotImplementedError

    def destroy(self):
        """ Remove the marker if it was added to the map when destroying"""
        marker = self.marker
        parent = self.parent()
        if marker:
            if parent:
                del parent.markers[marker.__id__]
            marker.remove()
        super(AndroidMapItemBase, self).destroy()

    def set_visibile(self, visible):
        if self.marker:
            self.marker.setVisible(visible)
        else:
            self.options.visible(visible)

    def set_zindex(self, zindex):
        if self.marker:
            self.marker.setZIndex(zindex)
        else:
            self.options.zindex(zindex)


class AndroidMapMarker(AndroidMapItemBase, ProxyMapMarker):
    """ An Android implementation of an Enaml ProxyMapView.

    """

    def create_widget(self):
        """ Create the MarkerOptions for this map marker
            this later gets converted into a "Marker" instance when addMarker is called
        """
        self.options = MarkerOptions()

    def init_widget(self):
        super(AndroidMapMarker, self).init_widget()
        d = self.declaration
        if d.alpha:
            self.set_alpha(d.alpha)
        if d.anchor:
            self.set_anchor(d.anchor)
        if d.draggable:
            self.set_draggable(d.draggable)
        if not d.flat:
            self.set_flat(d.flat)
        if d.position:
            self.set_position(d.position)
        if d.rotation:
            self.set_rotation(d.rotation)
        if d.title:
            self.set_title(d.title)
        if d.snippit:
            self.set_snippit(d.snippit)

    def add_to_map(self, mapview):
        mapview.addMarker(self.options).then(self.on_marker)

    def child_added(self, child):
        """ If a child is added we have to make sure the map adapter exists """
        if child.widget:
            #: TODO: Should we keep count and remove the adapter if not all markers request it?
            self.parent().init_info_window_adapter()
        super(AndroidMapMarker, self).child_added(child)

    # --------------------------------------------------------------------------
    # Marker API
    # --------------------------------------------------------------------------
    def on_marker(self, marker):
        """ Convert our options into the actual marker object"""
        mid, pos = marker
        self.marker = Marker(__id__=mid)
        mapview = self.parent()
        #: Save ref
        mapview.markers[mid] = self

        #: Required so the packer can pass the id
        self.marker.setTag(mid)

        #: If we have a child widget we must configure the map to use the custom adapter
        for w in self.child_widgets():
            mapview.init_info_window_adapter()
            break

        d = self.declaration
        if d.show_info:
            self.set_show_info(d.show_info)

        #: Can free the options now
        del self.options

    def on_click(self):
        d = self.declaration
        result = {'handled': False}
        d.clicked(result)
        r = bool(result['handled'])
        if not r and (d.title or d.snippit):
            #: Info window is shown by default
            with self.marker.showInfoWindow.suppressed():
                d.show_info = True
        return r

    def on_drag_start(self, pos):
        d = self.declaration
        with self.marker.setPosition.suppressed():
            d.position = tuple(pos)
            d.dragging = True

    def on_drag(self, pos):
        d = self.declaration
        with self.marker.setPosition.suppressed():
            d.position = tuple(pos)

    def on_drag_end(self, pos):
        d = self.declaration
        with self.marker.setPosition.suppressed():
            d.position = tuple(pos)
            d.dragging = False

    def on_info_window_clicked(self, click):
        d = self.declaration
        d.info_clicked({'click': click})

    def on_info_window_closed(self):
        d = self.declaration
        with self.marker.hideInfoWindow.suppressed():
            d.show_info = False

    def on_info_window_requested(self):
        #: Use default window, subclasses can override if necessary
        d = self.declaration
        if d.custom_info_window_mode == 'custom':
            for w in self.child_widgets():
                return w
        return None

    def on_info_window_contents_requested(self):
        #: Return the first child widget as the view for the content
        for w in self.child_widgets():
            return w
        return None

    # --------------------------------------------------------------------------
    # ProxyMapMarker API
    # --------------------------------------------------------------------------
    def set_alpha(self, alpha):
        if self.marker:
            self.marker.setAlpha(alpha)
        else:
            self.options.alpha(alpha)

    def set_anchor(self, anchor):
        if self.marker:
            self.marker.setAnchor(*anchor)
        else:
            self.options.anchor(*anchor)

    def set_draggable(self, draggable):
        if self.marker:
            self.marker.setDraggable(draggable)
        else:
            self.options.draggable(draggable)

    def set_flat(self, flat):
        if self.marker:
            self.marker.setFlat(flat)
        else:
            self.options.flat(flat)

    def set_position(self, position):
        if self.marker:
            self.marker.setPosition(LatLng(*position))
        else:
            self.options.position(LatLng(*position))

    def set_rotation(self, rotation):
        if self.marker:
            self.marker.setRotation(rotation)
        else:
            self.options.rotation(rotation)

    def set_title(self, title):
        if self.marker:
            self.marker.setTitle(title)
        else:
            self.options.title(title)

    def set_snippit(self, snippit):
        if self.marker:
            self.marker.setSnippet(snippit)
        else:
            self.options.snippet(snippit)

    def set_show_info(self, show):
        if self.marker:
            if show:
                self.marker.showInfoWindow()
            else:
                self.marker.hideInfoWindow()

    def set_custom_info_window_mode(self, mode):
        pass


class AndroidMapCircle(AndroidMapItemBase, ProxyMapCircle):
    """ An Android implementation of an Enaml ProxyMapCircle.

    """

    def create_widget(self):
        """ Create the CircleOptions for this map item
            this later gets converted into a "Circle" instance when addCircle is called
        """
        self.options = CircleOptions()

    def add_to_map(self, mapview):
        mapview.addCircle(self.options).then(self.on_marker)

    def init_widget(self):
        super(AndroidMapCircle, self).init_widget()
        d = self.declaration
        if d.radius:
            self.set_radius(d.radius)
        #if d.clickable: doesn't work
        #    self.set_clickable(d.clickable)
        if d.position:
            self.set_position(d.position)
        if d.fill_color:
            self.set_fill_color(d.fill_color)
        if d.stroke_color:
            self.set_stroke_color(d.stroke_color)
        if d.stroke_width != 10:
            self.set_stroke_width(d.stroke_width)

    # --------------------------------------------------------------------------
    # Marker API
    # --------------------------------------------------------------------------
    def on_marker(self, mid):
        """ Convert our options into the actual circle object"""
        self.marker = Circle(__id__=mid)
        self.parent().markers[mid] = self

        #: Required so the packer can pass the id
        self.marker.setTag(mid)

        d = self.declaration
        if d.clickable:
            self.set_clickable(d.clickable)

        #: Can free the options now
        del self.options

    def on_click(self):
        d = self.declaration
        d.clicked()

    # --------------------------------------------------------------------------
    # ProxyMapCircle API
    # --------------------------------------------------------------------------
    def set_clickable(self, clickable):
        if self.marker:
            self.marker.setClickable(clickable)
        else:
            self.options.clickable(clickable)

    def set_position(self, position):
        if self.marker:
            self.marker.setCenter(LatLng(*position))
        else:
            self.options.center(LatLng(*position))

    def set_radius(self, radius):
        if self.marker:
            self.marker.setRadius(radius)
        else:
            self.options.radius(radius)

    def set_fill_color(self, color):
        if self.marker:
            self.marker.setFillColor(color)
        else:
            self.options.fillColor(color)

    def set_stroke_color(self, color):
        if self.marker:
            self.marker.setStrokeColor(color)
        else:
            self.options.strokeColor(color)

    def set_stroke_width(self, width):
        if self.marker:
            self.marker.setStrokeWidth(width)
        else:
            self.options.strokeWidth(width)


class AndroidMapPolyline(AndroidMapItemBase, ProxyMapPolyline):
    """ An Android implementation of an Enaml ProxyMapPolyline.

    """

    #: Hold the points
    points = Typed(LatLngList)

    def create_widget(self):
        """ Create the MarkerOptions for this map marker
            this later gets converted into a "Marker" instance when addMarker is called
        """
        self.options = PolylineOptions()
        #: List to hold our points
        self.points = LatLngList()

    def add_to_map(self, mapview):
        mapview.addPolyline(self.options).then(self.on_marker)

    def init_widget(self):
        super(AndroidMapPolyline, self).init_widget()
        d = self.declaration
        self.set_points(d.points)
        #if d.clickable:
        #    self.set_clickable(d.clickable)
        if d.color:
            self.set_color(d.color)
        if d.end_cap != 'butt':
            self.set_end_cap(d.end_cap)
        if d.start_cap != 'butt':
            self.set_start_cap(d.start_cap)
        if d.geodesic:
            self.set_geodesic(d.geodesic)
        if d.joint_type:
            self.set_joint_type(d.joint_type)
        if d.width != 10:
            self.set_width(d.width)

    # --------------------------------------------------------------------------
    # Polyline API
    # --------------------------------------------------------------------------
    def on_marker(self, mid):
        """ Convert our options into the actual marker object"""
        #mid, pos = marker
        self.marker = Polyline(__id__=mid)
        self.parent().markers[mid] = self
        self.marker.setTag(mid)

        d = self.declaration
        if d.clickable:
            self.set_clickable(d.clickable)

        #: Can free the options now
        del self.options

    def on_click(self):
        d = self.declaration
        d.clicked()

    # --------------------------------------------------------------------------
    # ProxyMapPolyline API
    # --------------------------------------------------------------------------
    def set_points(self, points):
        #: Have to hold on until after added to the ArrayList
        #: or the GC cleans them up and the bridge destroys them
        self.points.refresh_points(points)
        if self.marker:
            self.marker.setPoints(self.points)
        else:
            self.options.addAll(self.points)

    def update_points(self, change):
        """ Update the points in a smart way without passing them over the bridge with every
            change.
        """
        #: Delegate to the special LatLngList
        self.points.handle_change(change)
        #: Trigger update
        self.marker.setPoints(self.points)

    def set_clickable(self, clickable):
        if self.marker:
            self.marker.setClickable(clickable)
        else:
            self.options.clickable(clickable)

    def set_color(self, color):
        if self.marker:
            self.marker.setColor(color)
        else:
            self.options.color(color)

    def set_end_cap(self, cap):
        if self.marker:
            self.marker.setEndCap(Polyline.CAPS[cap]())
        else:
            self.options.endCap(Polyline.CAPS[cap]())

    def set_geodesic(self, geodesic):
        if self.marker:
            self.marker.setGeodesic(geodesic)
        else:
            self.options.geodesic(geodesic)

    def set_joint_type(self, joint_type):
        if self.marker:
            self.marker.setJointType(Polyline.JOINT_TYPES[joint_type])
        else:
            self.options.jointType(Polyline.JOINT_TYPES[joint_type])

    def set_start_cap(self, cap):
        if self.marker:
            self.marker.setStartCap(Polyline.CAPS[cap]())
        else:
            self.options.startCap(Polyline.CAPS[cap]())

    def set_width(self, width):
        if self.marker:
            self.marker.setWidth(width)
        else:
            self.options.width(width)


class AndroidMapPolygon(AndroidMapItemBase, ProxyMapPolygon):
    """ An Android implementation of an Enaml ProxyMapPolygon.

    """

    #: Hold the points
    points = Typed(LatLngList)

    #: Hold the holes
    #holes = List(ArrayList)

    def create_widget(self):
        """ Create the MarkerOptions for this map marker
            this later gets converted into a "Marker" instance when addMarker is called
        """
        self.options = PolygonOptions()
        self.points = LatLngList()

    def add_to_map(self, mapview):
        mapview.addPolygon(self.options).then(self.on_marker)

    def init_widget(self):
        super(AndroidMapPolygon, self).init_widget()
        d = self.declaration
        self.set_points(d.points)
        #if d.clickable:
        #    self.set_clickable(d.clickable)
        if d.fill_color:
            self.set_fill_color(d.fill_color)
        if d.geodesic:
            self.set_geodesic(d.geodesic)
        if d.stroke_joint_type:
            self.set_stroke_joint_type(d.joint_type)
        if d.stroke_color:
            self.set_stroke_color(d.stroke_color)
        if d.stroke_width != 10:
            self.set_stroke_width(d.stroke_width)

    # --------------------------------------------------------------------------
    # Marker API
    # --------------------------------------------------------------------------
    def on_marker(self, mid):
        """ Convert our options into the actual marker object"""
        #mid, pos = marker
        self.marker = Polygon(__id__=mid)
        self.parent().markers[mid] = self
        self.marker.setTag(mid)

        d = self.declaration
        if d.clickable:
            self.set_clickable(d.clickable)

        #: Can free the options now
        del self.options

    def on_click(self):
        d = self.declaration
        d.clicked()

    # --------------------------------------------------------------------------
    # ProxyMapMarker API
    # --------------------------------------------------------------------------
    def set_points(self, points):
        #: Have to hold on until after added to the ArrayList
        #: or the GC cleans them up and the bridge destroys them
        self.points.refresh_points(points)
        if self.marker:
            self.marker.setPoints(self.points)
        else:
            self.options.addAll(self.points)

    def update_points(self, change):
        #: Defer to points
        self.points.handle_change(change)
        #: Trigger update
        self.marker.setPoints(self.points)

    def set_clickable(self, clickable):
        if self.marker:
            self.marker.setClickable(clickable)
        else:
            self.options.clickable(clickable)

    def set_holes(self, holes):
        if self.marker:
            self.marker.setHoles([bridge.encode(LatLng(*p)) for hole in holes
                                                for p in hole])
        else:
            for hole in holes:
                self.options.addHole([bridge.encode(LatLng(*p)) for p in hole])

    def set_fill_color(self, color):
        if self.marker:
            self.marker.setFillColor(color)
        else:
            self.options.fillColor(color)

    def set_geodesic(self, geodesic):
        if self.marker:
            self.marker.setGeodesic(geodesic)
        else:
            self.options.geodesic(geodesic)

    def set_stroke_color(self, color):
        if self.marker:
            self.marker.setStrokeColor(color)
        else:
            self.options.strokeColor(color)

    def set_stroke_joint_type(self, joint_type):
        if self.marker:
            self.marker.setStrokeJointType(Polyline.JOINT_TYPES[joint_type])
        else:
            self.options.strokeJointType(Polyline.JOINT_TYPES[joint_type])

    def set_stroke_width(self, width):
        if self.marker:
            self.marker.setStrokeWidth(width)
        else:
            self.options.strokeWidth(width)
