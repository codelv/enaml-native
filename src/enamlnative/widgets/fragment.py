'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import (
    Typed, ForwardTyped, Bool, Event, observe, set_default
)

from enaml.core.declarative import d_
from enaml.core.conditional import Conditional, new_scope
from enaml.widgets.toolkit_object import ToolkitObject, ProxyToolkitObject, flag_property, ACTIVE_PROXY_FLAG
from enaml.application import Application


class ProxyFragment(ProxyToolkitObject):
    """ The abstract definition of a proxy fragment object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Fragment)
    

class Fragment(Conditional, ToolkitObject):
    """ Fragment a "sub" activity with a lifecycle,  view, and state.
        A fragment has no "widget" but it can have child
        widgets that will define it's view.  The children are rendered
        when the fragment's view is requested.
    """

    #: An event fired when an object's proxy is activated. It is
    #: triggered once during the object lifetime, at the end of the
    #: activate_proxy method.
    activated = d_(Event(), writable=False)

    #: Fragments are hidden by default and writable from the declaration
    condition = d_(Bool(False), writable=False)

    #: A property which gets and sets the active proxy flag. This should
    #: not be manipulated directly by user code. This flag will be set to
    #: True by external code after the proxy widget hierarchy is setup.
    proxy_is_active = flag_property(ACTIVE_PROXY_FLAG)

    #: A reference to the proxy object.
    proxy = Typed(ProxyFragment)

    def initialize(self):
        """ A reimplemented initializer.
        This initializer will invoke the application to create the
        proxy if one has not already been provided.
        """
        if not self.proxy:
            app = Application.instance()
            if app is None:
                msg = 'cannot create a proxy without an active Application'
                raise RuntimeError(msg)
            self.proxy = app.create_proxy(self)
        super(Fragment, self).initialize()

    def destroy(self):
        """ A reimplemented destructor.
        This destructor invokes the 'destroy' method on the proxy
        toolkit object.
        """
        super(Fragment, self).destroy()
        self.proxy_is_active = False
        if self.proxy:
            self.proxy.destroy()
            del self.proxy

    def refresh_items(self):
        """ Refresh the items of the pattern.
        This method destroys the old items and creates and initializes
        the new items.
        """
        items = []
        if self.condition:
            for nodes, key, f_locals in self.pattern_nodes:
                with new_scope(key, f_locals):
                    for node in nodes:
                        child = node(None)
                        if isinstance(child, list):
                            items.extend(child)
                        else:
                            items.append(child)

        for old in self.items:
            if not old.is_destroyed:
                old.destroy()

        #: Insert items into THIS node, NOT the PARENT
        #if len(items) > 0:
        #    self.parent.insert_children(self, items)

        self.items = items


    # #--------------------------------------------------------------------------
    # # Observers
    # #--------------------------------------------------------------------------
    # @observe(
    #     'alpha',
    #     'background_color',
    # )
    # def _update_proxy(self, change):
    #     """ An observer which sends the state change to the proxy.
    #
    #     """
    #     # The superclass implementation is sufficient.
    #     super(Fragment, self)._update_proxy(change)
