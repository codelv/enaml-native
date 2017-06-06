'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''
import jnius
from atom.api import Typed

from enamlnative.widgets.text_view import ProxyTextView

from .android_view import AndroidView

TextView = jnius.autoclass('android.widget.TextView')

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


class AndroidTextView(AndroidView, ProxyTextView):
    """ An Android implementation of an Enaml ProxyTextView.

    """
    #: A reference to the widget created by the proxy.
    widget = Typed(TextView)

    #: A reference to the text changed listener
    watcher = Typed(TextWatcher)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the underlying label widget.

        """
        self.widget = TextView(self.get_context())

    def init_widget(self):
        """ Initialize the underlying widget.

        """
        super(AndroidTextView, self).init_widget()
        d = self.declaration
        self.set_text(d.text)

    #--------------------------------------------------------------------------
    # ProxyTextView API
    #--------------------------------------------------------------------------
    def set_text(self, text):
        """ Set the text in the widget.

        """
        self.widget.setText(text, 0, len(text))


