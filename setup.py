#!/usr/bin/env python
# coding: utf-8
"""
$ dooku_

  Dooku is a set of libraries for the Python programming language that
  provides various useful stuff that you might need in everyday usage.

  The idea is to provide a set of libraries and useful functions, just
  like Boost does in C++ world.

  Documentation:  http://dooku.readthedocs.org/
  Source code:    https://github.com/ikalnitsky/dooku
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

    packages=find_packages(exclude=('tests')),
    test_suite='tests',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
