"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Aug 3, 2017

@author: jrm
"""

from atom.api import Typed, Tuple, observe
from enamlnative.widgets.view import ProxyView

from .bridge import ObjcBridgeObject, ObjcMethod, ObjcProperty, ObjcCallback
from .uikit_toolkit_object import UiKitToolkitObject
from .yoga import Yoga


class NSObject(ObjcBridgeObject):

    addObserver = ObjcMethod('NSObject',
                             dict(forKeyPath="NSString"),
                             dict(options="NSKeyValueObservingOptions"),
                             dict(context="void*"))
    removeObserver = ObjcMethod('NSObject', dict(forKeyPath="NSString"))

    observeValueForKeyPath = ObjcCallback('NSString',
                                          dict(ofObject="id"),
                                          dict(change="NSDictionary"),
                                          dict(context="void*"))

    NSKeyValueObservingOptionNew = 0x01
    NSKeyValueObservingOptionOld = 0x02
    NSKeyValueObservingOptionInitial = 0x04
    NSKeyValueObservingOptionPrior = 0x08


class UIResponder(NSObject):
    pass


class UIView(UIResponder):
    """ From:
        https://developer.apple.com/documentation/uikit/uiview?language=objc
    """
    yoga = Typed(Yoga)

    def _default_yoga(self):
        return Yoga(self, 'yoga')

    #: Properties
    backgroundColor = ObjcProperty('UIColor')
    hidden = ObjcProperty('bool')
    alpha = ObjcProperty('float')
    opaque = ObjcProperty('bool')
    tintColor = ObjcProperty('UIColor')
    tintAdjustmentMode = ObjcProperty('UIViewTintAdjustmentMode')
    clipsToBounds = ObjcProperty('bool')
    clearsContextBeforeDrawing = ObjcProperty('bool')
    maskView = ObjcProperty('UIView')
    userInteractionEnabled = ObjcProperty('bool')
    multipleTouchEnabled = ObjcProperty('bool')
    exclusiveTouch = ObjcProperty('bool')

    frame = ObjcProperty('CGRect')
    bounds = ObjcProperty('CGRect')
    center = ObjcProperty('CGPoint')
    transform = ObjcProperty('CGAffineTransform')

    layoutMargins = ObjcProperty('UIEdgeInserts')
    preservesSuperviewLayoutMargins = ObjcProperty('bool')

    #: Methods
    addSubview = ObjcMethod('UIView')
    bringSubviewToFront = ObjcMethod('UIView')
    sendSubviewToBack = ObjcMethod('UIView')
    removeFromSuperview = ObjcMethod()
    insertSubview = ObjcMethod('UIView', dict(atIndex='NSInteger',
                                              aboveSubview='UIView',
                                              belowSubview='UIView'))
    exchangeSubviewAtIndex = ObjcMethod('NSInteger',
                                        dict(withSubviewAtIndex='NSInteger'))

    #:


class UiKitView(UiKitToolkitObject, ProxyView):
    """ An UiKit implementation of an Enaml ProxyToolkitObject.

    """

    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(UIView)

    #: Frame in (x,y,width,height)
    frame = Tuple()

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'widget' attribute.

        """
        self.widget = UIView()#initWithFrame=frame)

    def init_widget(self):
        """ Initialize the underlying widget.

        This reads all items declared in the enamldef block for this node
        and sets only the values that have been specified. All other values
        will be left as default. Doing it this way makes atom to only create
        the properties that need to be overridden from defaults thus greatly
        reducing the number of initialization checks, saving time and memory.

        If you don't want this to happen override `get_declared_keys`
        to return an empty list.

        """
        super(UiKitView, self).init_widget()

        self.widget.yoga.isEnabled = True

        # Initialize the widget by updating only the members that
        # have read expressions declared. This saves a lot of time and
        # simplifies widget initialization code
        for k, v in self.get_declared_items():
            handler = getattr(self, 'set_'+k, None)
            if handler:
                handler(v)

    def get_declared_items(self):
        """ Get the members that were set in the enamldef block for this
        Declaration. Layout keys are grouped together until the end so as
        to avoid triggering multiple updates.

        Returns
        -------
        result: List of (k,v) pairs that were defined for this widget in enaml
            List of keys and values

        """
        d = self.declaration
        engine = d._d_engine
        if engine:
            for k, h in engine._handlers.items():
                # Handlers with read operations
                if not h.read_pair:
                    continue
                v = getattr(d, k)
                yield (k, v)

    def init_layout(self):
        """ Initialize the layout of the toolkit widget.

         This method is called during the bottom-up pass. This method
         should initialize the layout of the widget. The child widgets
         will be fully initialized and layed out when this is called.

         """
        widget = self.widget
        for child_widget in self.child_widgets():
            widget.addSubview(child_widget)

    def update_frame(self):
        """ Define the view frame for this widgets"""
        d = self.declaration
        if d.x or d.y or d.width or d.height:
            self.frame = (d.x, d.y, d.width, d.height)

    def get_app(self):
        """ Get the app of the View.

        """
        from .app import IPhoneApplication
        return IPhoneApplication.instance()

    # -------------------------------------------------------------------------
    # ProxyToolkitObject API
    # -------------------------------------------------------------------------

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

    # -------------------------------------------------------------------------
    # ProxyView API
    # -------------------------------------------------------------------------
    @observe('frame')
    def set_frame(self, change):
        if self.frame:
            self.widget.frame = self.frame

    def set_alpha(self, alpha):
        self.widget.alpha = alpha

    def set_clickable(self, clickable):
        raise NotImplementedError

    def set_background_color(self, color):
        self.widget.backgroundColor = color

    def set_width(self, width):
        self.yoga.width = width

    def set_height(self, height):
        self.yoga.height = height

    def set_padding(self, padding):
        yoga = self.widget.yoga
        yoga.paddingTop = padding[0]
        yoga.paddingRight = padding[1]
        yoga.paddingBottom = padding[2]
        yoga.paddingLeft = padding[3]

    def set_margins(self, margins):
        yoga = self.widget.yoga
        yoga.marginTop = margins[0]
        yoga.marginRight = margins[1]
        yoga.marginBottom = margins[2]
        yoga.marginLeft = margins[3]

    def set_top(self, top):
        self.widget.yoga.top = top

    def set_left(self, left):
        self.widget.yoga.left = left

    def set_right(self, right):
        self.widget.yoga.right = right

    def set_bottom(self, bottom):
        self.widget.yoga.bottom = bottom

    def set_x(self, x):
        self.widget.yoga.left = x

    def set_y(self, y):
        self.widget.yoga.top = y

    def set_z(self, z):
        raise NotImplementedError

    def set_max_height(self, max_height):
        self.widget.yoga.maxHeight = max_height

    def set_min_width(self, min_width):
        self.widget.yoga.minWidth = min_width

    def set_max_width(self, max_width):
        self.widget.yoga.maxWidth = max_width

    def set_flex_grow(self, flex_grow):
        self.widget.yoga.flexGrow = flex_grow

    def set_flex_basis(self, basis):
        self.widget.yoga.flexBasis = int(basis*100)

    def set_flex_shrink(self, flex_shrink):
        self.widget.yoga.flexShrink = flex_shrink

    def set_align_self(self, align_self):
        self.widget.yoga.alignSelf = Yoga.ALIGN_SELF[align_self]

