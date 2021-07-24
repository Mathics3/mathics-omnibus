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

# Setup in EXTRAS_REQUIRE various install options:
#  mathicsscript_full, etc.
mathicsscript_full = {"PyYAML", "PyQT5", "cairosvg", "ujson",}
django_full = {"ujson",}
pymathics_full = {"pymathics-natlang >= 2.2.0", "pymathics-graph >= 2.3.0",}
full = mathicsscript_full | django_full | pymathics_full

EXTRAS_REQUIRE = {}
for field in "mathicsscript_full pymathics_full full".split():
    EXTRAS_REQUIRE[field] = locals()[field]

PYTHON_VERSION = sys.version_info[0] + (sys.version_info[1] / 10.0)
IS_PYPY = "__pypy__" in sys.builtin_module_names

install_requires = [
    "Mathics3 >= 3.1.0",
    "mathicsscript >= 3.2.1",
    "Mathics-Django >= 3.1.0",
    "pymathics-natlang >= 2.2.0",
    "pymathics-graph >= 2.3.0",
]

py_modules = None
short_desc = "A Collection Mathics components to provide the full Mathics experience"
url = "http://github.com/Mathics3/mathics-omnibus"

classifiers = [
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]
