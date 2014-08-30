# coding: utf-8
"""
    dooku.tests
    ~~~~~~~~~~~

    Tests Dooku itself.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
import unittest

try:
    from unittest import mock  # NOQA
except:
    import mock  # NOQA


class DookuTestCase(unittest.TestCase):
    """
    The base class for all Dooku's test cases.
    """
