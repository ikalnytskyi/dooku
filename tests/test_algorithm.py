# coding: utf-8
"""
    dooku.tests.test_algorithm
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests Dooku's algorithm stuff.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""

from dooku.algorithm import *  # NOQA

from . import DookuTestCase


class TestStdCpp(DookuTestCase):

    def test_any_of(self):
        """
        The any_of function has to return expected result for all samples
        of test set.
        """
        self.assertTrue(any_of(lambda x: x == 1, [1, 2, 3, 4, 5]))
        self.assertTrue(any_of(lambda x: x == 2, [1, 2, 3, 4, 5]))
        self.assertTrue(any_of(lambda x: x == 5, [1, 2, 3, 4, 5]))

        self.assertFalse(any_of(lambda x: x == 0, [1, 2, 3, 4, 5]))
        self.assertFalse(any_of(lambda x: x == 6, [1, 2, 3, 4, 5]))

    def test_all_of(self):
        """
        The all_of function has to return expected result for all samples
        of test set.
        """
        self.assertTrue(all_of(lambda x: x > 0, [1, 2, 3, 4, 5]))
        self.assertTrue(all_of(lambda x: x < 6, [1, 2, 3, 4, 5]))

        self.assertFalse(all_of(lambda x: x > 1, [1, 2, 3, 4, 5]))
        self.assertFalse(all_of(lambda x: x == 2, [1, 2, 3, 4, 5]))

    def test_none_of(self):
        """
        The none_of function has to return expected result for all samples
        of test set.
        """
        self.assertTrue(none_of(lambda x: x == 7, [1, 2, 3, 4, 5]))

        self.assertFalse(none_of(lambda x: x == 1, [1, 2, 3, 4, 5]))
        self.assertFalse(none_of(lambda x: x == 2, [1, 2, 3, 4, 5]))
        self.assertFalse(none_of(lambda x: x == 5, [1, 2, 3, 4, 5]))

    def test_find_if(self):
        """
        The find_if function has to return expected result for all samples
        of test set.
        """
        self.assertEqual(find_if(lambda x: x == 1, [1, 2, 3, 4, 5]), 1)
        self.assertEqual(find_if(lambda x: x == 2, [1, 2, 3, 4, 5]), 2)
        self.assertEqual(find_if(lambda x: x == 5, [1, 2, 3, 4, 5]), 5)
        self.assertIsNone(find_if(lambda x: x == 0, [1, 2, 3, 4, 5]))

        vector = [{'a': 13}, {'a': 42}]
        result = find_if(lambda x: x['a'] == 42, vector)

        self.assertIsInstance(result, dict)
        self.assertEqual(id(result), id(vector[1]))
