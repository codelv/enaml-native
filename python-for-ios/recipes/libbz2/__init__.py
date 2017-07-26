# -*- coding: utf-8 -*-
from toolchain import Recipe, shprint
from os.path import join, exists
import os
import sh

class Libbzip2Recipe(Recipe):
    version = '1.0.6'
    url = 'http://www.bzip.org/{version}/bzip2-{version}.tar.gz'

    def build_arch(self, arch):
        build_env = arch.get_env()
        install_dir = join(self.build_dir,'install')

        # Patch sources to use correct compiler
        shprint(sh.sed, '-ie', 's#CC=gcc#CC={}#'.format(build_env['CC']) ,'Makefile')
        # Patch sources to use correct install directory
        #shprint(sh.sed, '-ie', 's#PREFIX=/usr/local#PREFIX={}'.format(install_dir),
        #        'Makefile')

        shprint(sh.make, "clean")
        shprint(sh.make, 'install', 'PREFIX={}'.format('install'),_env=build_env)

    def install(self):
        #: Copy libbz2
        shprint(sh.cp,join(self.build_dir,'install','lib','libbz2.a'),
                      join(self.ctx.dist_dir,'lib'))

        for arch in self.filtered_archs:
            #: Copy headers
            dest = join(self.ctx.dist_dir,'include',arch.arch,'libbz2')
            if not exists(dest):
                os.makedirs(dest)
            shprint(sh.cp,join(self.build_dir,'install','include','bzlib.h'), dest)

recipe = Libbzip2Recipe()
