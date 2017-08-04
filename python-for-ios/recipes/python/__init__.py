from toolchain import Recipe, Framework, shprint, current_directory, info
from os.path import join, exists
import sh
import os


class PythonFramework(Framework):
    name = "Python"
    version = "2.7"
    bundle_id = "com.frmdstryr.enamlnative.Python"
    headers = ["Include/*.h", "pyconfig.h"]
    library = "lib/{arch}/libpython2.7.dylib"
    libraries = ["lib/{arch}/libpython2.7.dylib"]
    resources = []

    def install_binary(self, recipe):
        """ We want linked extensions to be able to use libpython from the Libraries
            so instead of dupilcating it, use a symlink.
        """

        info("Adding a simlink of Python {} to {}.framework...".format(self.library, self.name))
        #: Copy the library renamed to the framework name
        libname = os.path.split(self.library)[-1]

        #: Make a universal library and saves it to the destination
        shprint(sh.ln, '-sf', 'Libraries/{}'.format(libname), self.name)


class PythonRecipe(Recipe):
    version = "2.7.13"
    url = "https://www.python.org/ftp/python/{version}/Python-{version}.tgz"
    depends = ["libffi", ]
    optional_depends = ["openssl"]
    #library = "libpython2.7.dylib"
    framework = PythonFramework()
    pbx_libraries = ["libz", "libbz2", "libsqlite3"]

    def init_with_ctx(self, ctx):
        super(PythonRecipe, self).init_with_ctx(ctx)
        self.ctx.python_ver_dir = "python2.7"
        self.ctx.site_packages_dir = join(
            ctx.dist_dir, "root", "python", "lib", ctx.python_ver_dir,
            "site-packages")

    def prebuild_arch(self, arch):
        # common to all archs
        if  self.has_marker("patched"):
            return
        self.apply_patch("ssize-t-max.patch")
        #self.apply_patch("dynload.patch")
        self.apply_patch("static-_sqlite3.patch")
        self.copy_file("ModulesSetup", "Modules/Setup.local")
        self.copy_file("_scproxy.py", "Lib/_scproxy.py")
        self.apply_patch("xcompile.patch")
        self.apply_patch("setuppath.patch")
        self.append_file("ModulesSetup.mobile", "Modules/Setup.local")
        if "openssl.build_all" in self.ctx.state:
             self.append_file("ModulesSetup.openssl", "Modules/Setup.local")

        self.set_marker("patched")

    def build_arch(self, arch):
        build_env = arch.get_env()
        #build_env['ENABLE_BITCODE'] = "YES"

        #: Required flag or we get linking errors when loading from a framework!
        build_env['LDFLAGS'] += " -lffi"

        if "openssl.build_all" in self.ctx.state:
            #: Probably not the place to put it but make an ln to the version
            with current_directory(join(self.ctx.dist_dir,'lib',arch.arch)):
                for x in ['ssl', 'crypto']:
                    shprint(sh.ln, '-sf',
                            'lib{}.1.0.2.dylib'.format(x),
                            'lib{}.dylib'.format(x))
            build_env['LDFLAGS'] += " -lssl -lcrypto -L{}".format(
                join(self.ctx.dist_dir, 'lib', arch.arch)
            )


        configure = sh.Command(join(self.build_dir, "configure"))
        local_arch = arch.arch
        if arch.arch == "arm64" :
            local_arch = "aarch64"
        shprint(configure,
                #"CC={} -fembed-bitcode".format(build_env["CC"]),
                "CC={}".format(build_env["CC"]),
                "LD={}".format(build_env["LD"]),
                "CFLAGS={}".format(build_env["CFLAGS"]),
                "LDFLAGS={} -undefined dynamic_lookup".format(build_env["LDFLAGS"]),
                "ac_cv_file__dev_ptmx=no",
                "ac_cv_file__dev_ptc=no",
                "--without-pymalloc",
                "--disable-toolbox-glue",
                "--host={}-apple-darwin".format(local_arch),
                "--build=x86_64-apple-darwin16.4.0",
                "--prefix=/python",
                #"--exec_prefix=@executable_path/../Frameworks",  #: Install prefix
                "--enable-ipv6",
                "--enable-shared",  #: Build shared library
                "--with-system-ffi",
                "--without-doc-strings",
                _env=build_env)

        self._patch_pyconfig()
        self.apply_patch("random.patch")
        self.apply_patch("ctypes_duplicate.patch")

        #: Patch the makefile to use the install_name "@rpath/"
        shprint(sh.sed, '-ie',
                "s!-install_name,$(prefix)/lib/libpython$(VERSION).dylib!"
                "-install_name,@rpath/libpython$(VERSION).dylib!",
                "Makefile")


        shprint(sh.make, "-j4",
                "CROSS_COMPILE_TARGET=yes",
                "HOSTPYTHON={}".format(self.ctx.hostpython))
                #"HOSTPGEN={}".format(self.ctx.hostpgen))

        #: Copy libpython to dist/lib/arch folder
        arch_lib_dir = join(self.ctx.dist_dir, 'lib', arch.arch)
        if not exists(arch_lib_dir):
            os.makedirs(arch_lib_dir)
        self.copy_file(
            join(self.get_build_dir(arch.arch),'libpython2.7.dylib'),
            join(arch_lib_dir,'libpython2.7.dylib')
        )


    def install(self):
        arch = list(self.filtered_archs)[0]
        build_env = arch.get_env()
        build_dir = self.get_build_dir(arch.arch)
        build_env["PATH"] = os.environ["PATH"]
        shprint(sh.make,
                "-C", build_dir,
                "install",
                "CROSS_COMPILE_TARGET=yes",
                "HOSTPYTHON={}".format(self.ctx.hostpython),
                "prefix={}".format(join(self.ctx.dist_dir, "root", "python")),
                _env=build_env)
        #self.reduce_python()

    def _patch_pyconfig(self):
        # patch pyconfig to remove some functionnalities
        # (to have uniform build accross all platfors)
        # this was before in a patch itself, but because the different
        # architecture can lead to different pyconfig.h, we would need one patch
        # per arch. Instead, express here the line we don't want / we want.
        pyconfig = join(self.build_dir, "pyconfig.h")
        def _remove_line(lines, pattern):
            for line in lines[:]:
                if pattern in line:
                    lines.remove(line)
        with open(pyconfig) as fd:
            lines = fd.readlines()
        _remove_line(lines, "#define HAVE_BIND_TEXTDOMAIN_CODESET 1")
        _remove_line(lines, "#define HAVE_FINITE 1")
        _remove_line(lines, "#define HAVE_FSEEK64 1")
        _remove_line(lines, "#define HAVE_FTELL64 1")
        _remove_line(lines, "#define HAVE_GAMMA 1")
        _remove_line(lines, "#define HAVE_GETHOSTBYNAME_R 1")
        _remove_line(lines, "#define HAVE_GETHOSTBYNAME_R_6_ARG 1")
        _remove_line(lines, "#define HAVE_GETRESGID 1")
        _remove_line(lines, "#define HAVE_GETRESUID 1")
        _remove_line(lines, "#define HAVE_GETSPENT 1")
        _remove_line(lines, "#define HAVE_GETSPNAM 1")
        _remove_line(lines, "#define HAVE_MREMAP 1")
        _remove_line(lines, "#define HAVE_PLOCK 1")
        _remove_line(lines, "#define HAVE_SEM_TIMEDWAIT 1")
        _remove_line(lines, "#define HAVE_SETRESGID 1")
        _remove_line(lines, "#define HAVE_SETRESUID 1")
        _remove_line(lines, "#define HAVE_TMPNAM_R 1")
        _remove_line(lines, "#define HAVE__GETPTY 1")
        lines.append("#define HAVE_GETHOSTBYNAME 1\n")
        with open(pyconfig, "wb") as fd:
            fd.writelines(lines)

    def reduce_python(self):
        print("Reduce python")
        oldpwd = os.getcwd()
        try:
            print("Remove files unlikely to be used")
            os.chdir(join(self.ctx.dist_dir, "root", "python"))
            sh.rm("-rf", "share")
            sh.rm("-rf", "bin")
            os.chdir(join(self.ctx.dist_dir, "root", "python", "lib"))
            sh.rm("-rf", "pkgconfig")
            if exists('libpython2.7.a'):
                sh.rm("libpython2.7.a")
            os.chdir(join(self.ctx.dist_dir, "root", "python", "lib", "python2.7"))
            sh.find(".", "-iname", "*.pyc", "-exec", "rm", "{}", ";")
            sh.find(".", "-iname", "*.py", "-exec", "rm", "{}", ";")
            #sh.find(".", "-iname", "test*", "-exec", "rm", "-rf", "{}", ";")
            sh.rm("-rf", "wsgiref", "bsddb", "curses", "idlelib", "hotshot")
            sh.rm("-rf", sh.glob("lib*"))

            # now create the zip.
            print("Create a python27.zip")

            sh.rm("config/libpython2.7.a")
            sh.rm("config/python.o")
            sh.rm("config/config.c.in")
            sh.rm("config/makesetup")
            sh.rm("config/install-sh")
            sh.mv("config", "..")
            sh.mv("site-packages", "..")
            sh.zip("-r", "../python27.zip", sh.glob("*"))
            sh.rm("-rf", sh.glob("*"))
            sh.mv("../config", ".")
            sh.mv("../site-packages", ".")
        finally:
            os.chdir(oldpwd)


recipe = PythonRecipe()
