'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 10, 2017

@author: jrm
'''
from atom.api import Typed, Dict, set_default

from enamlnative.widgets.map_view import ProxyMapView, ProxyMapMarker
from enamlnative.core import bridge

from .android_toolkit_object import AndroidToolkitObject
from .android_frame_layout import AndroidFrameLayout, FrameLayout
from .android_fragment import FragmentTransaction, FragmentManager
from .bridge import JavaBridgeObject, JavaMethod, JavaStaticMethod, JavaCallback
from .api import LocationManager


class ConnectionResult:
    #: https://developers.google.com/android/reference/com/google/android/gms/common/ConnectionResult
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


class GoogleMap(JavaBridgeObject):
    __nativeclass__ = set_default('com.google.android.gms.maps.GoogleMap')

    addMarker = JavaMethod('com.google.android.gms.maps.model.MarkerOptions',
                           returns='com.google.android.gms.maps.model.Marker')
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

    setOnMarkerClickListener = JavaMethod('com.google.android.gms.maps.GoogleMap$OnMarkerClickListener')
    onMarkerClick = JavaCallback('com.google.android.gms.maps.model.Marker', returns='boolean')

    setOnMarkerDragListener = JavaMethod('com.google.android.gms.maps.GoogleMap$OnMarkerDragListener')
    onMarkerDrag = JavaCallback('com.google.android.gms.maps.model.Marker')
    onMarkerDragEnd = JavaCallback('com.google.android.gms.maps.model.Marker')
    onMarkerDragStart = JavaCallback('com.google.android.gms.maps.model.Marker')

    setOnInfoWindowClickListener = JavaMethod('com.google.android.gms.maps.GoogleMap$OnInfoWindowClickListener')
    onInfoWindowClick = JavaCallback('com.google.android.gms.maps.model.Marker')
    setOnInfoWindowCloseListener = JavaMethod('com.google.android.gms.maps.GoogleMap$OnInfoWindowCloseListener')
    onInfoWindowClose = JavaCallback('com.google.android.gms.maps.model.Marker')
    setOnInfoWindowLongClickListener = JavaMethod('com.google.android.gms.maps.GoogleMap$OnInfoWindowLongClickListener')
    onInfoWindowLongClick = JavaCallback('com.google.android.gms.maps.model.Marker')



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


class MarkerOptions(JavaBridgeObject):
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
    visible = JavaMethod('boolean')
    zindex = JavaMethod('float')


class Marker(JavaBridgeObject):
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
    setVisible = JavaMethod('boolean')
    setZIndex = JavaMethod('float')
    showInfoWindow = JavaMethod()
    hideInfoWindow = JavaMethod()
    setTag = JavaMethod("java.lang.Object")
    remove = JavaMethod()


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

        #: Hack because the callback creates a new object for us
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

        #: Connect signals
        self.map.onMarkerClick.connect(self.on_marker_clicked)
        self.map.setOnMarkerClickListener(self.map.getId())

        self.map.onMarkerDragStart.connect(self.on_marker_drag_start)
        self.map.onMarkerDrag.connect(self.on_marker_drag)
        self.map.onMarkerDragEnd.connect(self.on_marker_drag_end)
        self.map.setOnMarkerDragListener(self.map.getId())

        #: Info window
        self.map.onInfoWindowClick.connect(self.on_info_window_clicked)
        self.map.onInfoWindowLongClick.connect(self.on_info_window_long_clicked)
        self.map.onInfoWindowClose.connect(self.on_info_window_closed)
        self.map.setOnInfoWindowClickListener(self.map.getId())
        self.map.setOnInfoWindowCloseListener(self.map.getId())
        self.map.setOnInfoWindowLongClickListener(self.map.getId())

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
            if isinstance(child, AndroidMapMarker):
                self.map.addMarker(child.options).then(child.on_marker)
                                   
    def child_added(self, child):
        if isinstance(child, AndroidMapMarker):
            self.map.addMarker(child.options).then(child.on_marker)
        else:
            super(AndroidMapView, self).child_added(child)
    
    def child_removed(self, child):
        if isinstance(child, AndroidMapMarker):
            pass #: It removes itself
        else:
            super(AndroidMapView, self).child_removed(child)

    # --------------------------------------------------------------------------
    # Marker API
    # --------------------------------------------------------------------------
    def on_marker_clicked(self, marker):
        #: TODO: Get marker
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
        d = self.declaration
        if self.map:
            #: Bit of a hack but it "should" work hahah
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


class AndroidMapMarker(AndroidToolkitObject, ProxyMapMarker):
    """ An Android implementation of an Enaml ProxyMapView.

    """

    #: Holder for the marker
    options = Typed(MarkerOptions)

    #: Holder for the marker
    marker = Typed(Marker)

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
        if not d.visible:
            self.set_visibile(d.visible)
        if d.zindex:
            self.set_zindex(d.zindex)

    def destroy(self):
        """ Remove the marker if it was added to the map when destroying"""
        marker = self.marker
        parent = self.parent()
        if marker:
            if parent:
                del parent.markers[marker.__id__]
            marker.remove()
        super(AndroidMapMarker, self).destroy()

    # --------------------------------------------------------------------------
    # Marker API
    # --------------------------------------------------------------------------
    def on_marker(self, marker):
        """ Convert our options into the actual marker object"""
        mid, pos = marker
        self.marker = Marker(__id__=mid)
        self.parent().markers[mid] = self
        self.marker.setTag(mid)

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

    def on_drag(self, pos):
        d = self.declaration
        with self.marker.setPosition.suppressed():
            d.position = tuple(pos)

    def on_drag_end(self, pos):
        d = self.declaration
        with self.marker.setPosition.suppressed():
            d.position = tuple(pos)

    def on_info_window_clicked(self, click):
        d = self.declaration
        d.info_clicked({'click': click})

    def on_info_window_closed(self):
        d = self.declaration
        with self.marker.hideInfoWindow.suppressed():
            d.show_info = False

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
