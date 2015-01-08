#!/usr/bin/env python
# coding: utf-8
"""
Dooku
-----

Dooku is a set of libraries for the Python programming language that
provides various useful stuff that you might need in everyday usage.

The idea is to provide a set of libraries and useful functions, just
like Boost does in C++ world.

Dooku is a good not only as a set of libraries, it also may be used
as a some kind of incubator where various developers can test and
evolve their projects. So please don't hesitate to propose your
library to be a part of Dooku.

Links
`````

* `documentation <https://dooku.readthedocs.org/>`_
* `source code <https://github.com/ikalnitsky/dooku>`_
"""
from setuptools import setup, find_packages

from dooku import __version__ as dooku_version
from dooku import __license__ as dooku_license


setup(
    name='dooku',
    version=dooku_version,
    license=dooku_license,
    description='a set of libraries for everyday',
    long_description=__doc__,
    url='https://github.com/ikalnitsky/dooku',
    platforms=['any'],

    author='Igor Kalnitsky',
    author_email='igor@kalnitsky.org',

    packages=find_packages(exclude=('tests', )),
    test_suite='tests',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
