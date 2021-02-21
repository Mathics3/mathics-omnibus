#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Python Setuptools for Mathics via docker."""

from setuptools import setup
from __pkginfo__ import (
    __version__,
    author,
    author_email,
    classifiers,
    install_requires,
    long_description,
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
    scripts=scripts,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=install_requires,
    url=url,
)
