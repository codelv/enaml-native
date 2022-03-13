import re
import sys
import enaml
from os.path import exists, join


def convert(name):
    # Straight from So
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


ANDROID_WIDGET_TEMPLATE = """
Android Implementation
----------------------------

.. autoclass:: {mod.__module__}.{mod.__name__}

"""

IOS_WIDGET_TEMPLATE = """
iOS Implementation
----------------------------

.. autoclass:: {mod.__module__}.{mod.__name__}

"""

EXAMPLE_TEMPLATE = """
Example
----------------------------

.. literalinclude:: ../{path}
    :language: enaml
"""

IMAGE_TEMPLATE = """
Screenshot
----------------------------

.. image:: ../{path}
"""

DECLARATION_TEMPLATE = """
{cls}
========================================

{image}

{example}

Declaration
----------------------------

.. autoclass:: {mod}.{cls}

{android}

{ios}
"""

WIDGET_INDEX_TEMPLATE = """
Widgets
========================================

.. toctree::
    :maxdepth: 2

    {toc}

"""

API_TEMPLATE = """
{platform} {api.__name__}
========================================

{example}

.. autoclass:: {api.__module__}.{api.__name__}

"""

API_INDEX_TEMPLATE = """
APIs
========================================

.. toctree::
    :maxdepth: 2

    {toc}

"""


def find_example(*example_names: str) -> str:
    for filename in example_names:
        path = join("../examples", filename)
        if exists(path):
            return EXAMPLE_TEMPLATE.format(path=path)
    return ""


def find_image(*image_names: str) -> str:
    for name in image_names:
        path = f"images/{name}"
        if exists(path):
            return IMAGE_TEMPLATE.format(path=path)
    return ""


def make_widgets():
    """ """
    from enamlnative.widgets import api
    from enamlnative.android.factories import ANDROID_FACTORIES

    # from enamlnative.ios.factories import IOS_FACTORIES
    IOS_FACTORIES = {}

    widgets = [getattr(api, n) for n in dir(api) if not n.startswith("_")]
    toc = []
    for Widget in widgets:
        example = "No example available."
        pkg = Widget.__module__.split(".")[-1]
        cls = Widget.__name__
        fname = cls.lower()
        uname = convert(cls)
        toc.append(f"{cls} <{fname}>")
        example = find_example(
            f"{pkg}.enaml",
            f"{pkg}s.enaml",
            f"{fname}.enaml",
            f"{fname}s.enaml",
            f"{uname}.enaml",
            f"{uname}s.enaml",
        )

        image = find_image(
            f"android_{fname}.gif",
            f"android_{uname}.gif",
            f"android_{uname}.gif",
        )

        if cls in ANDROID_FACTORIES:
            mod = ANDROID_FACTORIES[cls]()
            android = ANDROID_WIDGET_TEMPLATE.format(mod=mod)
        else:
            android = "No Android implementation found"

        if cls in IOS_FACTORIES:
            mod = IOS_FACTORIES[cls]()
            ios = IOS_WIDGET_TEMPLATE.format(mod=mod)
        else:
            ios = "No iOS implementation found."

        with open(f"widgets/{fname}.rst", "w") as f:
            mod = Widget.__module__
            tmpl = DECLARATION_TEMPLATE.format(
                mod=mod,
                cls=cls,
                example=example,
                android=android,
                ios=ios,
                image=image,
            )
            f.write(tmpl)

    with open("widgets/index.rst", "w") as f:
        f.write(WIDGET_INDEX_TEMPLATE.format(toc="\n    ".join(toc)))


def make_apis():
    from enamlnative.android import api as android_apis

    # from enamlnative.ios import api as ios_apis

    apis = [
        getattr(android_apis, n) for n in dir(android_apis) if not n.startswith("_")
    ]
    # + [
    #     getattr(ios_apis, n) for n in dir(ios_apis)
    #     if not n.startswith("_")
    # ]

    toc = []
    for api in apis:
        platform = api.__module__.split(".")[1]
        name = api.__name__
        fname = name.lower()
        example = find_example(
            f"{fname}.enaml",
        )
        toc.append(f"{name} <{platform}_{fname}>")
        with open(f"apis/{platform}_{fname}.rst", "w") as f:
            f.write(
                API_TEMPLATE.format(platform=platform.title(), api=api, example=example)
            )

    with open("apis/index.rst", "w") as f:
        f.write(API_INDEX_TEMPLATE.format(toc="\n    ".join(toc)))


def main():
    make_widgets()
    make_apis()


if __name__ == "__main__":
    sys.path.append("../src")
    sys.path.append("../tests")
    with enaml.imports():
        main()
