"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on July 10, 2017
"""
import imp
import os
import sys
from glob import glob
from typing import Optional


class ExtensionImporter:
    """Loads renamed extensions files from the app's lib folder"""

    extension_modules: dict[str, str] = {}

    def __init__(self):
        #: On iOS extensions are built as dylibs
        ext_type = "dylib" if sys.platform == "darwin" else "so"

        #: Android only copies libraries with a lib prefix
        prefix = "" if sys.platform == "darwin" else "lib."
        start = 0 if sys.platform == "darwin" else 1

        #: Find all included extension modules
        lib_dir = os.environ.get("PY_LIB_DIR", ".")
        # print("Loading {} extensions from {}".format(ext_type, lib_dir))

        for lib in glob(f"{lib_dir}/{prefix}*.{ext_type}"):
            name = lib.split("/")[-1]  # Lib filename
            mod = ".".join(name.split(".")[start:-1])  # Strip lib and so
            self.extension_modules[mod] = lib

        # print("Libraries found: {}".format(self.extension_modules))

    def load_module(self, mod: str):
        """Load the extension using the load_dynamic method."""
        try:
            return sys.modules[mod]
        except KeyError:
            pass

        lib = ExtensionImporter.extension_modules[mod]
        m = imp.load_dynamic(mod, lib)
        sys.modules[mod] = m
        return m

    def find_module(self, mod: str, path: Optional[str] = None):
        """Use this as the loader if the desired module is an extension
        within the given library folder.
        """
        if mod in self.extension_modules:
            return self
        return None
