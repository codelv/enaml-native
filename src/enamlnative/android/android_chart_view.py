'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed, List, Instance, Subclass, set_default

from enamlnative.widgets.chart_view import (
    ProxyChartView, ProxyLineChart, ProxyDataSet, ProxyBarChart, ProxyPieChart, ProxyScatterChart
)

from .android_toolkit_object import AndroidToolkitObject
from .android_view_group import AndroidViewGroup, ViewGroup
from .android_utils import ArrayList
from .bridge import JavaBridgeObject, JavaMethod, JavaField
from . import bridge


class ChartView(ViewGroup):
    __nativeclass__ = set_default('com.github.mikephil.charting.charts.Chart')
    setBorderColor = JavaMethod('android.graphics.Color')
    setBorderWidth = JavaMethod('float')
    setData = JavaMethod('com.github.mikephil.charting.data.ChartData')
    setNoDataText = JavaMethod('java.lang.String')
    setNoDataTextColor = JavaMethod('android.graphics.Color')
    setNoDataTextTypeface = JavaMethod('android.graphics.Typeface')
    invalidate = JavaMethod()


class Entry(JavaBridgeObject):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.Entry')
    __signature__ = set_default(('float', 'float'))


class BubbleEntry(Entry):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.BubbleEntry')
    __signature__ = set_default(('float', 'float', 'float'))


class CandleEntry(Entry):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.CandleEntry')
    __signature__ = set_default(('float', 'float', 'float', 'float', 'float'))


class RadarEntry(Entry):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.RadarEntry')
    __signature__ = set_default(('float',))


class EntryList(ArrayList):
    """ A ArrayList<Entry> that handles changes from an atom ContainerList"""

    #: Class used to create the entry instances
    entry_factory = Subclass(Entry)

    def refresh_data(self, data):
        Entry = self.entry_factory
        data = [Entry(*d) for d in data]
        self.clear()
        #: Must manually encode these the bridge currently doesnt try as it's slower
        self.addAll([bridge.encode(c) for c in data])

    def handle_change(self, change):
        """ Handle changes from atom ContainerLists """
        Entry = self.entry_factory
        op = change['operation']
        if op in 'append':
            self.add(len(change['value']), Entry(*change['item']))
        elif op == 'insert':
            self.add(change['index'], Entry(*change['item']))
        elif op == 'extend':
            points = [Entry(*p) for p in change['items']]
            self.addAll([bridge.encode(c) for c in points])
        elif op == '__setitem__':
            self.set(change['index'], Entry(*change['newitem']))
        elif op == 'pop':
            self.remove(change['index'])
        else:
            raise NotImplementedError("Unsupported change operation {}".format(op))


class ChartData(JavaBridgeObject):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.ChartData')
    clearValues = JavaMethod()
    addDataSet = JavaMethod('java.lang.Object')
    removeDataSet = JavaMethod('int')
    notifyDataChanged = JavaMethod()
    setHighlightEnabled = JavaMethod('boolean')
    setValueTextColor = JavaMethod('android.graphics.Color')
    setValueTextSize = JavaMethod('float')
    setValueTypeface = JavaMethod('android.graphics.Typeface')


class DataSet(JavaBridgeObject):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.DataSet')
    setColor = JavaMethod('android.graphics.Color')
    setValueTextColor = JavaMethod('android.graphics.Color')


#: =================================================================
#: Bar chart
#: =================================================================
class BarChart(ChartView):
    __nativeclass__ = set_default('com.github.mikephil.charting.charts.BarChart')


class BarEntry(Entry):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.BarEntry')
    __signature__ = set_default(('float', 'float'))


class BarDataSet(DataSet):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.BarDataSet')
    __signature__ = set_default(('java.util.List', 'java.lang.String'))


class BarData(ChartData):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.BarData')
    __signature__ = set_default(('java.util.List',))
    setBarWidth = JavaMethod('float')
    #: fromx, groupSpace, barSpace
    groupBars = JavaMethod('float', 'float', 'float')


#: =================================================================
#: Scatter chart
#: =================================================================
class ScatterChart(ChartView):
    __nativeclass__ = set_default('com.github.mikephil.charting.charts.ScatterChart')


class ScatterDataSet(DataSet):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.ScatterDataSet')
    __signature__ = set_default(('java.util.List', 'java.lang.String'))


class ScatterData(ChartData):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.ScatterData')
    __signature__ = set_default(('java.util.List',))


#: =================================================================
#: Pie chart
#: =================================================================
class PieChart(ChartView):
    __nativeclass__ = set_default('com.github.mikephil.charting.charts.PieChart')


class PieEntry(Entry):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.PieEntry')
    __signature__ = set_default(('float', 'java.lang.String'))


class PieDataSet(DataSet):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.PieDataSet')
    __signature__ = set_default(('java.util.List', 'java.lang.String'))


class PieData(ChartData):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.PieData')
    __signature__ = set_default(('com.github.mikephil.charting.interfaces.datasets.IPieDataSet',))


#: =================================================================
#: Line chart
#: =================================================================
class LineChart(ChartView):
    __nativeclass__ = set_default('com.github.mikephil.charting.charts.LineChart')


class LineDataSet(DataSet):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.LineDataSet')
    __signature__ = set_default(('java.util.List', 'java.lang.String'))


class LineData(ChartData):
    __nativeclass__ = set_default('com.github.mikephil.charting.data.LineData')
    __signature__ = set_default(('java.util.List',))


