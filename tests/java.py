"""
Copyright (c) 2017-2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on Jan 18, 2018

@author
"""
import hashlib
from textwrap import dedent
from enamlnative.android.bridge import (
    JavaBridgeObject, JavaMethod, JavaStaticMethod, JavaField, JavaCallback,
    JavaProxy
)


def get_member_id(cls, m):
    """
    
    Parameters
    ----------
    cls
    m

    Returns
    -------

    """
    return hashlib.

def find_java_classes(cls):
    """ Find all java classes. Pulled from
    
    
    Parameters
    ----------
    cls: Type or Class
        Class to find

    Returns
    -------
    result: List
        All of subclasses of the given class
    
    References
    -----------
    - https://stackoverflow.com/questions/3862310/

    """
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(find_java_classes(subclass))

    return all_subclasses


def generate_source(cls):
    """ Generate java source to decode and use the object directly without 
    reflection.
    
    Parameters
    ----------
    cls: JavaBridgeObject
        Class to generate jova source for

    Returns
    -------

    """
    #: Java class name
    classname = cls.__nativeclass__.default_value_mode[-1]

    source = dedent("""
    package com.codelv.enamlnative.gen;
    
    class Bridge{classname} implements BridgeInterface {{
        
        public {classname} createObject(int constructorId, Value[] args) {{
            switch (constructorId) {{
                {constructors}
            }}
        }}
        
        public Object invokeStatic(int methodId, Value[] args) {{
            switch (methodId) {{
                {staticmethods}
            }}
        }}
        
        public Object invokeMethod(Object objRef, int methodId, Value[] args) {{
            switch (methodId) {{
                {methods}
            }}
        }}
        
        public void setField(Object objRef, int fieldId, Value[] args) {{
            {classname} obj = ({classname}) objRef;
            switch (fieldId) {{
                {fields}
            }}
        }}
    
    }}
    
    """)

    #: Find all java fields, methods, etc...
    methods = []
    fields = []
    static_methods = []
    for m in cls.members().values():
        if isinstance(m, JavaMethod):
            if m.__returns__:
                methods.append(dedent("""
                case {id}:
                    return obj.{m.name}({method_args});
                """))
            else:
                methods.append(dedent("""
                case {id}:
                    obj.{m.name}({method_args});
                    break;
                """))

        elif isinstance(m, JavaField):
            fields.append(dedent("""
                case {id}:
                    obj.{m.name} = {value};
                    break;
                """).format(m=m, id=get_member_id(cls, m)))

        elif isinstance(m, JavaStaticMethod):
            if m.__returns__:
                static_methods.append(dedent("""
                case {id}:
                    return obj.{m.name}({method_args});
                """))
        else:
            static_methods.append(dedent("""
                case {method_id}:
                    obj.{method_name}({method_args});
                    break;
                """))

    #: Return the rendered source
    return source.format(classname=classname,
                         methods="\n        ".join(methods),
                         static_methods="\n        ".join(static_methods),
                         fields="\n        ".join(fields))


def generate():
    """ Generate the Java source used to eliminate the need for using
    reflection over the bridge.
    
    """
    #: Import all the classes first
    from enamlnative.android import api
    from enamlnative.android.factories import ANDROID_FACTORIES
    for name, factory in ANDROID_FACTORIES.items():
        factory()

    #: Now gather them all
    java_classes = find_java_classes(JavaBridgeObject)

    #: Now generate it
    for cls in java_classes:
        generate_source(cls)