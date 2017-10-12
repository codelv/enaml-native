'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 10, 2017

@author: jrm
'''
from atom.api import (
    Atom, Typed, ForwardTyped, Unicode, Enum, Bool, Float, Tuple, Event, observe, set_default
)

from enaml.core.declarative import d_

from enaml.widgets.toolkit_object import ToolkitObject, ProxyToolkitObject
from .frame_layout import FrameLayout, ProxyFrameLayout


class LatLng(Atom):
    """ A model for the map coordinates """
    latitude = Float()
    longitude = Float()

class Camera(Atom):
    """ A model for the map camera """
    bearing = Float()
    target = Typed(LatLng)
    tilt = Float()
    zoom = Float()


class ProxyMapView(ProxyFrameLayout):
    """ The abstract definition of a proxy MapView object.

    """
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: MapView)

    def set_map_bounds(self, bounds):
        raise NotImplementedError

    def set_map_type(self, map_type):
        raise NotImplementedError

    def set_show_toolbar(self, show):
        raise NotImplementedError

    def set_show_compass(self, show):
        raise NotImplementedError

    def set_show_zoom_controls(self, show):
        raise NotImplementedError

    def set_show_location(self, show):
        raise NotImplementedError

    def set_show_buildings(self, show):
        raise NotImplementedError

    def set_show_traffic(self, show):
        raise NotImplementedError

    def set_show_indoors(self, show):
        raise NotImplementedError

    def set_camera(self, camera):
        raise NotImplementedError

    def set_ambient_mode(self, enabled):
        raise NotImplementedError

    def set_lite_mode(self, enabled):
        raise NotImplementedError

    def set_min_zoom(self, zoom):
        raise NotImplementedError

    def set_max_zoom(self, zoom):
        raise NotImplementedError

    def set_rotate_gestures(self, enabled):
        raise NotImplementedError

    def set_scroll_gestures(self, enabled):
        raise NotImplementedError

    def set_tilt_gestures(self, enabled):
        raise NotImplementedError

    def set_zoom_gestures(self, enabled):
        raise NotImplementedError
    

class ProxyMapMarker(ProxyToolkitObject):
    #: A reference to the MapMarker declaration.
    declaration = ForwardTyped(lambda: MapMarker)

    def set_alpha(self, alpha):
        raise NotImplementedError

    def set_anchor(self, anchor):
        raise NotImplementedError

    def set_draggable(self, draggable):
        raise NotImplementedError

    def set_flat(self, flat):
        raise NotImplementedError

    def set_position(self, position):
        raise NotImplementedError

    def set_rotation(self, rotation):
        raise NotImplementedError

    def set_title(self, title):
        raise NotImplementedError

    def set_snippit(self, snippit):
        raise NotImplementedError

    def set_show_info(self, show):
        raise NotImplementedError

    def set_visibile(self, visible):
        raise NotImplementedError

    def set_zindex(self, zindex):
        raise NotImplementedError


class MapView(FrameLayout):
    """ A map view using google maps.

    """
    #: Fill parent by default
    layout_height = set_default("match_parent")
    layout_width = set_default("match_parent")

    #: Specifies whether ambient-mode styling should be enabled.
    #:  The default value is false. When enabled, ambient-styled maps can be displayed
    #: when an Ambiactive device enters ambient mode.
    ambient_mode = d_(Bool())

    #: Specifies a the initial camera position for the map.
    camera = d_(Typed(Camera))

    #: Map display type
    map_type = d_(Enum('normal', 'hybrid', 'satellite', 'terrain', 'none'))

    #: Specifies a LatLngBounds to constrain the camera target,
    #: so that when users scroll and pan the map, the camera target does
    #: not move outside these bounds.
    map_bounds = d_(Tuple(LatLng))

    #: Specifies whether the compass should be enabled.
    show_compass = d_(Bool(True))

    #: Specifies whether the zoom controls should be enabled
    show_zoom_controls = d_(Bool(True))

    #: Specifies whether the mapToolbar should be enabled
    show_toolbar = d_(Bool(True))

    #: Show my location
    show_location = d_(Bool())

    #: Show traffic
    show_traffic = d_(Bool(False))

    #: Sets whether indoor maps should be enabled.
    show_indoors = d_(Bool())

    #: Turns the 3D buildings layer on or off.
    show_buildings = d_(Bool())

    #: Specifies whether the map should be created in lite mode
    lite_mode = d_(Bool(False))

    #: Specifies whether rotate gestures should be enabled.
    rotate_gestures = d_(Bool(True))

    #: Specifies whether zoom gestures should be enabled
    scroll_gestures = d_(Bool(True))

    #: Specifies whether tilt gestures should be enabled
    tilt_gestures = d_(Bool(True))

    #: Specifies whether zoom gestures should be enabled.
    zoom_gestures = d_(Bool(True))

    #: Specifies a preferred lower bound for camera zoom.
    min_zoom = d_(Float())

    #: Specifies a preferred upper bound for camera zoom.
    max_zoom = d_(Float())

    #: A reference to the ProxyMapView object.
    proxy = Typed(ProxyMapView)

    @observe('ambient_mode', 'camera', 'map_type', 'map_bounds',
             'show_compass', 'show_toolbar', 'show_zoom_controls', 'show_location',
             'show_traffic', 'show_indoors', 'show_buildings',
             'lite_mode',
             'min_zoom', 'max_zoom',
             'rotate_gestures', 'scroll_gestures','tilt_gestures', 'zoom_gestures')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(MapView, self)._update_proxy(change)


class MapMarker(ToolkitObject):
    """ A marker on the map. """

    #: Sets the alpha (opacity) of the marker.
    alpha = d_(Float(strict=False))

    #: Specifies the anchor to be at a particular point in the marker image.
    anchor = d_(Tuple(float))

    #: Sets the draggability for the marker.
    draggable = d_(Bool())

    #: Sets whether this marker should be flat against the map true or a billboard facing the camera false.
    flat = d_(Bool(True))

    #: Sets the location for the marker.
    position = d_(Tuple(float))

    #: Sets the rotation of the marker in degrees clockwise about the marker's anchor point.
    rotation = d_(Float(0, strict=False))

    #: Sets the title for the marker.
    title = d_(Unicode())

    #: Sets the snippit for the marker.
    snippit = d_(Unicode())

    #: Show info window
    show_info = d_(Bool())

    #: Sets the visibility for the marker.
    visible = d_(Bool(True))

    #: Sets the zIndex for the marker.
    zindex = d_(Float(strict=False))

    #: Marker clicked
    #: event value will have a 'result' that can be set to True
    #: to indicate the event was handled
    clicked = d_(Event(dict), writable=False)

    #: Info window clicked
    #: the event value will have an indicator of the type of click ('long', 'short')
    info_clicked = d_(Event(dict), writable=False)

    #: A reference to the ProxyMapMarker object.
    proxy = Typed(ProxyMapMarker)

    @observe('alpha', 'anchor', 'draggable', 'flat', 'position',
             'title', 'snippit', 'visible', 'zindex', 'show_info')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(MapMarker, self)._update_proxy(change)