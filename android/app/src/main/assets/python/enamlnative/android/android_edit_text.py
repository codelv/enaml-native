'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.edit_text import ProxyEditText

from .android_text_view import AndroidTextView

EditText = jnius.autoclass('android.widget.EditText')

class TextWatcher(jnius.PythonJavaClass):
    __javainterfaces__ = ['android/text/TextWatcher']

    def __init__(self, handler):
        self.__handler__ = handler
        super(TextWatcher, self).__init__()

    @jnius.java_method('(Landroid/text/Editable;)V')
    def afterTextChanged(self,s):
        print "afterTextChanged called"
        pass

    @jnius.java_method('(Ljava/lang/CharSequence;III)V')
    def beforeTextChanged(self, s, start, before, count):
        print "beforeTextChanged called"

    @jnius.java_method('(Ljava/lang/CharSequence;III)V')
    def onTextChanged(self, s, start, before, count):
        print "onTextChanged called"
        self.__handler__.on_text_changed(s)


class AndroidEditText(AndroidTextView, ProxyEditText):
    """ An Android implementation of an Enaml ProxyEditText.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(EditText)

    #: A reference to the text changed listener
    watcher = Typed(TextWatcher)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = EditText(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidEditText, self).init_widget()
        d = self.declaration
        if d.selection:
            self.set_selection(d.selection)

            #: TODO: Handle onTextChanged somehow...???
        #: 1. Extend EditText in Java, override events,
        #:    and have them call python via the bridge --> Lot of work
        #: 2. Use jnius to create interface in python. Uses reflect
        #:    So I expect it to be --> Very slow!
        #: 3. What I want is to be able to extend the autoclass :)
        self.watcher = TextWatcher(self)
        self.widget.addTextChangedListener(self.watcher)
        # self.widget.onTextChanged.connect(self.on_text_changed)
        # activity.setListener()

    def on_text_changed(self, text):
        print "on_text_changed {}".format(text)
        d = self.declaration
        #d.text = text

    #--------------------------------------------------------------------------
    # ProxyEditText API
    #--------------------------------------------------------------------------
    def set_selection(self, selection):
        self.widget.setSelection(*selection)

