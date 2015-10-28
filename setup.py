#!/usr/bin/env python
# coding: utf-8

from io import open
from setuptools import setup, find_packages

from dooku import __version__ as dooku_version
from dooku import __license__ as dooku_license


with open('README.rst', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='dooku',
    version=dooku_version,
    license=dooku_license,
    description='Daily set of libraries for the Force-sensitives. =/',
    long_description=LONG_DESCRIPTION,
    author='Igor Kalnitsky',
    author_email='igor@kalnitsky.org',
    url='https://github.com/ikalnitsky/dooku',

    packages=find_packages(exclude=['tests']),
    test_suite='tests',
    platforms=['any'],
    zip_safe=False,

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)
