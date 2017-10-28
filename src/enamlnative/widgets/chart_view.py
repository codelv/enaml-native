'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Oct 23, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, ContainerList, Unicode,
    Tuple, Float, Int, Bool, observe, set_default
)

from enaml.core.declarative import d_
from enaml.widgets.toolkit_object import ToolkitObject, ProxyToolkitObject

from .view_group import ViewGroup, ProxyViewGroup


class ProxyChartView(ProxyViewGroup):
    """ The abstract definition of a proxy ChartView object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: ChartView)

    def set_description(self, desc):
        raise NotImplementedError

    def set_description_color(self, color):
        raise NotImplementedError

    def set_description_position(self, pos):
        raise NotImplementedError

    def set_description_font_family(self, font):
        raise NotImplementedError

    def set_description_text_size(self, size):
        raise NotImplementedError

    def set_no_data_text(self, text):
        raise NotImplementedError

    def set_show_grid_background(self, show):
        raise NotImplementedError

    def set_grid_background_color(self, color):
        raise NotImplementedError

    def set_show_border(self, show):
        raise NotImplementedError

    def set_border_color(self, color):
        raise NotImplementedError

    def set_border_width(self, width):
        raise NotImplementedError

    def set_max_visible_vales(self, count):
        raise NotImplementedError


class ProxyLineChart(ProxyChartView):
    #: A reference to the chart declaration.
    declaration = ForwardTyped(lambda: LineChart)


class ProxyScatterChart(ProxyChartView):
    #: A reference to the chart declaration.
    declaration = ForwardTyped(lambda: ScatterChart)


class ProxyBarChart(ProxyChartView):
    #: A reference to the chart declaration.
    declaration = ForwardTyped(lambda: BarChart)


class ProxyPieChart(ProxyChartView):
    #: A reference to the chart declaration.
    declaration = ForwardTyped(lambda: PieChart)


class ProxyDataSet(ProxyToolkitObject):
    #: A reference to the data set declaration.
    declaration = ForwardTyped(lambda: DataSet)

    def set_data(self, data):
        raise NotImplementedError

    def update_data(self, change):
        raise NotImplementedError

    def set_color(self, color):
        raise NotImplementedError

    def set_text(self, text):
        raise NotImplementedError

    def set_text_color(self, color):
        raise NotImplementedError


class ChartView(ViewGroup):
    """ ChartView displays different types of charts """

    #: Expand by default
    layout_height = set_default("match_parent")
    layout_width = set_default("match_parent")

    #: Description text at the bottom right corner
    description = d_(Unicode())

    #: Color of description text at the bottom right corner
    description_color = d_(Unicode())

    #: Position of the description text
    description_position = d_(Tuple(float))

    #: Sets the size of the description text in pixels
    description_text_size = d_(Float(strict=False))

    #: Font for description
    description_font_family = d_(Unicode())

    #: ets the text that should appear if the chart is empty.
    no_data_text = d_(Unicode())

    #: If enabled, the background rectangle behind the chart drawing-area will be drawn.
    show_grid_background = d_(Bool(True))

    #: Color of the grid background
    grid_background_color = d_(Unicode())

    #: Draw lines around the chart
    show_border = d_(Bool(True))

    #: Color of border around the chart
    border_color = d_(Unicode())

    #: Border width around the chart
    border_width = d_(Float(strict=False))

    #: Sets the number of maximum visible drawn value-labels on the chart.
    max_visible_values = d_(Int())

    #: A reference to the ProxyLabel object.
    proxy = Typed(ProxyChartView)

    # --------------------------------------------------------------------------
    # Observers
    # --------------------------------------------------------------------------
    @observe('description', 'description_color', 'description_text_size', 'description_position',
             'description_font_family', 'no_data_text', 'show_grid_background',
             'grid_background_color', 'show_border',  'border_color', 'border_width',
             'max_visible_values')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        super(ChartView, self)._update_proxy(change)


class DataSet(ToolkitObject):
    #: Data this chart displays
    data = d_(ContainerList())

    #: Series color
    color = d_(Unicode())

    #: Label text
    text = d_(Unicode())

    #: Label color
    text_color = d_(Unicode())

    @observe('data')
    def _update_proxy(self, change):
        """ An observer which sends the state change to the proxy.

        """
        if change['name'] == 'data' and change['type'] == 'container':
            self.proxy.update_data(change)
        else:
            super(DataSet, self)._update_proxy(change)


class LineChart(ChartView):
    #: A reference to the proxy object.
    proxy = Typed(ProxyLineChart)


class BarChart(ChartView):
    #: A reference to the proxy object.
    proxy = Typed(ProxyBarChart)


class PieChart(ChartView):
    #: A reference to the proxy object.
    proxy = Typed(ProxyPieChart)


class ScatterChart(ChartView):
    #: A reference to the proxy object.
    proxy = Typed(ProxyScatterChart)
