import sys
import os.path as osp

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
django_full = {"ujson",}
mathics_core_full = {"psutil", "scikit-image", "lxml", "wordcloud", "cython",}
mathicsscript_full = {"PyYAML", "PyQT5", "cairosvg", "ujson",}
pymathics_full = {"pymathics-natlang >= 6.2.0", "pymathics-graph >= 6.2.0",}
full = mathicsscript_full | django_full | pymathics_full

EXTRAS_REQUIRE = {}
for field in "mathics_core_full mathicsscript_full pymathics_full full".split():
    EXTRAS_REQUIRE[field] = locals()[field]

IS_PYPY = "__pypy__" in sys.builtin_module_names

install_requires = [
    "Mathics3 >= 7.0.0.dev0,<7.1.0",
    "mathicsscript >= 6.2.0",
    "Mathics-Django >= 6.2.0",
    "pymathics-natlang >= 6.2.0",
    "pymathics-graph >= 6.2.0",
]

packages=["mathics_omnibus", "script"]
py_modules = None
short_desc = "A Collection Mathics components to provide the full Mathics experience"
url = "http://github.com/Mathics3/mathics-omnibus"

classifiers = [
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
