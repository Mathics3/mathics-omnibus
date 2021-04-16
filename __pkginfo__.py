import sys

author = "Rocky Bernstein"
author_email = "rb@dustyfeet.com"
scripts = [
    "script/dmathics",
    "script/dmathicsserver",
    "script/dmathicsscript",
]

import os.path as osp


def get_srcdir():
    filename = osp.normcase(osp.dirname(osp.abspath(__file__)))
    return osp.realpath(filename)


def read(*rnames):
    return open(osp.join(get_srcdir(), *rnames)).read()


# Get/set __version__VERSION and long_description from files
exec(read("mathics_omnibus/version.py"))

PYTHON_VERSION = sys.version_info[0] + (sys.version_info[1] / 10.0)
IS_PYPY = "__pypy__" in sys.builtin_module_names

install_requires = [
    "Mathics3 >= 2.1.0",
    "mathicsscript >= 2.0.1",
    "Mathics-Django >= 2.2.0",
    "pymathics-natlang",
    "pymathics-graph",
]

py_modules = None
short_desc = "A Collection Mathics components to provide the ful Mathics experience"
url = "http://github.com/Mathics3/mathics-omnibus"

classifiers = [
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

long_description = read("README.rst") + "\n"
