'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed, List

from enamlnative.widgets.spinner import ProxySpinner

from .android_text_view import TextView
from .android_view_group import AndroidViewGroup

String = jnius.autoclass('java.lang.String')
Gravity = jnius.autoclass('android.view.Gravity')
LayoutParams = jnius.autoclass('android.view.ViewGroup$LayoutParams')
Spinner = jnius.autoclass('android.widget.Spinner')
DataSetObservers = jnius.autoclass('android.database.DataSetObserver')

class SpinnerAdapter(jnius.PythonJavaClass):
    """ Python implementation of an Android SpinnerAdapter.
        It simply delegates all calls to a handler
        with "pythonized" versions of the methods (eg camelCase to camel_case).

    """
    __javainterfaces__ = ['android/widget/SpinnerAdapter']

    def __init__(self, handler):
        self.__handler__ = handler
        super(SpinnerAdapter, self).__init__()

    @jnius.java_method('()I')
    def getCount(self):
        return self.__handler__.get_count()

    @jnius.java_method('(I)Ljava/lang/Object;')
    def getItem(self, position):
        return self.__handler__.get_item(position)

    @jnius.java_method('(I)J')
    def getItemId(self, position):
        return self.__handler__.get_item_id(position)

    @jnius.java_method('(I)I')
    def getItemViewType(self, position):
        return self.__handler__.get_item_view_type(position)

    @jnius.java_method('()I')
    def getViewTypeCount(self):
        return self.__handler__.get_view_type_count()

    @jnius.java_method('()Z')
    def hasStableIds(self):
        return self.__handler__.has_stable_ids()

    @jnius.java_method('()Z')
    def isEmpty(self):
        return self.__handler__.is_empty()

    @jnius.java_method('(ILandroid/view/View;Landroid/view/ViewGroup;)Landroid/view/View;')
    def getView(self, position, convertView, parent):
        return self.__handler__.get_view(position, convertView, parent)

    @jnius.java_method('(ILandroid/view/View;Landroid/view/ViewGroup;)Landroid/view/View;')
    def getDropDownView(self, position, convertView, parent):
        return self.__handler__.get_drop_down_view(position, convertView, parent)

    @jnius.java_method('(Landroid/database/DataSetObserver;)V')
    def registerDataSetObserver(self, observer):
        return self.__handler__.register_data_set_observer(observer)

    @jnius.java_method('(Landroid/database/DataSetObserver;)V')
    def unregisterDataSetObserver(self, observer):
        return self.__handler__.unregister_data_set_observer(observer)


class OnItemSelectedListener(jnius.PythonJavaClass):
    """ Python implementation of an Android AdapterView.OnItemSelectedListener.
        It simply delegates all calls to a handler
        with "pythonized" versions of the methods (eg camelCase to camel_case).

    """
    __javainterfaces__ = ['android/widget/AdapterView$OnItemSelectedListener']

    def __init__(self, handler):
        self.__handler__ = handler
        super(OnItemSelectedListener, self).__init__()

    @jnius.java_method('(Landroid/widget/AdapterView;Landroid/view/View;IJ)V')
    def onItemSelected(self, parent, view, position, id):
        return self.__handler__.on_item_selected(parent, view, position, id)

    @jnius.java_method('(Landroid/widget/AdapterView;)V')
    def onNothingSelected(self, parent):
        return self.__handler__.on_nothing_selected(parent)


class AndroidSpinner(AndroidViewGroup, ProxySpinner):
    """ An Android implementation of an Enaml ProxySpinner.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(Spinner)

    #: Layout params constructor for this layout
    layout_params = LayoutParams

    #: Reference to adapter
    adapter = Typed(SpinnerAdapter)

    #: Reference to a data set observer
    observers = List(DataSetObservers)

    #: View cache
    views = List(TextView, default=[])

    #: Selection listener reference
    selection_listener = Typed(OnItemSelectedListener)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = Spinner(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidSpinner, self).init_widget()
        d = self.declaration
        self.set_prompt(d.prompt)
        if d.drop_down_width:
            self.set_drop_down_width(d.drop_down_width)
        if d.drop_down_horizontal_offset:
            self.set_drop_down_horizontal_offset(d.drop_down_horizontal_offset)
        if d.drop_down_vertical_offset:
            self.set_drop_down_vertical_offset(d.drop_down_vertical_offset)
        if d.gravity:
            self.set_gravity(d.gravity)

        #: Create the adapter
        self.adapter = SpinnerAdapter(self)
        self.set_items(d.items)
        self.widget.setAdapter(self.adapter)

        if d.selected:
            self.set_selected(d.selected)

        #: Selection listener
        self.selection_listener = OnItemSelectedListener(self)
        self.widget.setOnItemSelectedListener(self.selection_listener)

    # --------------------------------------------------------------------------
    # SpinnerAdapter API
    # --------------------------------------------------------------------------

    def get_count(self):
        d = self.declaration
        return len(d.items)

    def get_item(self, position):
        return None # Not implemented, it must be converted to an object

    def get_item_id(self, position):
        d = self.declaration
        return id(d.items[position])

    def get_item_view_type(self, position):
        return 0

    def get_view_type_count(self):
        return 1

    def has_stable_ids(self):
        return True

    def is_empty(self):
        d = self.declaration
        return len(d.items)==0

    def get_view(self, position, convert_view, parent):
        return self.views[position]

    def get_drop_down_view(self, position, convert_view, parent):
        """ Return the view

        """
        return self.get_view(position, convert_view, parent)

    def register_data_set_observer(self, observer):
        self.observers.append(observer)

    def unregister_data_set_observer(self, observer):
        try:
            self.observers.remove(observer)
        except:
            pass

    # --------------------------------------------------------------------------
    # OnSelectionListener API
    # --------------------------------------------------------------------------

    def on_item_selected(self, parent, view, position, id):
        d = self.declaration
        d.selected = position

    def on_nothing_selected(self, parent):
        pass

    # --------------------------------------------------------------------------
    # ProxySpinner API
    # --------------------------------------------------------------------------
    def set_prompt(self, prompt):
        self.widget.setPrompt(String(prompt))

    def set_selected(self, selected):
        self.widget.setSelection(selected)

    def set_items(self, items):
        """ Generate the view cache

        """
        views = []
        context = self.get_context()
        for item in items:
            tv = TextView(context)
            tv.setText(String(str(item)))
            views.append(tv)
        self.views = views

        #: Notify java observers
        for observer in self.observers:
            observer.onChanged()

    def set_gravity(self, gravity):
        g = getattr(Gravity,gravity.upper())
        self.widget.setGravity(g)

    def set_drop_down_horizontal_offset(self, offset):
        self.widget.setDropDownHorizontalOffset(offset)

    def set_drop_down_vertical_offset(self, offset):
        self.widget.setDropDownVerticalOffset(offset)

    def set_drop_down_width(self, width):
        self.widget.setDropDownWidth(width)


