"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
from atom.api import Typed, ForwardTyped, Bool, observe
from enaml.core.declarative import d_
from enaml.core.conditional import Conditional, new_scope
from enaml.widgets.toolkit_object import ToolkitObject, ProxyToolkitObject


class ProxyFragment(ProxyToolkitObject):
    """ The abstract definition of a proxy fragment object.

    """
    #: A reference to the Label declaration.
    declaration = ForwardTyped(lambda: Fragment)

    def set_cached(self, cached):
        raise NotImplementedError

    def set_defer_loading(self, defer):
        raise NotImplementedError


class Fragment(Conditional, ToolkitObject):
    """ Fragment a "sub" activity with a lifecycle,  view, and state.
    A fragment has no "widget" but it can have child
    widgets that will define it's view.  The children are rendered
    when the fragment's view is requested.
    
    """

    #: A reference to the proxy object.
    proxy = Typed(ProxyFragment)

    #: Don't destroy the view once loaded
    cached = d_(Bool())

    #: Defer loading of child nodes
    defer_loading = d_(Bool(True))

    def refresh_items(self):
        """ Refresh the items of the pattern.
        This method destroys the old items and creates and initializes
        the new items.

        It is overridden to NOT insert the children to the parent. The Fragment
        adapter handles this.

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

    @observe('cached', 'defer_loading')
    def _update_proxy(self, change):
        """ Update the proxy """
        super(Fragment, self)._update_proxy(change)
