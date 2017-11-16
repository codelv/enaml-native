"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file COPYING.txt, distributed with this software.

Created on May 20, 2017

@author: jrm
"""
import sys
from contextlib import contextmanager


@contextmanager
def imports():
    """ Install the import hook to load python extensions from app's lib folder
        during the context of this block.

        This method is preferred as it's faster than using install.
    """
    from .core.import_hooks import ExtensionImporter
    importer = ExtensionImporter()
    sys.meta_path.append(importer)
    yield
    sys.meta_path.remove(importer)


def install():
    """ Install the import hook to load extensions from the app Lib folder.
        Like imports but leaves it in the meta_path, thus it is slower.
    """
    from .core.import_hooks import ExtensionImporter
    importer = ExtensionImporter()
    sys.meta_path.append(importer)