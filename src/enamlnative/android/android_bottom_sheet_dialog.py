"""
Copyright (c) 2017-2022, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Jan 29, 2018
"""
from atom.api import Typed
from enamlnative.widgets.bottom_sheet_dialog import ProxyBottomSheetDialog
from .android_dialog import AndroidDialog, Dialog


class BottomSheetDialog(Dialog):
    package = "com.google.android.material.bottomsheet"

    #: Simply uses a different class
    __nativeclass__ = f"{package}.BottomSheetDialog"


class AndroidBottomSheetDialog(AndroidDialog, ProxyBottomSheetDialog):
    """An Android implementation of an Enaml ProxyBottomSheetDialog."""

    #: A reference to the widget created by the proxy.
    dialog = Typed(BottomSheetDialog)

    # -------------------------------------------------------------------------
    # Initialization API
    # -------------------------------------------------------------------------
    def create_widget(self):
        """Create the underlying widget.

        A dialog is not a subclass of view, hence we don't set name as widget
        or children will try to use it as their parent.

        """
        d = self.declaration
        self.dialog = BottomSheetDialog(self.get_context(), d.style)
