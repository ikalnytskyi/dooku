# coding: utf-8
"""
    dooku.tests.test_itertools
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests Dooku's itertools stuff.

    :copyright: (c) 2015, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""

from dooku import itertools

from . import DookuTestCase


class TestChunkBy(DookuTestCase):

    def test_default_case(self):
        chunks = itertools.chunk_by(3, [0, 1, 2, 3, 4, 5, 6, 7, 8])

        self.assertEqual(list(chunks), [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
        ])

    def test_not_enough_items(self):
        chunks = itertools.chunk_by(3, [0, 1, 2, 3, 4, 5, 6, 7])

        self.assertEqual(list(chunks), [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, None),
        ])

    def test_fillvalue(self):
        chunks = itertools.chunk_by(3, [0, 1, 2, 3, 4, 5, 6, 7], '42')

        self.assertEqual(list(chunks), [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, '42'),
        ])

    def test_chunk_is_one(self):
        chunks = itertools.chunk_by(1, [0, 1, 2, 3, 4, 5, 6, 7])

        self.assertEqual(
            list(chunks),
            [(0, ), (1, ), (2, ), (3, ), (4, ), (5, ), (6, ), (7, )])
