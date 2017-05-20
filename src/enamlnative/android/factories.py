'''
Created on May 20, 2017

@author: jrm
'''

def text_view_factory():
    from .android_text_view import AndroidTextView
    return AndroidTextView

def linear_layout_factory():
    from .android_linear_layout import AndroidLinearLayout
    return AndroidLinearLayout


ANDROID_FACTORIES = {
    'TextView':text_view_factory,
    'LinearLayout':linear_layout_factory,
}