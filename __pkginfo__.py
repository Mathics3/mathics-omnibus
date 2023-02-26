import sys

author = "Rocky Bernstein"
author_email = "rb@dustyfeet.com"
scripts = [
    "script/dmathics",
    "script/dmathicsdoc",
    "script/dmathicsdoccopy",
    "script/dmathicsserver",
    "script/dmathicsscript",
    "script/term-background.sh",
]

import os.path as osp


def get_srcdir():
    filename = osp.normcase(osp.dirname(osp.abspath(__file__)))
    return osp.realpath(filename)


def read(*rnames):
    return open(osp.join(get_srcdir(), *rnames)).read()


# Get/set __version__ and long_description from files.
exec(read("mathics_omnibus/version.py"))
long_description = read("README.rst") + "\n"

#  mathicsscript_full, etc.
django_full = {"ujson",}

# All mathics-core enhancement options
mathics_core_full = {"psutil", "scikit-image", "lxml", "wordcloud", "cython",}

# All mathicsscript enhancement options
mathicsscript_full = {"PyYAML", "PyQT5", "cairosvg", "ujson",}

# All Mathics3 Modules
mathics3_modules_full = {"pymathics-natlang >= 6.0.0", "pymathics-graph >= 6.0.0",}

# options you can give in ... of:
#    pip install mathics_omnibus[...]

EXTRAS_REQUIRE = {
    "core-full": mathics_core_full,
    "django_full": django_full,
    "mathicsscript-full": mathicsscript_full,
    "Mathics3-Modules-full": mathics3_modules_full,
    "full": mathics_core_full | django_full | mathicsscript_full | mathics3_modules_full
    }

IS_PYPY = "__pypy__" in sys.builtin_module_names

install_requires = [
    "Mathics3 >=6.0.0",
    "mathicsscript >= 6.0.0",
    "Mathics-Django >= 6.0.0",
    # Mathics3 6.0.0 accidentally omitted Pillow > 9.2
    "pillow >= 9.2.0",
]

packages=["mathics_omnibus", "script"]
py_modules = None
short_desc = "A Collection Mathics3 components to provide the full Mathics3 experience"
url = "http://github.com/Mathics3/mathics-omnibus"

classifiers = [
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]
