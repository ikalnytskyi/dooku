# coding: utf-8
"""
    dooku.itertools
    ~~~~~~~~~~~~~~~

    The module implements various iteration algorithms for different purposes.

    :copyright: (c) 2015, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""

from __future__ import absolute_import

try:
    from itertools import zip_longest
except ImportError:  # fallback to Python 2.x
    from itertools import izip_longest as zip_longest


def chunk_by(n, iterable, fillvalue=None):
    """
    Iterate over a given ``iterable`` by ``n`` elements at a time.

        >>> for x, y in chunk_by(2, [1, 2, 3, 4, 5]):
        ... # iteration no 1: x=1, y=2
        ... # iteration no 2: x=3, y=4
        ... # iteration no 3: x=5, y=None

    :param n: (int) a chunk size number
    :param iterable: (iterator) an input iterator
    :param fillvalue: (any) a value to be used to fit chunk size if there
                      not enough values in input iterator
    :returns: (iterator) an output iterator that iterates over the input
              one by chunks of size ``n``
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
