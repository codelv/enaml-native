"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the MIT License.

The full license is in the file LICENSE, distributed with this software.

Created on May 15, 2018

Converts Java classes to Python classes.

 
"""
import os
from jinja2 import Template
import fnmatch
import javalang
from javalang.tree import ClassDeclaration
from os.path import exists, join
from textwrap import dedent
from atom.api import *

SDK = os.path.expanduser('~/Android/Sdk/sources/android-27/')

class RefType(Atom):
    name = Str('JavaBridgeObject')

class Import(Atom):
    name = Str()
    pkg = Str()


def convert(path, node):
    """
    
    Parameters
    ----------
    path: String
        Path of the Java source file
    node: javalang node
    
    """
    root = node.package.name.replace(".", os.path.sep)
    if not exists(root):
        os.makedirs(root)
    if not exists(join(root, '__init__.py')):
        with open(join(root, '__init__.py'), 'w') as f:
            pass
    if not node.types or not isinstance(node.types[0], ClassDeclaration):
        print("No class in {}".format(path))
        return
    # Class
    cls = node.types[0]

    with open(join(root, cls.name+'.py'), 'w') as f:
        # Format imports
        scope = set()
        for imp in node.imports:
            imp.pkg = ".".join(imp.path.split(".")[:-1])
            imp.name = "*" if imp.wildcard else imp.path.split(".")[-1]
            scope.add(imp.name)

        # Import from local package if needed
        if cls.extends and cls.extends.name not in scope:
            node.imports.append(Import(pkg='.', name=cls.extends.name))

        # Format fields
        for f in cls.fields:
            if not hasattr(f, 'name'):
                f.name = f.decorators[0].name

        if cls.documentation:
            docs = '"""{}"""'.format("\n    ".join([
                l.lstrip().lstrip("*").replace("/*", "").replace("*/", "")
                for l in cls.documentation.split("\n")
            ]))
        else:
            docs = "# No docs"

        f.write(Template(dedent("""
        from atom.api import set_default
        {% for imp in node.imports %}
        from {{ imp.pkg }} import {{ imp.name }} 
        {% endfor %}
        
        class {{cls.name}}({{base.name}}):
            {{ docs }}
            __nativeclass__ = set_default('{{node.package.name}}.{{cls.name}}')
        {% for f in cls.fields %}
            {{ f.name }} = JavaField({{f.type.name}}){% endfor %}
        {% for m in cls.methods %}{% if 'public' in m.modifiers %}
            {{ m.name }} = {% if 'static' in m.modifiers %}JavaStaticMethod{% else %}JavaMethod{% endif %}({% for p in m.parameters %}'{{p.type.name}}',{% endfor %}){% endif %}{% endfor %}
        
        """)).render(imports=node.imports,
                     node=node,
                     docs=docs,
                     cls=cls,
                     base=cls.extends or RefType()
        ))


def main():
    matches = []
    for root, dirnames, filenames in os.walk(SDK):
        rroot = os.path.relpath(root, SDK)
        if rroot.startswith('java') or rroot.startswith('android'):
            for filename in fnmatch.filter(filenames, '*.java'):
                matches.append(os.path.join(root, filename))

    for path in matches:
        print("Parsing {}".format(path))
        with open(path) as f:
            node = javalang.parse.parse(f.read())
        convert(path, node)

if __name__ == '__main__':
    main()