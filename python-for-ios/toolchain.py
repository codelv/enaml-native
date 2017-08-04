#!/usr/bin/env python2
"""
Tool for compiling iOS toolchain
================================

This tool intend to replace all the previous tools/ in shell script.
"""

import sys
from sys import stdout
import os
from os.path import join, dirname, realpath, exists, isdir, basename
from os import listdir, unlink, makedirs, environ, chdir, getcwd, walk, remove
import zipfile
import tarfile
import importlib
import io
import json
import shutil
import fnmatch
import glob
import virtualenv
import plistlib
from contextlib import contextmanager
from datetime import datetime
from logger import setup_color, info, info_main, info_notify, shprint
try:
    from urllib.request import FancyURLopener, urlcleanup
except ImportError:
    from urllib import FancyURLopener, urlcleanup

curdir = dirname(__file__)
sys.path.insert(0, join(curdir, "tools", "external"))

import sh


IS_PY3 = sys.version_info[0] >= 3


@contextmanager
def current_directory(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        print("Entering into {}".format(newdir))
        yield
        print("Returning to {}".format(prevdir))
    finally:
        os.chdir(prevdir)

# @contextmanager
# def venv_active(venv):
#     print("Activating virtualenv {}".format(venv))
#     with current_directory(join(venv,'bin')):
#         yield
#     print("Deactivating virtualenv {}".format(venv))


# def shprint(command, *args, **kwargs):
#     kwargs["_iter"] = True
#     kwargs["_out_bufsize"] = 1
#     kwargs["_err_to_out"] = True
#     for line in command(*args, **kwargs):
#         stdout.write(line)


def cache_execution(f):
    def _cache_execution(self, *args, **kwargs):
        state = self.ctx.state
        key = "{}.{}".format(self.name, f.__name__)
        force = kwargs.pop("force", False)
        if args:
            for arg in args:
                key += ".{}".format(arg)
        key_time = "{}.at".format(key)
        if key in state and not force:
            info("# (ignored) {} {}".format(f.__name__.capitalize(), self.name))
            return
        info("{} {}".format(f.__name__.capitalize(), self.name))
        f(self, *args, **kwargs)
        state[key] = True
        state[key_time] = str(datetime.utcnow())
    return _cache_execution


class ChromeDownloader(FancyURLopener):
    version = (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36')

urlretrieve = ChromeDownloader().retrieve


class JsonStore(object):
    """Replacement of shelve using json, needed for support python 2 and 3.
    """

    def __init__(self, filename):
        super(JsonStore, self).__init__()
        self.filename = filename
        self.data = {}
        if exists(filename):
            try:
                with io.open(filename, encoding='utf-8') as fd:
                    self.data = json.load(fd)
            except ValueError:
                info("Unable to read the state.db, content will be replaced.")

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        self.sync()

    def __delitem__(self, key):
        del self.data[key]
        self.sync()

    def __contains__(self, item):
        return item in self.data

    def get(self, item, default=None):
        return self.data.get(item, default)

    def keys(self):
        return self.data.keys()

    def remove_all(self, prefix):
        for key in self.data.keys()[:]:
            if not key.startswith(prefix):
                continue
            del self.data[key]
        self.sync()

    def sync(self):
        # http://stackoverflow.com/questions/12309269/write-json-data-to-file-in-python/14870531#14870531
        if IS_PY3:
            with open(self.filename, 'w') as fd:
                json.dump(self.data, fd, ensure_ascii=False, indent=2)
        else:
            with io.open(self.filename, 'w', encoding='utf-8') as fd:
                fd.write(unicode(json.dumps(self.data, ensure_ascii=False, indent=2)))

class Arch(object):
    def __init__(self, ctx):
        super(Arch, self).__init__()
        self.ctx = ctx
        self._ccsh = None

    def __str__(self):
        return self.arch

    @property
    def include_dirs(self):
        return [
            "{}/{}".format(
                self.ctx.include_dir,
                d.format(arch=self))
            for d in self.ctx.include_dirs]


    def get_env(self):
        include_dirs = [
            "-I{}/{}".format(
                self.ctx.include_dir,
                d.format(arch=self))
            for d in self.ctx.include_dirs]

        env = {}
        ccache = sh.which('ccache')
        cc = sh.xcrun("-find", "-sdk", self.sdk, "clang").strip()
        if ccache:
            ccache = ccache.strip()
            use_ccache = environ.get("USE_CCACHE", "1")
            if use_ccache != '1':
                env["CC"] = cc
            else:
                if not self._ccsh:
                    self._ccsh = ccsh = sh.mktemp().strip()
                    with open(ccsh, 'w') as f:
                        f.write('#!/bin/sh\n')
                        f.write(ccache + ' ' + cc + ' "$@"\n')
                    sh.chmod('+x', ccsh)
                else:
                    ccsh = self._ccsh
                env["USE_CCACHE"] = '1'
                env["CCACHE"] = ccache
                env["CC"] = ccsh

                env.update({k: v for k, v in environ.items() if k.startswith('CCACHE_')})
                env.setdefault('CCACHE_MAXSIZE', '10G')
                env.setdefault('CCACHE_HARDLINK', 'true')
                env.setdefault('CCACHE_SLOPPINESS', ('file_macro,time_macros,'
                    'include_file_mtime,include_file_ctime,file_stat_matches'))
        else:
            env["CC"] = cc
        env["AR"] = sh.xcrun("-find", "-sdk", self.sdk, "ar").strip()
        env["CXX"] = sh.xcrun("-find", "-sdk", self.sdk, "g++").strip()

        env["LD"] = sh.xcrun("-find", "-sdk", self.sdk, "ld").strip()
        env["OTHER_CFLAGS"] = " ".join(include_dirs)
        env["OTHER_LDFLAGS"] = " ".join([
            "-L{}/{}".format(self.ctx.dist_dir, "lib"),
        ])
        env["CFLAGS"] = " ".join([
            "-arch", self.arch,
            "-pipe", "-no-cpp-precomp",
            "--sysroot", self.sysroot,
            #"-I{}/common".format(self.ctx.include_dir),
            #"-I{}/{}".format(self.ctx.include_dir, self.arch),
            "-O3",
            self.version_min
        ] + include_dirs)
        env["LDFLAGS"] = " ".join([
            "-arch", self.arch,
            "--sysroot", self.sysroot,
            "-L{}/{}".format(self.ctx.dist_dir, "lib"),
            "-lsqlite3",
            self.version_min
        ])
        return env



class ArchSimulator(Arch):
    sdk = "iphonesimulator"
    arch = "i386"
    triple = "i386-apple-darwin11"
    version_min = "-miphoneos-version-min=8.0"
    sysroot = sh.xcrun("--sdk", "iphonesimulator", "--show-sdk-path").strip()


class Arch64Simulator(Arch):
    sdk = "iphonesimulator"
    arch = "x86_64"
    triple = "x86_64-apple-darwin13"
    version_min = "-miphoneos-version-min=8.0"
    sysroot = sh.xcrun("--sdk", "iphonesimulator", "--show-sdk-path").strip()


class ArchIOS(Arch):
    sdk = "iphoneos"
    arch = "armv7"
    triple = "arm-apple-darwin11"
    version_min = "-miphoneos-version-min=8.0.0"
    sysroot = sh.xcrun("--sdk", "iphoneos", "--show-sdk-path").strip()


class Arch64IOS(Arch):
    sdk = "iphoneos"
    arch = "arm64"
    triple = "aarch64-apple-darwin13"
    version_min = "-miphoneos-version-min=8.0"
    sysroot = sh.xcrun("--sdk", "iphoneos", "--show-sdk-path").strip()


class Graph(object):
    # Taken from python-for-android/depsort
    def __init__(self):
        # `graph`: dict that maps each package to a set of its dependencies.
        self.graph = {}

    def add(self, dependent, dependency):
        """Add a dependency relationship to the graph"""
        self.graph.setdefault(dependent, set())
        self.graph.setdefault(dependency, set())
        if dependent != dependency:
            self.graph[dependent].add(dependency)

    def add_optional(self, dependent, dependency):
        """Add an optional (ordering only) dependency relationship to the graph

        Only call this after all mandatory requirements are added
        """
        if dependent in self.graph and dependency in self.graph:
            self.add(dependent, dependency)

    def find_order(self):
        """Do a topological sort on a dependency graph

        :Parameters:
            :Returns:
                iterator, sorted items form first to last
        """
        graph = dict((k, set(v)) for k, v in self.graph.items())
        while graph:
            # Find all items without a parent
            leftmost = [l for l, s in graph.items() if not s]
            if not leftmost:
                raise ValueError('Dependency cycle detected! %s' % graph)
            # If there is more than one, sort them for predictable order
            leftmost.sort()
            for result in leftmost:
                # Yield and remove them from the graph
                yield result
                graph.pop(result)
                for bset in graph.values():
                    bset.discard(result)


class Context(object):
    env = environ.copy()
    root_dir = None
    cache_dir = None
    build_dir = None
    dist_dir = None
    install_dir = None
    ccache = None
    cython = None
    sdkver = None
    sdksimver = None

    def __init__(self):
        super(Context, self).__init__()
        self.include_dirs = []

        ok = True

        sdks = sh.xcodebuild("-showsdks").splitlines()

        # get the latest iphoneos
        iphoneos = [x for x in sdks if "iphoneos" in x]
        if not iphoneos:
            info("No iphone SDK installed")
            ok = False
        else:
            iphoneos = iphoneos[0].split()[-1].replace("iphoneos", "")
            self.sdkver = iphoneos

        # get the latest iphonesimulator version
        iphonesim = [x for x in sdks if "iphonesimulator" in x]
        if not iphonesim:
            ok = False
            info("Error: No iphonesimulator SDK installed")
        else:
            iphonesim = iphonesim[0].split()[-1].replace("iphonesimulator", "")
            self.sdksimver = iphonesim

        # get the path for Developer
        self.devroot = "{}/Platforms/iPhoneOS.platform/Developer".format(
            sh.xcode_select("-print-path").strip())

        # path to the iOS SDK
        self.iossdkroot = "{}/SDKs/iPhoneOS{}.sdk".format(
            self.devroot, self.sdkver)

        # root of the toolchain
        self.root_dir = realpath(dirname(__file__))
        self.build_dir = "{}/build".format(self.root_dir)
        self.cache_dir = "{}/.cache".format(self.root_dir)
        self.dist_dir = "{}/dist".format(self.root_dir)
        self.install_dir = "{}/dist/root".format(self.root_dir)
        self.include_dir = "{}/dist/include".format(self.root_dir)
        self.hostpython = "{}/dist/hostpython/bin/python".format(self.root_dir)
        self.site_packages_dir = "{}/dist/root/python/lib/python2.7/site-packages".format(self.root_dir)
        self.python_ver_dir = "python2.7"

        self.archs = (
            ArchSimulator(self),
            Arch64Simulator(self),
            ArchIOS(self),
            Arch64IOS(self))
        # path to some tools
        self.ccache = sh.which("ccache")
        if not self.ccache:
            #info("ccache is missing, the build will not be optimized in the future.")
            pass
        for cython_fn in ("cython-2.7", "cython"):
            cython = sh.which(cython_fn)
            if cython:
                self.cython = cython
                break
        if not self.cython:
            ok = False
            info("Missing requirement: cython is not installed")

        # check the basic tools
        for tool in ("pkg-config", "autoconf", "automake", "libtool"):
            if not sh.which(tool):
                info("Missing requirement: {} is not installed".format(
                    tool))

        if not ok:
            sys.exit(1)

        self.use_pigz = sh.which('pigz')
        self.use_pbzip2 = sh.which('pbzip2')

        try:
            num_cores = int(sh.sysctl('-n', 'hw.ncpu'))
        except Exception:
            num_cores = None
        self.num_cores = num_cores if num_cores else 4  # default to 4 if we can't detect

        ensure_dir(self.root_dir)
        ensure_dir(self.build_dir)
        ensure_dir(self.cache_dir)
        ensure_dir(self.dist_dir)
        ensure_dir(self.install_dir)
        ensure_dir(self.include_dir)
        ensure_dir(join(self.include_dir, "common"))

        # remove the most obvious flags that can break the compilation
        self.env.pop("MACOSX_DEPLOYMENT_TARGET", None)
        self.env.pop("PYTHONDONTWRITEBYTECODE", None)
        self.env.pop("ARCHFLAGS", None)
        self.env.pop("CFLAGS", None)
        self.env.pop("LDFLAGS", None)

        # set the state
        self.state = JsonStore(join(self.dist_dir, "state.db"))

    @property
    def concurrent_make(self):
        return "-j{}".format(self.num_cores)

    @property
    def concurrent_xcodebuild(self):
        return "IDEBuildOperationMaxNumberOfConcurrentCompileTasks={}".format(self.num_cores)


class Framework(object):
    """ A delegate for building a framework for a recipe. This should be subclassed and
        assigned as the framework of your recipe.

        The goal is to be able to include one Python.framework in the xcode project that includes
        everything required for the app. This means, all Libraries, shared libraries
        (python extensions), and python sources.

    Ex.

        class MyFramework(Framework):
            name = "MyFramework"

        class MyRecipe(Recipe):
            framework = MyFramework()

    #: See the following for more info
    https://developer.apple.com/library/content/documentation/MacOSX/Conceptual/BPFrameworks/Concepts/FrameworkAnatomy.html

    The framework structure created is:

        MyFramework.framework/
            Headers      -> Versions/Current/Headers
            MyFramework  -> Versions/Current/MyFramework
            Resources    -> Versions/Current/Resources
            Libraries    -> Versions/Current/Libraries
            Versions/
                A/
                    Headers/
                        MyHeader.h
                    MyFramework
                    Resources/
                        English.lproj/
                            Documentation
                            InfoPlist.strings
                        Info.plist
                B/
                    Headers/
                        MyHeader.h
                    MyFramework
                    Resources/
                        English.lproj/
                            Documentation
                            InfoPlist.strings
                        Info.plist
                Current  -> B

    """

    #: Name
    name = ""

    #: Bundle id to use for plist
    bundle_id = ""

    #: Add anything you want to override in the plist
    plist = {}

    #: Version code
    version = "A"

    #: Headers to copy, relative to build dir
    #: (can be glob patterns such as include/python2.7/*.h)
    headers = []

    #: Resources to copy relative to build dir
    #:  (can be any glob pattern)
    resources = []

    #: Library to link, relative to the dist dir
    #: the path will be formatted with the arch parameters
    #: and passed to lipo to create a universal library
    library = None

    #: Any sub libraries these are relative to the dist folder
    #: the path will be formatted with the arch parameters
    #: and passed to lipo to create a universal library
    libraries = []

    def build(self, recipe):
        """ Create a framework for this recipe
        """
        info("Building or adding to {}.framework...".format(self.name))

        #: Copy ctx and recipe
        self.ctx = recipe.ctx
        self.recipe = recipe

        framework_dir = recipe.get_framework_dir()

        if not hasattr(recipe,'build_dir'):
            recipe.build_dir = recipe.get_build_dir(recipe.filtered_archs[0].arch)

        if not exists(framework_dir):
            os.makedirs(framework_dir)

        #: Create framework folder structure
        with current_directory(framework_dir):
            version_dir = join('Versions', self.version)

            if not exists(version_dir):
                os.makedirs(version_dir)

            with current_directory(version_dir):
                self.install_headers(recipe)
                self.install_resources(recipe)
                self.install_binary(recipe)
                self.install_libraries(recipe)

            #: Finally create symlinkes to the current version
            self.install_links(recipe)

            #: Create Info.plist
            self.install_plist(recipe)

    def install_headers(self, recipe):
        """ Install headers.
        Current directory is the framework's version folder.
            ex. MyFramework.framework/Versions/A/

        """
        if not self.headers:
            return

        #: Create and copy headers
        if not exists('Headers'):
            os.makedirs('Headers')

        #: Copy to headers
        with current_directory('Headers'):
            for pattern in self.headers:
                for h in glob.glob(join(recipe.build_dir, pattern)):
                    info("Adding Header {} to {}.framework...".format(h, self.name))
                    shprint(sh.cp, '-Rf', h, '.')

    def install_resources(self, recipe):
        """ Install any resources the framework requires.
            Current directory is the framework's version folder.
        """
        if not self.resources:
            return

        #: Create and copy headers
        if not exists('Resources'):
            os.makedirs('Resources')

        #: Copy to headers
        with current_directory('Resources'):

            for pattern in self.resources:
                for r in glob.glob(join(recipe.build_dir, pattern)):
                    info("Adding Resource {} to {}.framework...".format(r, self.name))
                    shprint(sh.cp, '-Rf', r, '.')

    def install_plist(self, recipe):
        """ Create or update the Info.plist file required by a framework.
        """
        #: Already created and  we don't want to update it
        if exists('Info.plist') and not self.plist:
            return

        if exists('Info.plist'):
            #: Read existing
            plist = plistlib.readPlist('Info.plist')
        else:
            #: Create new  Info.plist
            plist = dict(
                CFBundleDevelopmentRegion="en",  #: Shouldn't hard code..
                CFBundleExecutable=self.name,
                CFBundleIdentifier=self.bundle_id or self.name,
                CFBundleInfoDictionaryVersion="6.0",
                CFBundleName=self.name,
                CFBundlePackageType="FMWK",
                CFBundleShortVersionString=self.version,
                CFBundleVersion=self.version,
                NSPrincipalClass="",
            )

        #: Update with any customized params
        plist.update(self.plist)

        #: Save it
        plistlib.writePlist(plist,'Info.plist')

    def install_libraries(self, recipe):
        """ Install any libraries the framework requires.
            Current directory is the framework's version folder.
        """
        if not self.libraries:
            return

        #: Create and copy libraries
        if not exists('Libraries'):
            os.makedirs('Libraries')
        with current_directory('Libraries'):
            for library in self.libraries:
                info("Adding Library {} to {}.framework...".format(library, self.name))

                #: Allow glob patterns
                if '*' in library:
                    #: Expand the glob pattern for each arch and run lipo for each created
                    libs = {}
                    for arch in recipe.filtered_archs:
                        pattern = join(recipe.ctx.dist_dir, library.format(arch=arch.arch))
                        for lib in glob.glob(pattern):
                            libname = os.path.split(lib)[-1]
                            if libname not in libs:
                                libs[libname] = []
                            libs[libname].append(lib)

                    for lib in libs:
                        dest = os.path.split(lib)[-1]
                        self.lipo(recipe, libs[lib], dest)
                else:
                    dest = os.path.split(library)[-1]
                    lib = join(recipe.ctx.dist_dir, library)

                    #: Make a universal library and saves it to the destination
                    self.lipo(recipe, lib, dest)

    def install_binary(self, recipe):
        """ Install any resources the framework requires.
            Current directory is the framework's version folder.
        """
        if not self.library:
            return
        info("Adding Binary {} to {}.framework...".format(self.library, self.name))
        #: Copy the library renamed to the framework name
        framework_binary = join(recipe.ctx.dist_dir, self.library)

        #: Make a universal library and saves it to the destination
        self.lipo(recipe, framework_binary, self.name)

    def install_links(self, recipe):
        """ Create symlinks to the current version of this framework.
            Current directory is the framework folder.

        """
        #: Create version symlink
        if not exists('Versions/Current'):
            shprint(sh.ln, '-sf', '{}'.format(self.version), 'Versions/Current')

        #: Create symlinks (if required)
        for path in ['Headers', 'Resources', 'Libraries', self.name]:
            if exists('Versions/Current/{}'.format(path)) and not exists(path):
                shprint(sh.ln, '-sf', 'Versions/Current/{}'.format(path), path)

    def lipo(self, recipe, lib, dest):
        """ Run lipo on the given library and return the generated output
            that supports every arch.

            lib can be either a str or list. If it's a list it will be passed
            directly to lipo. If it's a string it will be formatted with each
            arch and then passed to lipo.

        """
        if isinstance(lib, (tuple, list)):
            libs = lib
        else:
            #: Format for each arch
            libs = [lib.format(arch=arch.arch) for arch in recipe.filtered_archs]
        shprint(sh.lipo, '-output', dest, '-create', *libs)


class FrameworkLibrary(Framework):
    """
        A framework that ADDS libraries to the Python framework
        this should be used for pretty much everything except the python recipe itself.

        If you need to use headers from this library, don't use this, instead
        create a separate framework for it.


        For example:

            Python.framework:
                Versions:
                    2.7:
                        Libraries:
                            yourlib.dylib # <-- libraries added here

        Note: the actual python recipe may not exist yet.
    """
    #: Add to the Python framework by default
    name = "Python"

    #: Add to python version 2.7
    version = "2.7"

    #: Add your libraries here
    libraries = []


class Recipe(object):
    #: Version to build
    version = None

    #: Unformatted url where the source can be downloaded
    url = None

    #: Arches that are supported
    archs = []

    #: Dependent recipes
    depends = []

    #: Optional dependencies
    optional_depends = []

    #: Library that will be built by this recipe
    library = None

    #: Libraries that will be built by this recipe
    libraries = []

    #: Include sources from this directory
    include_dir = None

    #: Include sources are specific to each arch
    #: and should be copied for each
    include_per_arch = False

    #: Name of framework to build, excluding .framework ex (Python)
    framework = None

    #: Version to use when creating the framework, by default uses the recipe version
    framework_version = None

    #: Frameworks to include
    frameworks = []

    #: Sources to include
    sources = []

    #: Idk what these are
    pbx_frameworks = []
    pbx_libraries = []

    # API available for recipes
    def download_file(self, url, filename, cwd=None):
        """
        Download an `url` to `outfn`
        """
        if not url:
            return

        def report_hook(index, blksize, size):
            if size <= 0:
                progression = '{0} bytes'.format(index * blksize)
            else:
                progression = '{0:.2f}%'.format(
                        index * blksize * 100. / float(size))
            stdout.write('- Download {}\r'.format(progression))
            stdout.flush()

        if cwd:
            filename = join(cwd, filename)
        if exists(filename):
            unlink(filename)

        # Clean up temporary files just in case before downloading.
        urlcleanup()

        info('Downloading {0}'.format(url))
        urlretrieve(url, filename, report_hook)
        return filename

    def extract_file(self, filename, cwd):
        """
        Extract the `filename` into the directory `cwd`.
        """
        if not filename:
            return
        info("Extract {} into {}".format(filename, cwd))
        if filename.endswith(".tgz") or filename.endswith(".tar.gz"):
            if self.ctx.use_pigz:
                comp = '--use-compress-program={}'.format(self.ctx.use_pigz)
            else:
                comp = '-z'
            shprint(sh.tar, "-C", cwd, "-xv", comp, "-f", filename)

        elif filename.endswith(".tbz2") or filename.endswith(".tar.bz2"):
            if self.ctx.use_pbzip2:
                comp = '--use-compress-program={}'.format(self.ctx.use_pbzip2)
            else:
                comp = '-j'
            shprint(sh.tar, "-C", cwd, "-xv", comp, "-f", filename)

        elif filename.endswith(".zip"):
            shprint(sh.unzip, "-d", cwd, filename)

        else:
            info("Error: cannot extract, unrecognized extension for {}".format(
                filename))
            raise Exception()

    def get_archive_rootdir(self, filename):
        if filename.endswith(".tgz") or filename.endswith(".tar.gz") or \
                filename.endswith(".tbz2") or filename.endswith(".tar.bz2"):
            try:
                archive = tarfile.open(filename)
            except tarfile.ReadError:
                info('Error extracting the archive {0}'.format(filename))
                info('This is usually caused by a corrupt download. The file'
                      ' will be removed and re-downloaded on the next run.')
                remove(filename)
                return

            root = archive.next().path.split("/")
            return root[0]
        elif filename.endswith(".zip"):
            with zipfile.ZipFile(filename) as zf:
                return dirname(zf.namelist()[0])
        else:
            info("Error: cannot detect root directory")
            info("Unrecognized extension for {}".format(filename))
            raise Exception()

    def apply_patch(self, filename, target_dir=''):
        """
        Apply a patch from the current recipe directory into the current
        build directory.
        """
        target_dir = target_dir or self.build_dir
        info("Apply patch {}".format(filename))
        filename = join(self.recipe_dir, filename)
        sh.patch("-t", "-d", target_dir, "-p1", "-i", filename)

    def copy_file(self, filename, dest):
        """
        Copy a file from the recipe folder
        to somewhere in the build folder.
        """
        info("Copy {} to {}".format(filename, dest))
        filename = join(self.recipe_dir, filename)
        dest = join(self.build_dir, dest)
        shutil.copy(filename, dest)

    def append_file(self, filename, dest):
        info("Append {} to {}".format(filename, dest))
        filename = join(self.recipe_dir, filename)
        dest = join(self.build_dir, dest)
        with open(filename, "rb") as fd:
            data = fd.read()
        with open(dest, "ab") as fd:
            fd.write(data)

    def has_marker(self, marker):
        """
        Return True if the current build directory has the marker set
        """
        return exists(join(self.build_dir, ".{}".format(marker)))

    def set_marker(self, marker):
        """
        Set a marker info the current build directory
        """
        with open(join(self.build_dir, ".{}".format(marker)), "w") as fd:
            fd.write("ok")

    def delete_marker(self, marker):
        """
        Delete a specific marker
        """
        try:
            unlink(join(self.build_dir, ".{}".format(marker)))
        except:
            pass

    def get_include_dir(self):
        """
        Return the common include dir for this recipe
        """
        return join(self.ctx.include_dir, "common", self.name)

    @property
    def name(self):
        modname = self.__class__.__module__
        return modname.split(".", 1)[-1]

    @property
    def archive_fn(self):
        bfn = basename(self.url.format(version=self.version))
        fn = "{}/{}-{}".format(
            self.ctx.cache_dir,
            self.name, bfn)
        return fn

    @property
    def filtered_archs(self):
        result = []
        for arch in self.ctx.archs:
            if not self.archs or (arch.arch in self.archs):
                result.append(arch)
        return result

    @property
    def dist_libraries(self):
        libraries = []
        name = self.name
        if not name.startswith("lib"):
            name = "lib{}".format(name)
        if self.library:
            static_fn = join(self.ctx.dist_dir, "lib", "{}.a".format(name))
            libraries.append(static_fn)
        for library in self.libraries:
            static_fn = join(self.ctx.dist_dir, "lib", basename(library))
            libraries.append(static_fn)
        return libraries

    def get_build_dir(self, arch):
        return join(self.ctx.build_dir, self.name, arch, self.archive_root)

    # Public Recipe API to be subclassed if needed

    def init_with_ctx(self, ctx):
        self.ctx = ctx
        include_dir = None
        if self.include_dir:
            if self.include_per_arch:
                include_dir = join("{arch.arch}", self.name)
            else:
                include_dir = join("common", self.name)
        if include_dir:
            info("Include dir added: {}".format(include_dir))
            self.ctx.include_dirs.append(include_dir)

    def get_recipe_env(self, arch=None):
        """Return the env specialized for the recipe
        """
        if arch is None:
            arch = self.filtered_archs[0]
        return arch.get_env()

    @property
    def archive_root(self):
        key = "{}.archive_root".format(self.name)
        value = self.ctx.state.get(key)
        if not value:
            value = self.get_archive_rootdir(self.archive_fn)
            if value is not None:
                self.ctx.state[key] = value
        return value

    def execute(self):
        """ Build api """
        if self.custom_dir:
            self.ctx.state.remove_all(self.name)
        self.download()
        self.extract()
        self.build_all()

    @property
    def custom_dir(self):
        """Check if there is a variable name to specify a custom version /
        directory to use instead of the current url.
        """
        envname = "{}_DIR".format(self.name.upper())
        d = environ.get(envname)
        if not d:
            return
        if not exists(d):
            raise ValueError("Invalid path passed into {}".format(envname))
        return d

    @cache_execution
    def download(self):
        key = "{}.archive_root".format(self.name)
        if self.custom_dir:
            self.ctx.state[key] = basename(self.custom_dir)
        else:
            src_dir = join(self.recipe_dir, self.url)
            if exists(src_dir):
                self.ctx.state[key] = basename(src_dir)
                return
            fn = self.archive_fn
            if not exists(fn):
                self.download_file(self.url.format(version=self.version), fn)
            status = self.get_archive_rootdir(self.archive_fn)
            if status is not None:
                self.ctx.state[key] = status

    @cache_execution
    def extract(self):
        # recipe tmp directory
        for arch in self.filtered_archs:
            info("Extract {} for {}".format(self.name, arch.arch))
            self.extract_arch(arch.arch)

    def extract_arch(self, arch):
        build_dir = join(self.ctx.build_dir, self.name, arch)
        dest_dir = join(build_dir, self.archive_root)
        if self.custom_dir:
            if exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(self.custom_dir, dest_dir)
        else:
            if exists(dest_dir):
                return
            src_dir = join(self.recipe_dir, self.url)
            if exists(src_dir):
                shutil.copytree(src_dir, dest_dir)
                return
            ensure_dir(build_dir)
            self.extract_file(self.archive_fn, build_dir)

    @cache_execution
    def build(self, arch):
        self.build_dir = self.get_build_dir(arch.arch)
        if self.has_marker("building"):
            info("Warning: {} build for {} was incomplete".format(
                self.name, arch.arch))
            info("Warning: deleting the build and restarting.")
            shutil.rmtree(self.build_dir)
            self.extract_arch(arch.arch)

        if self.has_marker("build_done"):
            info("Build python for {} already done.".format(arch.arch))
            return

        self.set_marker("building")

        chdir(self.build_dir)
        info("Prebuild {} for {}".format(self.name, arch.arch))
        self.prebuild_arch(arch)
        info("Build {} for {}".format(self.name, arch.arch))
        self.build_arch(arch)
        info("Postbuild {} for {}".format(self.name, arch.arch))
        self.postbuild_arch(arch)
        self.delete_marker("building")
        self.set_marker("build_done")

    @cache_execution
    def build_all(self):
        filtered_archs = self.filtered_archs
        info("Build {} for {} (filtered)".format(
            self.name,
            ", ".join([x.arch for x in filtered_archs])))

        #: Build each
        for arch in self.filtered_archs:
            self.build(arch)

        #: Create a 'universal' library
        self.build_library()

        #: Create a framework using the universal library
        self.build_framework()

        info("Install include files for {}".format(self.name))
        self.install_include()
        info("Install frameworks for {}".format(self.name))
        self.install_frameworks()
        info("Install sources for {}".format(self.name))
        self.install_sources()
        info("Install {}".format(self.name))
        self.install()

    def prebuild_arch(self, arch):
        prebuild = "prebuild_{}".format(arch.arch)
        if hasattr(self, prebuild):
            getattr(self, prebuild)()

    def build_arch(self, arch):
        build = "build_{}".format(arch.arch)
        if hasattr(self, build):
            getattr(self, build)()

    def postbuild_arch(self, arch):
        postbuild = "postbuild_{}".format(arch.arch)
        if hasattr(self, postbuild):
            getattr(self, postbuild)()

    def build_library(self):
        """ Build a cross platform library that supports multiple arches """
        name = self.name
        #: NO LONGER DO STATIC LIBRARIES
        if self.library:
            info("Create lipo library for {}".format(name))
            if not name.startswith("lib"):
                name = "lib{}".format(name)
            static_fn = join(self.ctx.dist_dir, "lib", "{}.a".format(name))
            ensure_dir(dirname(static_fn))
            info("Lipo {} to {}".format(self.name, static_fn))
            self.make_lipo(static_fn)
        if self.libraries:
            info("Create multiple lipo for {}".format(name))
            for library in self.libraries:
                static_fn = join(self.ctx.dist_dir, "lib", basename(library))
                ensure_dir(dirname(static_fn))
                info("  - Lipo-ize {}".format(library))
                self.make_lipo(static_fn, library)

    def get_framework_dir(self):
        """ Return directory where framework will go """
        if not self.framework:
            raise RuntimeError("This recipe does not have a framework. "
                               "Please define a framework if this is needed.")
        return join(self.ctx.dist_dir, 'frameworks', '{}.framework'.format(self.framework.name))

    def build_framework(self):
        """ Build a framework for this recipe """
        if self.framework:
            self.framework.build(self)

    @cache_execution
    def make_lipo(self, filename, library=None):
        library = library or self.library
        if not library:
            return
        args = []
        for arch in self.filtered_archs:
            library_fn = library.format(arch=arch)
            args += [
                "-arch", arch.arch,
                join(self.get_build_dir(arch.arch), library_fn)]
        shprint(sh.lipo, "-create", "-output", filename, *args)

    @cache_execution
    def install_frameworks(self):
        if not self.frameworks:
            return
        arch = self.filtered_archs[0]
        build_dir = self.get_build_dir(arch.arch)
        for framework in self.frameworks:
            info(" - Install {}".format(framework))
            src = join(build_dir, framework)
            dest = join(self.ctx.dist_dir, "frameworks", framework)
            ensure_dir(dirname(dest))
            if exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(src, dest)

    @cache_execution
    def install_sources(self):
        if not self.sources:
            return
        arch = self.filtered_archs[0]
        build_dir = self.get_build_dir(arch.arch)
        for source in self.sources:
            info(" - Install {}".format(source))
            src = join(build_dir, source)
            dest = join(self.ctx.dist_dir, "sources", self.name)
            ensure_dir(dirname(dest))
            if exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(src, dest)

    @cache_execution
    def install_include(self):
        if not self.include_dir:
            return
        if self.include_per_arch:
            archs = self.ctx.archs
        else:
            archs = self.filtered_archs[:1]

        include_dirs = self.include_dir
        if not isinstance(include_dirs, (list, tuple)):
            include_dirs = list([include_dirs])

        for arch in archs:
            arch_dir = "common"
            if self.include_per_arch:
                arch_dir = arch.arch
            dest_dir = join(self.ctx.include_dir, arch_dir, self.name)
            if exists(dest_dir):
                shutil.rmtree(dest_dir)
            build_dir = self.get_build_dir(arch.arch)

            for include_dir in include_dirs:
                dest_name = None
                if isinstance(include_dir, (list, tuple)):
                    include_dir, dest_name = include_dir
                include_dir = include_dir.format(arch=arch, ctx=self.ctx)
                src_dir = join(build_dir, include_dir)
                if dest_name is None:
                    dest_name = basename(src_dir)
                if isdir(src_dir):
                    shutil.copytree(src_dir, dest_dir)
                else:
                    dest = join(dest_dir, dest_name)
                    info("Copy {} to {}".format(src_dir, dest))
                    ensure_dir(dirname(dest))
                    shutil.copy(src_dir, dest)

    @cache_execution
    def install(self):
        pass

    @classmethod
    def list_recipes(cls):
        recipes_dir = join(dirname(__file__), "recipes")
        for name in listdir(recipes_dir):
            fn = join(recipes_dir, name)
            if isdir(fn):
                yield name

    @classmethod
    def get_recipe(cls, name, ctx):
        if not hasattr(cls, "recipes"):
           cls.recipes = {}

        if '==' in name:
            name, version = name.split('==')
        else:
            version = None

        if name in cls.recipes:
            recipe = cls.recipes[name]
        else:
            mod = importlib.import_module("recipes.{}".format(name))
            recipe = mod.recipe
            recipe.recipe_dir = join(ctx.root_dir, "recipes", name)

        if version:
            recipe.version = version

        return recipe


class PythonRecipe(Recipe):
    @cache_execution
    def install(self):
        self.install_python_package()
        self.reduce_python_package()

    @staticmethod
    def remove_junk(d):
        exts = []#".pyc", ".py", ".so.lib", ".so.o", ".sh"]
        for root, dirnames, filenames in walk(d):
            for fn in filenames:
                if any([fn.endswith(ext) for ext in exts]):
                    unlink(join(root, fn))

    def install_python_package(self, name=None, env=None, is_dir=True):
        """Automate the installation of a Python package into the target
        site-packages.

        It will works with the first filtered_archs, and the name of the recipe.
        """
        arch = self.filtered_archs[0]
        if name is None:
            name = self.name
        if env is None:
            env = self.get_recipe_env(arch)
        info("Install {} into the site-packages".format(name))
        build_dir = self.get_build_dir(arch.arch)
        chdir(build_dir)
        hostpython = sh.Command(self.ctx.hostpython)

        #: Install in isobuild folder, make sure python path exists or setuptools complains
        install_dir = join(build_dir, "install")
        site_packages_dir = join(install_dir,'lib','python2.7','site-packages')
        env['PYTHONPATH'] = ":".join([install_dir,site_packages_dir])

        if not exists(site_packages_dir):
            os.makedirs(site_packages_dir)

        shprint(hostpython, "setup.py", "install", "-O2",
                "--prefix", install_dir, _env=env)
        dest_dir = join(self.ctx.site_packages_dir, name)

        # #self.remove_junk(install_dir)
        # if is_dir:
        #     if exists(dest_dir):
        #         shutil.rmtree(dest_dir)
        #     func = shutil.copytree
        # else:
        #     func = shutil.copy
        # func(
        #     join(install_dir, "lib",
        #          self.ctx.python_ver_dir, "site-packages", name),
        #     dest_dir)

    def reduce_python_package(self):
        """Feel free to remove things you don't want in the final
        site-packages.
        """
        pass


class PipRecipe(PythonRecipe):
    """  Recipe for recipes not found (assume install by pip)"""

    def execute(self):
        with current_directory('build'):
            if not exists('venv'):
                shprint(sh.virtualenv,'venv')
            info("Installing {} via pip".format(self.name))
            shprint(sh.bash,'-c','source venv/bin/activate && '
                                 'pip install {} --target={}'.format(self.name,self.ctx.site_packages_dir))
            info("{} installed!".format(self.name))

            #: Compile to pyo
            #: Compile pip packages to bytecode
            shprint(sh.bash,
                '-c',
                "source venv/bin/activate && env CC=/bin/false CXX=/bin/false "
                "python -O -m compileall -f {0}".format(self.ctx.site_packages_dir))

            #: Clean .dist-info etc..
        self.reduce_python_package()

    def reduce_python_package(self):
        with current_directory(self.ctx.site_packages_dir):
            #shprint(sh.find,'.','-type','f','-name','*.py','-delete')
            shprint(sh.find,'.','-type','f','-name','*.pyc','-delete')
            #shprint(sh.find,'.','-type','f','-name','*.pyo','-delete') #: Use pyo
            for p in [
                'enaml/qt',
                'tornado/test',
                '*.egg-info',
                '*.dist-info',
                'tests',
                'usr',
            ]:
                try:
                    sh.rm('-R', *glob.glob(p))
                except:
                    pass


class PythonExtensionRecipe(PythonRecipe):
    """ Add common methods and environment variables
        needed for compiling extensions.

    """

    def get_local_arch(self, arch):
        if arch.arch == "arm64":
            return "aarch64"
        elif arch.arch=="armv7":
            return "arm"
        else:
            return arch.arch

    def prebuild_arch(self, arch):
        """ Make sure libpython.dylib exists under dist/lib/<arch>/
            by simlinking to the current version
        """

        with current_directory(join(self.ctx.dist_dir, 'lib', arch.arch)):
            if not exists('libpython.dylib'):
                #: Make a simlink
                shprint(sh.ln, '-sf', 'libpython2.7.dylib', 'libpython.dylib')

    def install_sysconfigdata(self, arch):
        """ Hostpython needs _sysconfigdata for the arch we are building
            so copy it to the build directory.
        """
        build_dir = self.get_build_dir(arch.arch)
        local_arch = self.get_local_arch(arch)

        with current_directory(build_dir):
            #: Copy _sysconfigdata to hostpython
            _sysconfigdata = join(self.ctx.build_dir, 'python', arch.arch,
                                  'Python-2.7.13', 'build',
                                  'lib.darwin-{}-2.7'.format(local_arch),
                                  '_sysconfigdata.py')
            #: Copy python config here
            shprint(sh.cp,_sysconfigdata, '.')

            #: Patch SO name
            #: it already builds Mach-O libraries but the filetype is wrong
            shprint(sh.sed, '-id', "s!'SO': '.so',!'SO': '.dylib',!", '_sysconfigdata.py')


    def install_modules(self, arch):
        """Automate the installation of a Python package into the target
        site-packages.

        """
        env = self.get_recipe_env(arch)
        build_dir = self.get_build_dir(arch.arch)
        with current_directory(join(build_dir, 'build',
                                    'lib.{}-2.7'.format(env['_PYTHON_HOST_PLATFORM']))):
            dest = join(self.ctx.dist_dir, 'python', arch.arch)
            if not exists(dest):
                os.makedirs(dest)

            #: Find all the so files
            for f in sh.find('.','-name','*.dylib').strip().split("\n"):
                so_name = ".".join(f.split("/")[1:])
                so_file = join(dest, so_name)
                if exists(so_file):
                    os.remove(so_file)
                #: Copy
                shprint(sh.mv, f, so_file)

    def get_recipe_env(self, arch):
        env = super(PythonExtensionRecipe, self).get_recipe_env(arch)
        #env['PYTHONHOME'] = join(self.ctx.dist_dir,'hostpython','lib','python2.7')
        env["KIVYIOSROOT"] = self.ctx.root_dir
        env["IOSSDKROOT"] = arch.sysroot
        #: LIB LINK NOT USED
        #env["LDSHARED"] = join(self.ctx.root_dir, "tools", "liblink")
        env["ARM_LD"] = env["LD"]
        env["ARCH"] = arch.arch

        env["C_INCLUDE_PATH"] = join(arch.sysroot, "usr", "include")
        env["LIBRARY_PATH"] = join(arch.sysroot, "usr", "lib")

        #: Tell the compiler we want to include headers from libffi
        #: and use bitcode. Update no bitcode
        #env["CFLAGS"] += " -fembed-bitcode -I{}".format(
        env["CFLAGS"] += " -I{}".format(
            join(self.ctx.dist_dir, "include", arch.arch, "libffi"),
            #join(self.ctx.dist_dir, "lib", arch.arch, "libbz2"),
        )

        #: Magic flag for osx cross compiling
        env['_PYTHON_HOST_PLATFORM'] = 'darwin-{}'.format(self.get_local_arch(arch))

        #: Tell the loader we want to load libraries from dist/lib/arch
        env['LDFLAGS'] += " -L{}".format(
            join(self.ctx.dist_dir, "lib", arch.arch),
        )

        #: We want to link python
        env["LDFLAGS"] += " -lpython"# -lffi -lz"

        #: If you need to link ssl add this
        # if "openssl.build_all" in self.ctx.state:
        #     env['LDFLAGS'] += " -lssl -lcrypto"
        #     env['CFLAGS'] += " -I{}".format(
        #         join(self.ctx.dist_dir, "include", arch.arch, "openssl"),
        #     )
        return env


class CythonRecipe(PythonExtensionRecipe):
    """ Use for python extensions that use cython (.pyx files) """
    pre_build_ext = False
    cythonize = True

    def cythonize_file(self, filename):
        """ Convert a cython .pyx file to .c """
        if filename.startswith(self.build_dir):
            filename = filename[len(self.build_dir) + 1:]
        info("Cythonize {}".format(filename))
        cmd = sh.Command(join(self.ctx.root_dir, "tools", "cythonize.py"))
        shprint(cmd, filename)

    def cythonize_build(self):
        """ Convert all cython files to .c files """
        if not self.cythonize:
            return
        root_dir = self.build_dir
        for root, dirnames, filenames in walk(root_dir):
            for filename in fnmatch.filter(filenames, "*.pyx"):
                self.cythonize_file(join(root, filename))

    def biglink(self):
        raise RuntimeError("biglink IS DISABLED") #: We're building shared libs
        dirs = []
        for root, dirnames, filenames in walk(self.build_dir):
            if fnmatch.filter(filenames, "*.so.libs"):
                dirs.append(root)
        cmd = sh.Command(join(self.ctx.root_dir, "tools", "biglink"))
        shprint(cmd, join(self.build_dir, "lib{}.a".format(self.name)), *dirs)

    def build_arch(self, arch):
        """ Build a recipe with cython files """
        build_env = self.get_recipe_env(arch)
        hostpython = sh.Command(self.ctx.hostpython)
        build_dir = self.get_build_dir(arch.arch)

        with current_directory(build_dir):
            self.install_sysconfigdata(arch)

            if self.pre_build_ext:
                try:
                    #: This build should fail because there is no cython in the hostpython env
                    #: so it fails to compile, but it generates the necessary files for cythonizing
                    shprint(hostpython, "setup.py", "build_ext", "--debug",
                            _env=build_env)
                except:
                    pass

            #: Convert pyx to .c using your SYSTEM cython, NOT hostpython.
            self.cythonize_build()

            #: Build using the regular compiler
            shprint(hostpython, "setup.py", "build_ext", "--debug",
                    _env=build_env)

            #: Now copy all the compiled libraries
            self.install_modules(arch)


class CppPythonRecipe(PythonExtensionRecipe):
    """ Recipe for Python Extensions that use C++ """

    def get_recipe_env(self, arch):
        env = super(CppPythonRecipe, self).get_recipe_env(arch)

        env['PYTHONXCPREFIX'] = self.get_build_dir(arch.arch)

        #: Make sure it's a shared library (should it be dylib --> doesn't make a difference?)
        env['LDFLAGS'] += " -shared"
        env['LDSHARED'] = "{CC} -shared".format(**env)

        #: Cross compile build
        env['CROSS_COMPILE'] = arch.arch
        env['CROSS_COMPILE_TARGET'] = 'yes'

        return env

    def build_arch(self, arch):
        build_env = self.get_recipe_env(arch)
        hostpython = sh.Command(self.ctx.hostpython)
        build_dir = self.get_build_dir(arch.arch)

        with current_directory(build_dir):
            self.install_sysconfigdata(arch)

            shprint(hostpython, "setup.py", "build_ext", "--debug",
                    _env=build_env)

        self.install_package(arch)

    def install(self):
        """ Do our own install"""
        pass

    def install_package(self, arch):
        """Automate the installation of a Python package into the target
        site-packages.

        It will works with the first filtered_archs, and the name of the recipe.
        """
        self.install_modules(arch)
        # env = self.get_recipe_env(arch)
        # info("Install {} into the site-packages".format(self))
        # build_dir = self.get_build_dir(arch.arch)
        # with current_directory(build_dir):
        #     hostpython = sh.Command(self.ctx.hostpython)
        #
        #     #: Install in dist/python/arch folder,
        #     #: make sure python path exists or setuptools complains
        #     install_dir = join(self.ctx.dist_dir, "python", arch.arch)
        #     site_packages_dir = join(install_dir,'lib','python2.7','site-packages')
        #     env['PYTHONPATH'] = ":".join([install_dir,site_packages_dir])
        #
        #     #: Make sure it exists or we blow up
        #     if not exists(site_packages_dir):
        #         os.makedirs(site_packages_dir)
        #
        #     #: Run install into the arch specifc install dir
        #     shprint(hostpython, "setup.py", "install", "-O2",
        #             "--prefix", install_dir, _env=env)
        #
        # self.install_modules(arch)




def build_recipes(names, ctx):
    # gather all the dependencies
    info("Want to build {}".format(names))
    graph = Graph()
    recipe_to_load = names
    recipe_loaded = []
    while names:
        name = recipe_to_load.pop(0)
        if name in recipe_loaded:
            continue
        try:
            recipe = Recipe.get_recipe(name, ctx)
        except ImportError:
            info("Warning: No recipe named {}, creating PipRecipe".format(name))
            recipe = type('{}PipRecipe'.format(name.title),(PipRecipe,),{'name':name})()
            Recipe.recipes[name] = recipe # Add
            #sys.exit(1)
        graph.add(name, name)
        info("Loaded recipe {} (depends of {}, optional are {})".format(name,
            recipe.depends, recipe.optional_depends))
        for depend in recipe.depends:
            graph.add(name, depend)
            recipe_to_load += recipe.depends
        for depend in recipe.optional_depends:
            # in case of compilation after the initial one, take in account
            # of the already compiled recipes
            key = "{}.build_all".format(depend)
            if key in ctx.state:
                recipe_to_load.append(name)
                graph.add(name, depend)
            else:
                graph.add_optional(name, depend)
        recipe_loaded.append(name)

    build_order = list(graph.find_order())
    info("Build order is {}".format(build_order))
    recipes = [Recipe.get_recipe(name, ctx) for name in build_order]
    for recipe in recipes:
        recipe.init_with_ctx(ctx)
    for recipe in recipes:
        recipe.execute()


def ensure_dir(filename):
    if not exists(filename):
        makedirs(filename)


def update_pbxproj(filename):
    # list all the compiled recipes
    ctx = Context()
    pbx_libraries = []
    pbx_frameworks = []
    frameworks = []
    libraries = []
    sources = []
    for recipe in Recipe.list_recipes():
        key = "{}.build_all".format(recipe)
        if key not in ctx.state:
            continue
        recipe = Recipe.get_recipe(recipe, ctx)
        recipe.init_with_ctx(ctx)
        pbx_frameworks.extend(recipe.pbx_frameworks)
        pbx_libraries.extend(recipe.pbx_libraries)
        libraries.extend(recipe.dist_libraries)
        frameworks.extend(recipe.frameworks)
        if recipe.sources:
            sources.append(recipe.name)

    pbx_frameworks = list(set(pbx_frameworks))
    pbx_libraries = list(set(pbx_libraries))
    libraries = list(set(libraries))

    info("-" * 70)
    info("The project need to have:")
    info("iOS Frameworks: {}".format(pbx_frameworks))
    info("iOS Libraries: {}".format(pbx_libraries))
    info("iOS local Frameworks: {}".format(frameworks))
    info("Libraries: {}".format(libraries))
    info("Sources to link: {}".format(sources))

    info("-" * 70)
    info("Analysis of {}".format(filename))

    from mod_pbxproj import XcodeProject
    project = XcodeProject.Load(filename)
    sysroot = sh.xcrun("--sdk", "iphonesimulator", "--show-sdk-path").strip()

    group = project.get_or_create_group("Frameworks")
    g_classes = project.get_or_create_group("Classes")
    for framework in pbx_frameworks:
        framework_name = "{}.framework".format(framework)
        if framework_name in frameworks:
            info("Ensure {} is in the project (local)".format(framework))
            f_path = join(ctx.dist_dir, "frameworks", framework_name)
        else:
            info("Ensure {} is in the project (system)".format(framework))
            f_path = join(sysroot, "System", "Library", "Frameworks",
                          "{}.framework".format(framework))
        project.add_file_if_doesnt_exist(f_path, parent=group, tree="DEVELOPER_DIR")
    for library in pbx_libraries:
        info("Ensure {} is in the project".format(library))
        f_path = join(sysroot, "usr", "lib",
                      "{}.dylib".format(library))
        project.add_file_if_doesnt_exist(f_path, parent=group, tree="DEVELOPER_DIR")
    for library in libraries:
        info("Ensure {} is in the project".format(library))
        project.add_file_if_doesnt_exist(library, parent=group)
    for name in sources:
        info("Ensure {} sources are used".format(name))
        fn = join(ctx.dist_dir, "sources", name)
        project.add_folder(fn, parent=g_classes)


    if project.modified:
        project.backup()
        project.save()


if __name__ == "__main__":
    import argparse
    setup_color('auto')

    class ToolchainCL(object):
        def __init__(self):
            parser = argparse.ArgumentParser(
                    description="Tool for managing the iOS / Python toolchain",
                    usage="""toolchain <command> [<args>]

Available commands:
    build         Build a recipe (compile a library for the required target
                  architecture)
    clean         Clean the build of the specified recipe
    distclean     Clean the build and the result
    recipes       List all the available recipes
    status        List all the recipes and their build status

Xcode:
    create        Create a new xcode project
    update        Update an existing xcode project (frameworks, libraries..)
    launchimage   Create Launch images for your xcode project
    icon          Create Icons for your xcode project
    pip           Install a pip dependency into the distribution
""")
            parser.add_argument("command", help="Command to run")
            args = parser.parse_args(sys.argv[1:2])
            if not hasattr(self, args.command):
                info('Unrecognized command')
                parser.print_help()
                exit(1)
            getattr(self, args.command)()

        def build(self):
            ctx = Context()
            parser = argparse.ArgumentParser(
                    description="Build the toolchain")
            parser.add_argument("recipe", nargs="+", help="Recipe to compile")
            parser.add_argument("--arch", action="append",
                                help="Restrict compilation to this arch")
            parser.add_argument("--concurrency", type=int, default=ctx.num_cores,
                                help="number of concurrent build processes (where supported)")
            parser.add_argument("--no-pigz", action="store_true", default=not bool(ctx.use_pigz),
                                help="do not use pigz for gzip decompression")
            parser.add_argument("--no-pbzip2", action="store_true", default=not bool(ctx.use_pbzip2),
                                help="do not use pbzip2 for bzip2 decompression")
            args = parser.parse_args(sys.argv[2:])

            if args.arch:
                if len(args.arch) == 1:
                    archs = args.arch[0].split()
                else:
                    archs = args.arch
                available_archs = [arch.arch for arch in ctx.archs]
                for arch in archs[:]:
                    if arch not in available_archs:
                        info("ERROR: Architecture {} invalid".format(arch))
                        archs.remove(arch)
                        continue
                ctx.archs = [arch for arch in ctx.archs if arch.arch in archs]
                info("Architectures restricted to: {}".format(archs))
            ctx.num_cores = args.concurrency
            if args.no_pigz:
                ctx.use_pigz = False
            if args.no_pbzip2:
                ctx.use_pbzip2 = False
            ctx.use_pigz = ctx.use_pbzip2
            info("Building with {} processes, where supported".format(ctx.num_cores))
            if ctx.use_pigz:
                info("Using pigz to decompress gzip data")
            if ctx.use_pbzip2:
                info("Using pbzip2 to decompress bzip2 data")
            build_recipes(args.recipe, ctx)

        def recipes(self):
            parser = argparse.ArgumentParser(
                    description="List all the available recipes")
            parser.add_argument(
                    "--compact", action="store_true",
                    help="Produce a compact list suitable for scripting")
            args = parser.parse_args(sys.argv[2:])

            if args.compact:
                info(" ".join(list(Recipe.list_recipes())))
            else:
                ctx = Context()
                for name in Recipe.list_recipes():
                    recipe = Recipe.get_recipe(name, ctx)
                    info("{recipe.name:<12} {recipe.version:<8}".format(
                          recipe=recipe))

        def clean(self):
            parser = argparse.ArgumentParser(
                    description="Clean the build")
            parser.add_argument("recipe", nargs="*", help="Recipe to clean")
            args = parser.parse_args(sys.argv[2:])
            ctx = Context()
            if args.recipe:
                for recipe in args.recipe:
                    info("Cleaning {} build".format(recipe))
                    ctx.state.remove_all("{}.".format(recipe))
                    build_dir = join(ctx.build_dir, recipe)
                    if exists(build_dir):
                        shutil.rmtree(build_dir)
            else:
                info("Delete build directory")
                if exists(ctx.build_dir):
                    shutil.rmtree(ctx.build_dir)

        def distclean(self):
            parser = argparse.ArgumentParser(
                    description="Clean the build, download, and dist")
            args = parser.parse_args(sys.argv[2:])
            ctx = Context()
            if exists(ctx.build_dir):
                shutil.rmtree(ctx.build_dir)
            if exists(ctx.dist_dir):
                shutil.rmtree(ctx.dist_dir)
            if exists(ctx.cache_dir):
                shutil.rmtree(ctx.cache_dir)

        def status(self):
            parser = argparse.ArgumentParser(
                    description="Give a status of the build")
            args = parser.parse_args(sys.argv[2:])
            ctx = Context()
            for recipe in Recipe.list_recipes():
                key = "{}.build_all".format(recipe)
                keytime = "{}.build_all.at".format(recipe)

                if key in ctx.state:
                    status = "Build OK (built at {})".format(ctx.state[keytime])
                else:
                    status = "Not built"
                info("{:<12} - {}".format(
                    recipe, status))

        def create(self):
            parser = argparse.ArgumentParser(
                    description="Create a new xcode project")
            parser.add_argument("name", help="Name of your project")
            parser.add_argument("directory", help="Directory where your project lives")
            args = parser.parse_args(sys.argv[2:])

            from cookiecutter.main import cookiecutter
            ctx = Context()
            template_dir = join(curdir, "tools", "templates")
            context = {
                "title": args.name,
                "project_name": args.name.lower(),
                "domain_name": "org.kivy.{}".format(args.name.lower()),
                "kivy_dir": dirname(realpath(__file__)),
                "project_dir": realpath(args.directory),
                "version": "1.0.0",
                "dist_dir": ctx.dist_dir,
            }
            cookiecutter(template_dir, no_input=True, extra_context=context)
            filename = join(
                    getcwd(),
                    "{}-ios".format(args.name.lower()),
                    "{}.xcodeproj".format(args.name.lower()),
                    "project.pbxproj")
            update_pbxproj(filename)
            info("--")
            info("Project directory : {}-ios".format(
                args.name.lower()))
            info("XCode project     : {0}-ios/{0}.xcodeproj".format(
                args.name.lower()))

        def update(self):
            parser = argparse.ArgumentParser(
                    description="Update an existing xcode project")
            parser.add_argument("filename", help="Path to your project or xcodeproj")
            args = parser.parse_args(sys.argv[2:])

            filename = args.filename
            if not filename.endswith(".xcodeproj"):
                # try to find the xcodeproj
                from glob import glob
                xcodeproj = glob(join(filename, "*.xcodeproj"))
                if not xcodeproj:
                    info("ERROR: Unable to find a xcodeproj in {}".format(filename))
                    sys.exit(1)
                filename = xcodeproj[0]

            filename = join(filename, "project.pbxproj")
            if not exists(filename):
                info("ERROR: {} not found".format(filename))
                sys.exit(1)

            update_pbxproj(filename)
            info("--")
            info("Project {} updated".format(filename))

        def pip(self):
            ctx = Context()
            for recipe in Recipe.list_recipes():
                key = "{}.build_all".format(recipe)
                if key not in ctx.state:
                    continue
                recipe = Recipe.get_recipe(recipe, ctx)
                recipe.init_with_ctx(ctx)
            if not hasattr(ctx, "site_packages_dir"):
                info("ERROR: python must be compiled before using pip")
                sys.exit(1)

            pip_env = {
                "CC": "/bin/false",
                "CXX": "/bin/false",
                "PYTHONPATH": ctx.site_packages_dir,
                "PYTHONOPTIMIZE": "2",
                # "PIP_INSTALL_TARGET": ctx.site_packages_dir
            }
            pip_path = sh.which("pip2")
            pip_args = []
            if len(sys.argv) > 2 and sys.argv[2] == "install":
                pip_args = ["--isolated", "--prefix", ctx.python_prefix]
                args = [pip_path] + [sys.argv[2]] + pip_args + sys.argv[3:]
            else:
                args = [pip_path] + pip_args + sys.argv[2:]

            if not pip_path:
                info("ERROR: pip not found")
                sys.exit(1)
            import os
            info("-- execute pip with: {}".format(args))
            os.execve(pip_path, args, pip_env)

        def launchimage(self):
            import xcassets
            self._xcassets("LaunchImage", xcassets.launchimage)

        def icon(self):
            import xcassets
            self._xcassets("Icon", xcassets.icon)

        def xcode(self):
            parser = argparse.ArgumentParser(description="Open the xcode project")
            parser.add_argument("filename", help="Path to your project or xcodeproj")
            args = parser.parse_args(sys.argv[2:])
            filename = args.filename
            if not filename.endswith(".xcodeproj"):
                # try to find the xcodeproj
                from glob import glob
                xcodeproj = glob(join(filename, "*.xcodeproj"))
                if not xcodeproj:
                    info("ERROR: Unable to find a xcodeproj in {}".format(filename))
                    sys.exit(1)
                filename = xcodeproj[0]
            sh.open(filename)

        def _xcassets(self, title, command):
            parser = argparse.ArgumentParser(
                    description="Generate {} for your project".format(title))
            parser.add_argument("filename", help="Path to your project or xcodeproj")
            parser.add_argument("image", help="Path to your initial {}.png".format(title.lower()))
            args = parser.parse_args(sys.argv[2:])

            if not exists(args.image):
                info("ERROR: image path does not exists.")
                return

            filename = args.filename
            if not filename.endswith(".xcodeproj"):
                # try to find the xcodeproj
                from glob import glob
                xcodeproj = glob(join(filename, "*.xcodeproj"))
                if not xcodeproj:
                    info("ERROR: Unable to find a xcodeproj in {}".format(filename))
                    sys.exit(1)
                filename = xcodeproj[0]

            project_name = filename.split("/")[-1].replace(".xcodeproj", "")
            images_xcassets = realpath(join(filename, "..", project_name,
                "Images.xcassets"))
            if not exists(images_xcassets):
                info("WARNING: Images.xcassets not found, creating it.")
                makedirs(images_xcassets)
            info("Images.xcassets located at {}".format(images_xcassets))

            command(images_xcassets, args.image)

    ToolchainCL()