class AndroidChartView(AndroidViewGroup, ProxyChartView):
    """ An Android implementation of an Enaml ProxyChartView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ChartView)

    #: Holder for the array list
    entry_factory = Subclass(Entry)

    #: Holder for data sets
    data_sets = List(DataSet)

    #: Holder for chart data container
    chart_data = Instance(ChartData)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ChartView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidChartView, self).init_widget()
        d = self.declaration
        if d.no_data_text:
            self.set_no_data_text(d.no_data_text)
        #: TODO:... all the others

    def init_layout(self):
        super(AndroidChartView, self).init_layout()
        d = self.declaration
        self.refresh_data_set()

    def child_added(self, child):
        if isinstance(child, AndroidDataSet):
            self.add_data_set(child)
        else:
            super(AndroidChartView, self).child_added(child)

    def child_removed(self, child):
        if isinstance(child, AndroidDataSet):
            self.remove_data_set(child)
        else:
            super(AndroidChartView, self).child_removed(child)

    # --------------------------------------------------------------------------
    # DataSet API
    # --------------------------------------------------------------------------
    def data_sets(self):
        for c in self.children():
            if isinstance(c, AndroidDataSet):
                yield c

    def make_data_set(self, data_set):
        raise NotImplementedError

    def handle_data_set_change(self, change):
        """ Tell chart data to update.

        """
        self.chart_data.notifyDataSetChanged()

    def refresh_data_set(self):
        """ Do a full refresh of the data.
            Note: Chart data must already be set by subclasses!
        """
        self.widget.setData(self.chart_data)
        self.widget.invalidate()

    def add_data_set(self, data_set):
        """ Add a new data set """
        self.chart_data.addDataSet(data_set.data_set)
        self.widget.invalidate()

    def remove_data_set(self, data_set):
        """ Remove a new data set """
        self.line_data.removeDataSet(data_set.data_set)
        self.widget.invalidate()

    # --------------------------------------------------------------------------
    # ProxyChartView API
    # --------------------------------------------------------------------------
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
        self.widget.setNoDataText(text)

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


class AndroidLineChart(AndroidChartView, ProxyLineChart):
    """ An Android implementation of an Enaml ProxyLineChart.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(LineChart)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = LineChart(self.get_context())

    # --------------------------------------------------------------------------
    # DataSet API
    # --------------------------------------------------------------------------
    def make_data_set(self, data_set):
        """ Configure the data set for this child"""
        d = data_set.declaration
        data_set.data_set = LineDataSet(data_set.data, d.text)

    def refresh_data_set(self):
        self.chart_data = LineData([bridge.encode(c.data_set) for c in self.data_sets()])
        super(AndroidLineChart, self).refresh_data_set()


class AndroidScatterChart(AndroidChartView, ProxyScatterChart):
    """ An Android implementation of an Enaml ProxyLineChart.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(ScatterChart)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = ScatterChart(self.get_context())

    # --------------------------------------------------------------------------
    # DataSet API
    # --------------------------------------------------------------------------
    def make_data_set(self, data_set):
        """ Configure the data set for this child"""
        d = data_set.declaration
        data_set.data_set = ScatterDataSet(data_set.data, d.text)

    def refresh_data_set(self):
        self.chart_data = ScatterData([bridge.encode(c.data_set) for c in self.data_sets()])
        super(AndroidScatterChart, self).refresh_data_set()


class AndroidBarChart(AndroidChartView, ProxyBarChart):
    """ An Android implementation of an Enaml ProxyLineChart.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(BarChart)

    #: Use pie chart specific entry
    entry_factory = set_default(BarEntry)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = BarChart(self.get_context())

    # --------------------------------------------------------------------------
    # DataSet API
    # --------------------------------------------------------------------------
    def make_data_set(self, data_set):
        """ Configure the data set for this child"""
        d = data_set.declaration
        data_set.data_set = BarDataSet(data_set.data, d.text)

    def refresh_data_set(self):
        self.chart_data = BarData([bridge.encode(c.data_set) for c in self.data_sets()])
        super(AndroidBarChart, self).refresh_data_set()


class AndroidPieChart(AndroidChartView, ProxyPieChart):
    """ An Android implementation of an Enaml ProxyLineChart.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(PieChart)

    #: Use pie chart specific entry
    entry_factory = set_default(PieEntry)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.widget = PieChart(self.get_context())

    # --------------------------------------------------------------------------
    # DataSet API
    # --------------------------------------------------------------------------
    def make_data_set(self, data_set):
        """ Configure the data set for this child"""
        d = data_set.declaration
        data_set.data_set = PieDataSet(data_set.data, d.text)

    def refresh_data_set(self):
        for c in self.data_sets():
            self.chart_data = PieData(c.data_set)
            break
        super(AndroidPieChart, self).refresh_data_set()


class AndroidDataSet(AndroidToolkitObject, ProxyDataSet):

    #: Holds the data
    data = Instance(EntryList)

    #: Holds settings and such for the data
    data_set = Instance(DataSet)

    def create_widget(self):
        self.data = EntryList()
        self.data.entry_factory = self.parent().entry_factory

    def init_widget(self):
        super(AndroidDataSet, self).init_widget()
        d = self.declaration
        if d.data:
            self.set_data(d.data)

        #: Let the parent choose the type
        self.parent().make_data_set(self)

        #: Now update the data set
        if d.color:
            self.set_color(d.color)
        if d.text_color:
            self.set_text_color(d.text_color)

    # --------------------------------------------------------------------------
    # DataSet API
    # --------------------------------------------------------------------------
    def set_data(self, data):
        self.data.refresh_data(data)

    def update_data(self, change):
        self.data.handle_change(change)
        self.parent().handle_data_set_change(change)

    def set_color(self, color):
        self.data_set.setColor(color)

    def set_text(self, text):
        self.data_set.setLabel(text)

    def set_text_color(self, color):
        self.data_set.setValueTextColor(color)
