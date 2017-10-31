
from atom.api import set_default
from .bridge import JavaMethod, JavaBridgeObject

class ArrayList(JavaBridgeObject):
    __nativeclass__ = set_default('java.util.ArrayList')
    add = JavaMethod('int', 'java.lang.Object')
    addAll = JavaMethod('java.util.Collection')
    remove = JavaMethod('int')
    removeAll = JavaMethod('java.util.Collection')
    clear = JavaMethod()