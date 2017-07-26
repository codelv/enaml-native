from os.path import join
from toolchain import CythonRecipe


class MsgPackRecipe(CythonRecipe):
    version = '0.4.7'
    url = 'https://pypi.python.org/packages/source/m/msgpack-python/msgpack-python-{version}.tar.gz'
    depends = ['python']#,'host_setuptools']
    #library = "libmsgpack.a"
    pre_build_ext = True
    support_ssl = False
    pbx_libraries = ["libz", "libpython"]

    def get_recipe_env(self, arch):
        env = super(MsgPackRecipe, self).get_recipe_env(arch)
        env["LDFLAGS"] += " -lpython -lffi -lz"
        env["CC"] += " -I{}".format(
            join(self.ctx.dist_dir, "include", arch.arch, "libffi"),
        )

        if self.support_ssl:
            env['LDFLAGS'] += " -lssl -lcrypto"
            env['CC'] += " -I{}".format(
                join(self.ctx.dist_dir, "include", arch.arch, "openssl"),
            )
        return env

recipe = MsgPackRecipe()
