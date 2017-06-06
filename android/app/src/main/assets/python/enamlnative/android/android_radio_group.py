'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.radio_group import ProxyRadioGroup

from .android_linear_layout import AndroidLinearLayout

RadioGroup = jnius.autoclass('android.widget.RadioGroup')


class RadioGroupOnCheckedChangeListener(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/widget/RadioGroup$OnCheckedChangeListener']

    def __init__(self, handler):
        self.__handler__ = handler
        super(RadioGroupOnCheckedChangeListener, self).__init__()

    @jnius.java_method('(Landroid/widget/RadioGroup;I)V')
    def onCheckedChanged(self, group, checked_id):
        self.__handler__.on_checked_changed(group, checked_id)


class AndroidRadioGroup(AndroidLinearLayout, ProxyRadioGroup):
    """ An Android implementation of an Enaml ProxyLinearLayout.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(RadioGroup)

    #: Save a reference to the CheckedChangeListener
    change_listener = Typed(RadioGroupOnCheckedChangeListener)

    # --------------------------------------------------------------------------
    # Initialization API
    # --------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying Android widget.

        """
        self.widget = RadioGroup(self.get_context())

    def init_layout(self):
        """ Set the checked state after all children have
            been populated.
        """
        super(AndroidRadioGroup, self).init_layout()
        d = self.declaration
        if d.checked:
            self.set_checked(d.checked)

        self.change_listener = RadioGroupOnCheckedChangeListener(self)
        self.widget.setOnCheckedChangeListener(self.change_listener)

    def on_checked_changed(self, group, checked_id):
        """ Set the checked property based on the checked state
            of all the children
        """
        d = self.declaration
        if checked_id<0:
            d.checked = None
        else:
            for c in self.children():
                if c.widget.getId() == checked_id:
                    d.checked = c.declaration
                    break

    # --------------------------------------------------------------------------
    # ProxyRadioGroup API
    # --------------------------------------------------------------------------
    def set_checked(self, checked):
        """ Properly check the correct radio button.

        """
        if not checked:
            self.widget.clearCheck()
        else:
            #: Checked is a reference to the radio declaration
            #: so we need to get the ID of it
            rb = checked.proxy.widget
            self.widget.check(rb.getId())
