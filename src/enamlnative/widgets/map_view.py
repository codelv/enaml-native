'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 10, 2017

@author: jrm
'''
from atom.api import (
    Atom, Typed, ForwardTyped, Unicode, Enum, Bool, Float, Tuple, Event,
    ContainerList, observe, set_default
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
    position = Tuple(float)
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

    def set_camera_zoom(self, zoom):
        raise NotImplementedError

    def set_camera_position(self, position):
        raise NotImplementedError

    def set_camera_bearing(self, bearing):
        raise NotImplementedError

    def set_camera_tilt(self, tilt):
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

    def set_custom_info_window_mode(self, mode):
        raise NotImplementedError


class ProxyMapCircle(ProxyToolkitObject):
    #: A reference to the MapCircle declaration.
    declaration = ForwardTyped(lambda: MapCircle)

    def set_position(self, position):
        raise NotImplementedError

    def set_radius(self, radius):
        raise NotImplementedError

    def set_clickable(self, clickable):
        raise NotImplementedError

    def set_fill_color(self, color):
        raise NotImplementedError

    def set_stroke_color(self, color):
        raise NotImplementedError

    def set_stroke_width(self, width):
        raise NotImplementedError

    def set_visible(self, visible):
        raise NotImplementedError

    def set_zindex(self, zindex):
        raise NotImplementedError


class ProxyMapPolyline(ProxyToolkitObject):
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: MapPolyline)

    def set_points(self, points):
        raise NotImplementedError

    def update_points(self, change):
        raise NotImplementedError

    def set_clickable(self, clickable):
        raise NotImplementedError

    def set_color(self, color):
        raise NotImplementedError

    def set_end_cap(self, cap):
        raise NotImplementedError

    def set_geodesic(self, geodesic):
        raise NotImplementedError

    def set_joint_type(self, joint_type):
        raise NotImplementedError

    def set_start_cap(self, cap):
        raise NotImplementedError

    def set_visible(self, visible):
        raise NotImplementedError

    def set_width(self, width):
        raise NotImplementedError

    def set_zindex(self, zindex):
        raise NotImplementedError


class ProxyMapPolygon(ProxyToolkitObject):
    #: A reference to the declaration.
    declaration = ForwardTyped(lambda: MapPolygon)

    def set_points(self, points):
        raise NotImplementedError

    def update_points(self, change):
        raise NotImplementedError

    def set_clickable(self, clickable):
        raise NotImplementedError

    def set_holes(self, holes):
        raise NotImplementedError

    def set_fill_color(self, color):
        raise NotImplementedError

    def set_geodesic(self, geodesic):
        raise NotImplementedError

    def set_stroke_color(self, color):
        raise NotImplementedError

    def set_stroke_joint_type(self, joint_type):
        raise NotImplementedError

    def set_stroke_width(self, width):
        raise NotImplementedError

    def set_visible(self, visible):
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
    camera_position = d_(Tuple(float))

    #: Map camera zoom level
    camera_zoom = d_(Float())

    #: Camera bearing
    camera_bearing = d_(Float())

    #: Camera tilt
    camera_tilt = d_(Float())

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

    #: Called when the map is clicked.
    #: the event change['value'] will have an indicator of the type of click and position
    clicked = d_(Event(dict), writable=False)

    #: Map is currently being dragged by the user
    dragging = d_(Bool(), writable=False)

    #: Map is currently being moved due to an animation
    animating = d_(Bool(), writable=False)

    #: A reference to the ProxyMapView object.
    proxy = Typed(ProxyMapView)

    @observe('ambient_mode', 'map_type', 'map_bounds',
             'show_compass', 'show_toolbar', 'show_zoom_controls', 'show_location',
             'show_traffic', 'show_indoors', 'show_buildings',
             'camera_zoom', 'camera_tilt', 'camera_position', 'camera_bearing',
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

    #: Sets whether this marker should be flat against the map true
    #: or a billboard facing the camera false.
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

    #: If marker has child widgets this will set how the contents should be rendered.
    #: if set to 'content' it uses the built-in popup window with custom content
    #: if set to 'custom' the child view is rendered as the info window itself
    custom_info_window_mode = d_(Enum('content', 'custom'))

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

    #: Marker is currently being dragged
    dragging = d_(Bool(), writable=False)

    #: A reference to the ProxyMapMarker object.
    proxy = Typed(ProxyMapMarker)

    @observe('alpha', 'anchor', 'draggable', 'flat', 'position', 'rotation',
             'title', 'snippit', 'visible', 'zindex', 'show_info', 'custom_info_window_mode')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(MapMarker, self)._update_proxy(change)


class MapCircle(ToolkitObject):
    """ A circle on the map. """

    #: Sets if it is clickable.
    clickable = d_(Bool())

    #: Circle clicked
    #: event value will have a 'result' that can be set to True
    #: to indicate the event was handled
    clicked = d_(Event(dict), writable=False)

    #: Sets the center for the circle.
    position = d_(Tuple(float))

    #: Sets the radius in meters.
    radius = d_(Float(0, strict=False))

    #: Sets the color of the polygon
    fill_color = d_(Unicode())

    #: Sets the color of the polygon
    stroke_color = d_(Unicode())

    #: Sets the width of the polyline in screen pixels.
    stroke_width = d_(Float(10, strict=False))

    #: Sets the visibility for the marker.
    visible = d_(Bool(True))

    #: Sets the zIndex for the marker.
    zindex = d_(Float(strict=False))

    #: A reference to the ProxyMapCircle object.
    proxy = Typed(ProxyMapCircle)

    @observe('clickable', 'position', 'radius', 'fill_color', 'stroke_color', 'stroke_width',
             'visible', 'zindex')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        # The superclass implementation is sufficient.
        super(MapCircle, self)._update_proxy(change)


class MapPolyline(ToolkitObject):
    """ A polyline on the map. """

    #: Sets the alpha (opacity) of the marker.
    points = d_(ContainerList(tuple))

    #: Specifies whether this polyline is clickable.
    clickable = d_(Bool())

    #: Sets the color of the polyline
    color = d_(Unicode())

    #: Sets the cap at the end vertex of the polyline
    end_cap = d_(Enum('butt', 'round', 'square'))

    #: Specifies whether to draw each segment of this polyline as a geodesic
    geodesic = d_(Bool())

    #: Sets the joint type for all vertices of the polyline except the start and end vertices.
    joint_type = d_(Enum('', 'bevel', 'round'))

    #: Sets the cap at the start vertex of the polyline
    start_cap = d_(Enum('butt', 'round', 'square'))

    #: Sets the visibility for the marker.
    visible = d_(Bool(True))

    #: Sets the width of the polyline in screen pixels.
    width = d_(Float(10, strict=False))

    #: Sets the zIndex for the marker.
    zindex = d_(Float(strict=False))

    #: Line clicked
    #: event value will have a 'result' that can be set to True
    #: to indicate the event was handled
    clicked = d_(Event(dict), writable=False)

    #: A reference to the proxy object.
    proxy = Typed(ProxyMapPolyline)

    @observe('points', 'clickable', 'color', 'end_cap', 'geodesic',
             'joint_type', 'start_cap', 'visible', 'width', 'zindex')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        if change['type'] == 'container':
            #: Only update what's needed
            self.proxy.update_points(change)
        else:
            super(MapPolyline, self)._update_proxy(change)


class MapPolygon(ToolkitObject):
    """ A polygon on the map. """

    #: Sets the alpha (opacity) of the marker.
    points = d_(ContainerList(tuple))

    #: Specifies whether this polygon is clickable.
    clickable = d_(Bool())

    #: Adds a holes to the polygon being built.
    #: May be a list of coordinates or multiple coordinate lists
    holes = d_(ContainerList(tuple))

    #: Sets the fill color of the polygon
    fill_color = d_(Unicode())

    #: Specifies whether to draw each segment of this polyline as a geodesic
    geodesic = d_(Bool())

    #: Sets the color of the polygon
    stroke_color = d_(Unicode())

    #: Sets the joint type for all vertices of the polyline except the start and end vertices.
    stroke_joint_type = d_(Enum('', 'bevel', 'round'))

    #: Sets the width of the polyline in screen pixels.
    stroke_width = d_(Float(10, strict=False))

    #: Sets the visibility for the polygon.
    visible = d_(Bool(True))

    #: Sets the zIndex for the polygon.
    zindex = d_(Float(strict=False))

    #: Line clicked
    #: event value will have a 'result' that can be set to True
    #: to indicate the event was handled
    clicked = d_(Event(dict), writable=False)

    #: A reference to the proxy object.
    proxy = Typed(ProxyMapPolygon)

    @observe('points', 'clickable', 'holes', 'fill_color', 'geodesic',
             'stroke_joint_type', 'stroke_width', 'visible', 'zindex')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        if change['type'] == 'container':
            #: Only update what's needed
            self.proxy.update_points(change)
        else:
            super(MapPolygon, self)._update_proxy(change)
