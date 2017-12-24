"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Dec 11, 2017

@author jrm

"""
import os
import sys
import logging


def init():
    sys.modules['nativehooks'] = sys.modules['enamlnative.core.remotehooks']
    logging.basicConfig()


def log(msg):
    """ Normally the app's native hooks provides this method """
    print(msg)


def publish(data):
    from enamlnative.core.dev import DevServerSession
    DevServerSession.instance().write_message(data, True)

