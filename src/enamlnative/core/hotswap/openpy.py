
import os
import sys

_PYCACHE = '__pycache__'
_OPT = 'opt-'

SOURCE_SUFFIXES = ['.py']  # _setup() adds .pyw as needed.

# Code for going between .py files and cached .pyc files ----------------------
def source_from_cache(path):
    """Given the path to a .pyc. file, return the path to its .py file.
    The .pyc file does not need to exist; this simply returns the path to
    the .py file calculated to correspond to the .pyc file.  If path does
    not conform to PEP 3147/488 format, ValueError will be raised. If
    sys.implementation.cache_tag is None then NotImplementedError is raised.
    """
    #if sys.implementation.cache_tag is None:
    #    raise NotImplementedError('sys.implementation.cache_tag is None')
    #path = os.fspath(path)
    head, pycache_filename = os.path.split(path)
    head, pycache = os.path.split(head)
    if pycache != _PYCACHE:
        raise ValueError('{} not bottom-level directory in '
                         '{!r}'.format(_PYCACHE, path))
    dot_count = pycache_filename.count('.')
    if dot_count not in {2, 3}:
        raise ValueError('expected only 2 or 3 dots in '
                         '{!r}'.format(pycache_filename))
    elif dot_count == 3:
        optimization = pycache_filename.rsplit('.', 2)[-2]
        if not optimization.startswith(_OPT):
            raise ValueError("optimization portion of filename does not start "
                             "with {!r}".format(_OPT))
        opt_level = optimization[len(_OPT):]
        if not opt_level.isalnum():
            raise ValueError("optimization level {!r} is not an alphanumeric "
                             "value".format(optimization))
    base_filename = pycache_filename.partition('.')[0]
    return os.path.join(head, base_filename + SOURCE_SUFFIXES[0])