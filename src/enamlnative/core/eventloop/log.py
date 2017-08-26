#!/usr/bin/env python
#
# Copyright 2012 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Logging support for Tornado.

Tornado uses three logger streams:

* ``tornado.access``: Per-request logging for Tornado's HTTP servers (and
  potentially other servers in the future)
* ``tornado.application``: Logging of errors from application code (i.e.
  uncaught exceptions from callbacks)
* ``tornado.general``: General-purpose logging, including any errors
  or warnings from Tornado itself.

These streams may be configured independently using the standard library's
`logging` module.  For example, you may wish to send ``tornado.access`` logs
to a separate file for analysis.
"""
from __future__ import print_function
from atom.api import Atom, Unicode

class Logger(Atom):
    name = Unicode()

    def debug(self,*args):
        print(*args)

    def info(self, *args):
        print(*args)

    def error(self, *args, **kwargs):
        print(*args)

    def warn(self, *args):
        print(*args)

    def warning(self, *args):
        self.warn(*args)

# Logger objects for internal tornado use
access_log = Logger(name="tornado.access")  # logging.getLogger("tornado.access")
app_log = Logger(name="tornado.application")  #logging.getLogger("tornado.application")
gen_log = Logger(name="tornado.general")  #logging.getLogger("tornado.general")
