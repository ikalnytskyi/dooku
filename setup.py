#!/usr/bin/env python
# coding: utf-8

import os

from io import open
from setuptools import setup, find_packages

from dooku import __version__ as dooku_version
from dooku import __license__ as dooku_license


here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='dooku',
    version=dooku_version,

    description='Daily set of libraries for the Force-sensitives. =/',
    long_description=long_description,
    license=dooku_license,
    url='https://github.com/ikalnitsky/dooku',

    author='Igor Kalnitsky',
    author_email='igor@kalnitsky.org',

    packages=find_packages(exclude=['docs', 'tests*']),
    test_suite='tests',
    platforms=['any'],
    zip_safe=False,

    tests_require=['mock >= 1.1.0', 'PyYAML'],

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
