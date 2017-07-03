'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed, Instance, Subclass, Float, set_default

from enamlnative.widgets.fragment import ProxyFragment

from .android_toolkit_object import AndroidToolkitObject
from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class BridgedFragment(JavaBridgeObject):
    __javaclass__ = set_default('com.enaml.adapters.BridgedFragmentStatePagerAdapter$BridgedFragment')

    setFragmentListener = JavaMethod('com.enaml.adapters.BridgedFragmentStatePagerAdapter$FragmentListener')
    onCreateView = JavaCallback(returns='android.view.View')
    onDestroyView = JavaCallback()


class AndroidFragment(AndroidToolkitObject, ProxyFragment):
    """ An Android implementation of an Enaml ProxyFragment.

    """
    #: A reference to the fragment created by the proxy.
    fragment = Typed(BridgedFragment)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.fragment = BridgedFragment()

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidFragment, self).init_widget()
        d = self.declaration
        self.fragment.setFragmentListener(id(self.fragment))
        self.fragment.onCreateView.connect(self.on_create_view)
        self.fragment.onDestroyView.connect(self.on_destroy_view)

    def init_layout(self):
        """ Initialize the layout of the toolkit widget.

        This method is called during the bottom-up pass. This method
        should initialize the layout of the widget. The child widgets
        will be fully initialized and layed out when this is called.

        """
        parent = self.parent()
        if parent is not None:
            parent.adapter.addFragment(self.fragment)

    def destroy(self):
        """ Custom destructor """
        super(AndroidFragment, self).destroy()

        #: Destroy fragment
        if self.fragment:
            del self.fragment



    # --------------------------------------------------------------------------
    # FragmentListener API
    # --------------------------------------------------------------------------
    def on_create_view(self):
        """ Trigger the click

        """
        d = self.declaration
        d.condition = True
        return self.get_view()

    def on_destroy_view(self):
        d = self.declaration
        d.condition = False

    # --------------------------------------------------------------------------
    # ProxyFragment API
    # --------------------------------------------------------------------------
    def get_view(self):
        d = self.declaration
        for view in d.items:
            if not view.is_initialized:
                view.initialize()
            if not view.proxy_is_active:
                view.activate_proxy()
            return view.proxy.widget
