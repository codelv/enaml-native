'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed
from enaml.widgets.toolkit_object import ProxyToolkitObject

from .bridge import JavaBridgeObject, JavaMethod, JavaCallback


class View(JavaBridgeObject):
    __javaclass__ = 'android.view.View'

    addView = JavaMethod('android.view.View')
    onClick = JavaCallback('android.view.View')
    setOnClickListener = JavaMethod('android.view.View$OnClickListener')
    setLayoutParams = JavaMethod('android.view.ViewGroup.LayoutParams')
    setBackgroundColor = JavaMethod('android.graphics.Color')
    setClickable = JavaMethod('boolean')
    setTop = JavaMethod('int')
    setBottom = JavaMethod('int')
    setLeft = JavaMethod('int')
    setRight = JavaMethod('int')
    setLayoutDirection = JavaMethod('int')
    setPadding = JavaMethod('int','int','int','int')
    setMargins = JavaMethod('int','int','int','int')
    setX = JavaMethod('int')
    setY = JavaMethod('int')
    setZ = JavaMethod('int')
    setMaximumHeight = JavaMethod('int')
    setMaximumWidth = JavaMethod('int')
    setMinimumHeight = JavaMethod('int')
    setMinimumWidth = JavaMethod('int')
    setEnabled = JavaMethod('boolean')
    setTag = JavaMethod('java.lang.Object')
    setToolTipText = JavaMethod('java.lang.CharSequence')
    setVisibility = JavaMethod('int')
    removeView = JavaMethod('android.view.View')


class AndroidToolkitObject(ProxyToolkitObject):
    """ An Android implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(View)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'widget' attribute.

        """
        self.widget = View(self.get_context())

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        widget = self.widget
        if widget is not None:
            # Each Qt object gets a name. If one is not provided by the
            # widget author, one is generated. This is required so that
            # Qt stylesheet cascading can be prevented (Enaml's styling
            # engine applies the cascade itself). Names provided by the
            # widget author are assumed to be unique.
            d = self.declaration
            name = d.name or u'obj-%d' % id(d)
            widget.setTag(name)

    def init_layout(self):
        """ Initialize the layout of the toolkit widget.

        This method is called during the bottom-up pass. This method
        should initialize the layout of the widget. The child widgets
        will be fully initialized and layed out when this is called.

        """
        widget = self.parent_widget()
        if widget:
            widget.addView(self.widget)

    def get_context(self):
        """ Get the context of the View.

        """
        from .app import AndroidApplication
        return AndroidApplication.instance()

    #--------------------------------------------------------------------------
    # ProxyToolkitObject API
    #--------------------------------------------------------------------------
    def activate_top_down(self):
        """ Activate the proxy for the top-down pass.

        """
        self.create_widget()
        self.init_widget()

    def activate_bottom_up(self):
        """ Activate the proxy tree for the bottom-up pass.

        """
        self.init_layout()

    def destroy(self):
        """ A reimplemented destructor.

        This destructor will clear the reference to the toolkit widget
        and set its parent to None.

        """
        widget = self.widget
        if widget is not None:
            parent = self.parent_widget()
            if parent is not None:
                parent.removeView(widget)
            del self.widget
        super(AndroidToolkitObject, self).destroy()

    def child_removed(self, child):
        """ Handle the child removed event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super(AndroidToolkitObject, self).child_removed(child)
        if child.widget is not None:
            self.widget.removeView(child.widget)

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def parent_widget(self):
        """ Get the parent toolkit widget for this object.

        Returns
        -------
        result : JavaClass or None
            The toolkit widget declared on the declaration parent, or
            None if there is no such parent.

        """
        parent = self.parent()
        if parent is not None:
            return parent.widget

    def child_widgets(self):
        """ Get the child toolkit widgets for this object.

        Returns
        -------
        result : iterable of JavaClass
            The child widgets defined for this object.

        """
        for child in self.children():
            w = child.widget
            if w is not None:
                yield w
