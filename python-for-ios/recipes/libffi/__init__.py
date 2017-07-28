from toolchain import Recipe, FrameworkLibrary, shprint
import sh
import os
from os.path import join,exists


class LibffiFramework(FrameworkLibrary):
    #: TODO should be ARCH independent
    libraries = ['lib/{arch}/libffi.dylib']


class LibffiRecipe(Recipe):
    version = "3.2.1"
    url = "ftp://sourceware.org/pub/libffi/libffi-{version}.tar.gz"
    #library = "build/Release-{arch.sdk}/ffi.dynlib"
    include_per_arch = True
    include_dir = "build_{arch.sdk}-{arch.arch}/include"
    framework = LibffiFramework()

    def prebuild_arch(self, arch):
        if self.has_marker("patched"):
            return
        # necessary as it doesn't compile with XCode 6.0. If we use 5.1.1, the
        # compiler for i386 is not working.
        shprint(sh.sed,
                "-i.bak",
                "s/-miphoneos-version-min=5.1.1/-miphoneos-version-min=8.0/g",
                "generate-darwin-source-and-headers.py")
        self.apply_patch("fix-win32-unreferenced-symbol.patch")
        #: Make it a dylib and set min version to 8.0
        self.copy_file('project.pbxproj.dylib',
                       join(self.get_build_dir(arch.arch),'libffi.xcodeproj','project.pbxproj'))
        self.set_marker("patched")

    def build_arch(self, arch):
        shprint(sh.xcodebuild,
                "ONLY_ACTIVE_ARCH=NO",
                "ARCHS={}".format(arch.arch),
                # "ENABLE_BITCODE=YES",
                "-sdk", arch.sdk,
                "-project", "libffi.xcodeproj",
                "-target", "libffi-iOS",
                "-configuration", "Release")

        #: Copy to dist/lib/arch folder
        target = 'iphonesimulator' if arch.arch in ['i386','x86_64'] else 'iphoneos'
        arch_lib_dir = join(self.ctx.dist_dir,'lib',arch.arch)
        if not exists(arch_lib_dir):
            os.makedirs(arch_lib_dir)
        self.copy_file(
            join(self.get_build_dir(arch.arch),'build/Release-{}/libffi.dylib'.format(target)),
            join(arch_lib_dir,'libffi.dylib')
        )




recipe = LibffiRecipe()

