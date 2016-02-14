# coding: utf-8
"""
    dooku.tests
    ~~~~~~~~~~~

    Tests Dooku itself.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""

import sys
import unittest


PY2 = sys.version_info[0] == 2


class DookuTestCase(unittest.TestCase):
    """
    The base class for all Dooku's test cases.
    """


if PY2:
    # fix differences in unittest module between Py 2.x and Py 3.x
    DookuTestCase.assertRegex = DookuTestCase.assertRegexpMatches
    DookuTestCase.assertNotRegex = DookuTestCase.assertNotRegexpMatches
    DookuTestCase.assertCountEqual = DookuTestCase.assertItemsEqual
