import re
import sys
import enaml
import inspect
from textwrap import dedent
from os.path import exists, join, abspath


def convert(name):
    # Straight from So
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def make_widgets():
    """ """
    from enamlnative.widgets import api
    widgets = [getattr(api, n) for n in dir(api) if not n.startswith("_")]
    for Widget in widgets:
        example = "No example available."
        try:
            mod = Widget.__module__.split(".")[-1]
            for filename in ['{mod}.enaml',
                             '{mod}s.enaml',
                             '{name}.enaml',
                             '{uname}.enaml',
                             '{uname}s.enaml',
                             '{name}s.enaml']:
                path = join('../examples', filename.format(
                    mod=mod, name=Widget.__name__.lower(),
                    uname=convert(Widget.__name__)))
                if exists(path):
                    example = dedent("""
                    
                    .. literalinclude:: ../{path}
                        :language: python
                    """.strip()).format(path=path)
                else:
                    print("{} not found".format(abspath(path)))
        except:
            pass


        try:
            from enamlnative.android.factories import ANDROID_FACTORIES

            android = dedent("""
            Android Implementation
            ----------------------------

            .. autoclass:: {mod.__module__}.{mod.__name__}
            
            """.strip()).format(mod=ANDROID_FACTORIES[Widget.__name__]())
        except:
            android = "No Android implementation found"

        try:
            from enamlnative.ios.factories import IOS_FACTORIES

            ios = dedent("""
            iOS Implementation
            ----------------------------

            .. autoclass:: {mod.__module__}.{mod.__name__}
            
            """.strip()).format(mod=IOS_FACTORIES[Widget.__name__]())
        except:
            ios = "No iOS implementation found."

        with open('widgets/{}.rst'.format(Widget.__name__.lower()), 'w') as f:
            f.write(dedent("""
            {w.__name__}
            ========================================
            
            {ex}
            
            Declaration
            ----------------------------
                    
            .. autoclass:: {w.__module__}.{w.__name__}
            
            {android}
            {ios}
            """.format(w=Widget, android=android, ios=ios, ex=example)))

    with open('widgets/index.rst', 'w') as f:
        f.write(dedent("""
        Widgets
        ========================================
        
        .. toctree::
           :maxdepth: 2

           {toc}


        """).format(toc='\n   '.join([
            '{N} <{n}>'.format(N=w.__name__, n=w.__name__.lower())
            for w in widgets
        ])))


def make_apis():
    from enamlnative.android import api as android_apis
    #from enamlnative.ios import api as ios_apis

    apis = [
        getattr(android_apis, n) for n in dir(android_apis)
        if not n.startswith("_")
    ]
    # + [
    #     getattr(ios_apis, n) for n in dir(ios_apis)
    #     if not n.startswith("_")
    # ]

    for api in apis:
        platform = api.__module__.split('.')[1]
        with open('apis/{}_{}.rst'.format(
                platform, api.__name__.lower()), 'w') as f:
            f.write(dedent("""
            {platform} {cls.__name__}
            ========================================
            
            .. autoclass:: {cls.__module__}.{cls.__name__}
            
            """.format(cls=api, platform=platform)))

    with open('apis/index.rst', 'w') as f:
        f.write(dedent("""
        APIs
        ========================================
        
        .. toctree::
           :maxdepth: 2

           {toc}


        """).format(toc='\n   '.join([
            '{N} <{p}_{n}>'.format(N=api.__name__,
                                        p=api.__module__.split('.')[1],
                                        n=api.__name__.lower())
            for api in apis
        ])))



def main():
    make_widgets()
    make_apis()


if __name__ == '__main__':
    sys.path.append('../src')
    sys.path.append('../tests')
    with enaml.imports():
        main()
