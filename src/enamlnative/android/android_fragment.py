"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, Value, set_default

from enamlnative.widgets.fragment import ProxyFragment
from enamlnative.widgets.view_pager import ProxyPagerFragment

from .android_toolkit_object import AndroidToolkitObject
from .android_frame_layout import FrameLayout
from .android_view_pager import BridgedFragmentStatePagerAdapter
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class FragmentManager(JavaBridgeObject):
    __nativeclass__ = set_default('android.support.v4.app.FragmentManager')
    beginTransaction = JavaMethod(
        returns='android.support.v4.app.FragmentTransaction')


class FragmentTransaction(JavaBridgeObject):
    __nativeclass__ = set_default('android.support.v4.app.FragmentTransaction')
    commit = JavaMethod(returns='int')
    add = JavaMethod('int', 'android.support.v4.app.Fragment')
    replace = JavaMethod('int', 'android.support.v4.app.Fragment')


class BridgedFragment(JavaBridgeObject):
    __nativeclass__ = set_default(
        'com.codelv.enamlnative.adapters.BridgedFragmentStatePagerAdapter'
        '$BridgedFragment')
    setTitle = JavaMethod('java.lang.String')
    setFragmentListener = JavaMethod(
        'com.codelv.enamlnative.adapters.BridgedFragmentStatePagerAdapter'
        '$FragmentListener')
    onCreateView = JavaCallback(returns='android.view.View')
    onDestroyView = JavaCallback()


class AndroidFragment(AndroidToolkitObject, ProxyFragment):
    """ An Android implementation of an Enaml ProxyFragment.

    """
    #: A reference to the fragment created by the proxy.
    fragment = Typed(BridgedFragment)

    #: Reference to the adapter
    adapter = Typed(BridgedFragmentStatePagerAdapter)

    #: Future set when ready
    ready = Value()

    def _default_ready(self):
        return self.get_context().create_future()

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying widget.

        """
        self.fragment = BridgedFragment()

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidFragment, self).init_widget()
        f = self.fragment
        f.setFragmentListener(f.getId())
        f.onCreateView.connect(self.on_create_view)
        f.onDestroyView.connect(self.on_destroy_view)

    def init_layout(self):
        """ Initialize the layout of the toolkit widget.

        This method is called during the bottom-up pass. This method
        should initialize the layout of the widget. The child widgets
        will be fully initialized and layed out when this is called.

        """
        parent = self.parent()
        if parent is not None:
            self.adapter = parent.adapter
            self.adapter.addFragment(self.fragment)

    def destroy(self):
        """ Custom destructor that deletes the fragment and removes
        itself from the adapter it was added to.
        
        """
        #: Destroy fragment
        fragment = self.fragment
        if fragment:
            #: Stop listening
            fragment.setFragmentListener(None)

            #: Cleanup from fragment
            if self.adapter is not None:
                self.adapter.removeFragment(self.fragment)

            del self.fragment
        super(AndroidFragment, self).destroy()

    # -------------------------------------------------------------------------
    # FragmentListener API
    # -------------------------------------------------------------------------
    def on_create_view(self):
        """ Trigger the click

        """
        d = self.declaration
        changed = not d.condition
        if changed:
            d.condition = True

        view = self.get_view()

        if changed:
            self.ready.set_result(True)

        return view

    def on_destroy_view(self):
        d = self.declaration

        #: Destroy if we don't want to cache it
        if not d.cached:
            d.condition = False

            #: Delete the reference
            if self.widget:
                del self.widget

            #: Clear the ready state again!
            self.ready = self._default_ready()

    # -------------------------------------------------------------------------
    # ProxyFragment API
    # -------------------------------------------------------------------------
    def get_view(self):
        """ Get the page to display. If a view has already been created and
        is cached, use that otherwise initialize the view and proxy. If defer
        loading is used, wrap the view in a FrameLayout and defer add view 
        until later. 
        
        """
        d = self.declaration
        if d.cached and self.widget:
            return self.widget
        if d.defer_loading:
             self.widget = FrameLayout(self.get_context())
             app = self.get_context()
             app.deferred_call(
                 lambda: self.widget.addView(self.load_view(), 0))
        else:
            self.widget = self.load_view()
        return self.widget

    def load_view(self):
        d = self.declaration
        for view in d.items:
            if not view.is_initialized:
                view.initialize()
            if not view.proxy_is_active:
                view.activate_proxy()
            return view.proxy.widget

    def set_cached(self, cached):
        pass

    def set_defer_loading(self, defer):
        pass


class AndroidPagerFragment(AndroidFragment, ProxyPagerFragment):
    """ An Android implementation of an Enaml ProxyPagerFragment.

    """
    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidPagerFragment, self).init_widget()
        d = self.declaration
        if d.title:
            self.set_title(d.title)
        if d.icon:
            self.set_icon(d.icon)

    # -------------------------------------------------------------------------
    # ProxyPagerTabStrip API
    # -------------------------------------------------------------------------
    def set_title(self, title):
        self.fragment.setTitle(title)

    def set_icon(self, icon):
        pass
        #self.adapter.setPageIcon(self.widget, icon)
