'''
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
'''

#: The internal mapping of widget to proxy object.
__registry = {}


def register(widget, proxy):
    """ Register a widget and proxy object with the focus registry.

    Parameters
    ----------
    widget : QWidget
        The widget which should be mapped to the given proxy object.

    proxy : QtWidget
        The proxy object to associate with the given widget.

    """
    __registry[widget] = proxy


def unregister(widget):
    """ Unregister a widget from the focus registry.

    Parameters
    ----------
    widget : QWidget
        The widget which should be removed from the registry.

    """
    __registry.pop(widget, None)


def lookup(widget):
    """ Lookup a proxy object in the focus registry.

    Parameters
    ----------
    widget : QWidget
        The widget associated with the proxy object.

    Returns
    -------
    result : QtWidget or None
        The mapped proxy object, or None if the mapping does not exist.

    """
    return __registry.get(widget)


def focused_proxy():
    """ Get the currently focused proxy object.

    Returns
    -------
    result : QtWidget or None
        The mapped proxy object for the currently focused widget,
        or None if the focus widget does not map to a proxy.

    """
    return None # TODO: Not yet implemented
    #return lookup(QApplication.focusWidget())


def focused_declaration():
    """ Get the current focused declaration object.

    Returns
    -------
    result : Widget or None
        The declaration for the currently focused proxy, or None if
        the current focus widget does not map to a proxy.

    """
    fp = focused_proxy()
    return fp and fp.declaration