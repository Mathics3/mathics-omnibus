# -*- coding: utf-8 -*-

"""Python Setuptools for installation of a suite of Mathics3 PyPI packages."""

from setuptools import setup
from __pkginfo__ import (
    EXTRAS_REQUIRE,
    __version__,
    author,
    author_email,
    classifiers,
    install_requires,
    long_description,
    packages,
    scripts,
    short_desc,
    url,
)

setup(
    name="Mathics-omnibus",
    version=__version__,
    author=author,
    author_email=author_email,
    classifiers=classifiers,
    description=short_desc,
    extras_require=EXTRAS_REQUIRE,
    scripts=scripts,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=packages,
    install_requires=install_requires,
    url=url,
)
