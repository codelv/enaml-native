'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on Aug 3, 2017

@author: jrm
'''

from atom.api import Typed, set_default
from enamlnative.widgets.view import ProxyView

from .bridge import ObjcBridgeObject, ObjcMethod, ObjcProperty
from .uikit_toolkit_object import UiKitToolkitObject


class UIView(ObjcBridgeObject):
    """ From:
        https://developer.apple.com/documentation/uikit/uiview?language=objc
    """
    #__signature__ = set_default((dict(initWithFrame='CGRect'),))

    #: Properties
    backgroundColor = ObjcProperty('UIColor')
    hidden = ObjcProperty('boolean')
    alpha = ObjcProperty('float')
    opaque = ObjcProperty('boolean')
    tintColor = ObjcProperty('UIColor')
    tintAdjustmentMode = ObjcProperty('UIViewTintAdjustmentMode')
    clipsToBounds = ObjcProperty('boolean')
    clearsContextBeforeDrawing = ObjcProperty('boolean')
    maskView = ObjcProperty('UIView')
    userInteractionEnabled = ObjcProperty('boolean')
    multipleTouchEnabled = ObjcProperty('boolean')
    exclusiveTouch = ObjcProperty('boolean')

    frame = ObjcProperty('CGRect')
    bounds = ObjcProperty('CGRect')
    center = ObjcProperty('CGPoint')
    transform = ObjcProperty('CGAffineTransform')

    layoutMargins = ObjcProperty('UIEdgeInserts')
    preservesSuperviewLayoutMargins = ObjcProperty('boolean')

    #: Methods
    addSubview = ObjcMethod('UIView')
    bringSubviewToFront = ObjcMethod('UIView')
    sendSubviewToBack = ObjcMethod('UIView')
    removeFromSuperview = ObjcMethod()
    insertSubview = ObjcMethod('UIView', dict(atIndex='NSInteger',
                                              aboveSubview='UIView',
                                              belowSubview='UIView'))
    exchangeSubviewAtIndex = ObjcMethod('NSInteger', dict(withSubviewAtIndex='NSInteger'))


class UiKitView(UiKitToolkitObject, ProxyView):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UIView)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'widget' attribute.

        """
        if self.parent() is None: #: Root view?
            #: Testing...
            self.widget = UIView(__id__=-3)
        else:
            d = self.declaration
            #frame = (d.x,d.y,200, 100)
            self.widget = UIView()#initWithFrame=frame)

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        widget = self.widget

        d = self.declaration
        if d.background_color:
            self.set_background_color(d.background_color)

    def init_layout(self):
        """ Initialize the layout of the toolkit widget.

         This method is called during the bottom-up pass. This method
         should initialize the layout of the widget. The child widgets
         will be fully initialized and layed out when this is called.

         """
        widget = self.widget
        for child_widget in self.child_widgets():
            widget.addSubview(child_widget)

        d = self.declaration
        if d.x or d.y or d.width or d.height:
            self.update_frame()

    def get_app(self):
        """ Get the app of the View.

        """
        from .app import IPhoneApplication
        return IPhoneApplication.instance()

    # --------------------------------------------------------------------------
    # ProxyToolkitObject API
    # --------------------------------------------------------------------------

    def child_added(self, child):
        """ Handle the child added event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super(UiKitView, self).child_added(child)

        widget = self.widget
        #: TODO: Should index be cached?
        for i, child_widget in enumerate(self.child_widgets()):
            if child_widget == child.widget:
                widget.insertSubview(child_widget, atIndex=i)

    def child_moved(self, child):
        """ Handle the child moved event from the declaration.

        """
        super(UiKitView, self).child_moved(child)
        #: Remove and re-add in correct spot
        #: TODO: Should use exchangeSubviewAtIndex
        self.child_removed(child)
        self.child_added(child)

    def child_removed(self, child):
        """ Handle the child removed event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super(UiKitView, self).child_removed(child)
        if child.widget is not None:
            child.widget.removeFromSuperview()

    def destroy(self):
        """ A reimplemented destructor.

        This destructor will remove itself from the superview.

        """
        widget = self.widget
        if widget is not None:
            widget.removeFromSuperview()
        super(UiKitView, self).destroy()

    # --------------------------------------------------------------------------
    # ProxyView API
    # --------------------------------------------------------------------------
    def update_frame(self):
        d = self.declaration
        self.widget.frame = (d.x, d.y, d.width, d.height)

    def set_alpha(self, alpha):
        self.widget.alpha = alpha

    def set_clickable(self, clickable):
        raise NotImplementedError

    def set_background_color(self, color):
        self.widget.backgroundColor = color

    def set_layout_width(self, width):
        raise NotImplementedError

    def set_layout_height(self, height):
        raise NotImplementedError

    def set_layout_direction(self, direction):
        raise NotImplementedError

    def set_padding(self, padding):
        raise NotImplementedError

    def set_margins(self, margins):
        raise NotImplementedError

    def set_top(top):
        raise NotImplementedError

    def set_left(left):
        raise NotImplementedError

    def set_right(right):
        raise NotImplementedError

    def set_bottom(bottom):
        raise NotImplementedError

    def set_rotation(self,rotation):
        raise NotImplementedError

    def set_rotation_x(self, rotation):
        raise NotImplementedError

    def set_rotation_y(self, rotation):
        raise NotImplementedError

    def set_scale_x(self, scale):
        raise NotImplementedError

    def set_scale_y(self, scale):
        raise NotImplementedError

    def set_translation_x(self, translation):
        raise NotImplementedError

    def set_translation_y(self, translation):
        raise NotImplementedError

    def set_translation_z(self, translation):
        raise NotImplementedError

    def set_x(self, x):
        raise NotImplementedError

    def set_y(self, y):
        raise NotImplementedError

    def set_z(self, z):
        raise NotImplementedError