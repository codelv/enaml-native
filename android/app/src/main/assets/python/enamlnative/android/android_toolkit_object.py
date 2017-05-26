'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
from atom.api import Typed
from enaml.widgets.toolkit_object import ProxyToolkitObject

from jnius import JavaClass, MetaJavaClass, JavaMethod, autoclass

View = autoclass('android.view.View')

# class View(JavaClass):
#     __metaclass__ = MetaJavaClass
#     __javaclass__ = 'android/view/View'
#     __javaconstructor__ = (
#         ('(Landroid/content/Context;)V',False),
#     )
#
#     setActivated = JavaMethod('(Z)V')
#     setAlpha = JavaMethod('(F)V')
#     setBackgroundColor = JavaMethod('(I)V')
#     setBottom = JavaMethod('(I)V')
#     setCameraDistance = JavaMethod('(I)V')
#     setClickable = JavaMethod('(Z)V')
#     setClipToOutline = JavaMethod('(Z)V')
#     setContentDescription = JavaMethod('(Ljava.lang.CharSequence;)V')
#     setContextClickable = JavaMethod('(Z)V')
#     setDrawingCacheBackgroundColor = JavaMethod('(I)V')
#     setDrawingCacheQuality = JavaMethod('(I)V')
#     setDuplicateParentStateEnabled = JavaMethod('(Z)V')
#     setElevation = JavaMethod('(I)V')
#     setEnabled = JavaMethod('(Z)V')
#     setFadingEdgeLength = JavaMethod('(I)V')
#     setFilterTouchesWhenObscured = JavaMethod('(Z)V')
#     setFitsSystemWindow = JavaMethod('(Z)V')
#     setFocusable = JavaMethod('(Z)V')
#     setFocusableInTouchMode = JavaMethod('(Z)V')
#     setForegroundGravity = JavaMethod('(I)V')
#     setHapticFeedbackEnabled = JavaMethod('(Z)V')
#     setHasTransientState = JavaMethod('(Z)V')
#     setHorizontalFadingEdgeEnabled = JavaMethod('(Z)V')
#     setHorizontalScrollBarEnabled = JavaMethod('(Z)V')
#     setHovered = JavaMethod('(Z)V')
#     setId = JavaMethod('(I)V')
#     setImportantForAccessibility = JavaMethod('(I)V')
#     setKeepScreenOn = JavaMethod('(Z)V')
#     setLabelFor = JavaMethod('(I)V')
#     setLayoutDirection = JavaMethod('(I)V')
#     setLayoutParams = JavaMethod('(Landroid.view.ViewGroup$LayoutParams;)V')
#     setLeft = JavaMethod('(I)V')
#     setLongClickable = JavaMethod('(Z)V')
#     setOverScrollMode = JavaMethod('(I)V')
#     setMaximumHeight = JavaMethod('(I)V')
#     setMaximumWidth = JavaMethod('(I)V')
#     setMinimumHeight = JavaMethod('(I)V')
#     setMinimumWidth = JavaMethod('(I)V')
#     #setPadding = JavaMethod('(F,F,F,F)V')
#     #setPaddingRelative = JavaMethod('(F,F,F,F)V')
#     setPivotX = JavaMethod('(F)V')
#     setPivotY = JavaMethod('(F)V')
#     setPressed = JavaMethod('(Z)V')
#     setRight = JavaMethod('(I)V')
#     setRotation = JavaMethod('(F)V')
#     setRotationX = JavaMethod('(F)V')
#     setRotationY = JavaMethod('(F)V')
#     setSaveEnabled = JavaMethod('(Z)V')
#     setSaveFromParentEnabled = JavaMethod('(Z)V')
#     setScaleX = JavaMethod('(F)V')
#     setScaleY = JavaMethod('(F)V')
#     setScrollBarDefaultDelayBeforeFade = JavaMethod('(I)V')
#     setScrollBarFadeDuration = JavaMethod('(I)V')
#     setScrollBarSize = JavaMethod('(I)V')
#     setScrollBarStyle = JavaMethod('(I)V')
#     setScrollContainer = JavaMethod('(Z)V')
#     setScrollIndicators = JavaMethod('(I)V')
#     setScrollZ = JavaMethod('(I)V')
#     setScrollX = JavaMethod('(I)V')
#     setScrollY = JavaMethod('(I)V')
#     setScrollbarFadingEnabled = JavaMethod('(Z)V')
#     setSelected = JavaMethod('(Z)V')
#     setSoundEffectsEnabled = JavaMethod('(Z)V')
#     setSystemVisibility = JavaMethod('(I)V')
#     setTextAlignment = JavaMethod('(I)V')
#     setTextDirection = JavaMethod('(I)V')
#     setTag = JavaMethod('(Ljava/lang/String;)V')
#     setTop = JavaMethod('(I)V')
#     setTransitionName = JavaMethod('(Ljava/lang/String;)V')
#     setTranslationX = JavaMethod('(F)V')
#     setTranslationY = JavaMethod('(F)V')
#     setTranslationZ = JavaMethod('(F)V')
#
#     setVerticalFadingEdgeEnabled = JavaMethod('(Z)V')
#     setVerticalScrollBarEnabled = JavaMethod('(Z)V')
#     setVerticalScrollbarPosition = JavaMethod('(I)V')
#     setVisibility = JavaMethod('(I)V')
#
#     setX = JavaMethod('(F)V')
#     setY = JavaMethod('(F)V')
#     setZ = JavaMethod('(F)V')

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
        return AndroidApplication.instance().activity

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
            widget.getParent().removeView(widget)
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
        result : QObject or None
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
        result : iterable of QObject
            The child widgets defined for this object.

        """
        for child in self.children():
            w = child.widget
            if w is not None:
                yield w
