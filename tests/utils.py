#------------------------------------------------------------------------------
# Copyright (c) 2017, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
import os
import sh
from contextlib import contextmanager
from enaml.core.enaml_compiler import EnamlCompiler
from enaml.core.parser import parse
from textwrap import dedent


def load(source):
    """ Load a ContentView from a source string """
    return compile_source(dedent(source), 'ContentView')


def compile_source(source, item, filename='<test>'):
    """ Compile Enaml source code and return the target item.
    Parameters
    ----------
    source : str
        The Enaml source code string to compile.
    item : str
        The name of the item in the resulting namespace to return.
    filename : str, optional
        The filename to use when compiling the code. The default
        is '<test>'.
    Returns
    -------
    result : object
        The named object from the resulting namespace.
    """
    ast = parse(source, filename)
    code = EnamlCompiler.compile(ast, filename)
    namespace = {}
    exec code in namespace
    return namespace[item]


@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    print("[DEBUG]:   -> running cd {}".format(newdir))
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        print("[DEBUG]:   -> running cd {}".format(prevdir))
        os.chdir(prevdir)


@contextmanager
def source_activated(venv, command):
    print("[DEBUG]: Activating {} for command {}".format(venv, command))

    def cmd(*args):
        #: Make a wrapper to a that runs it in the venv
        return sh.bash('-c', 'source {venv}/bin/activate && {cmd} {args}'.format(
            venv=venv, cmd=command, args=" ".join(args)
        ))

    yield cmd

    print("[DEBUG]: Deactivating {} for {}".format(venv, command))


