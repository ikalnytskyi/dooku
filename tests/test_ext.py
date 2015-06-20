# coding: utf-8
"""
    dooku.tests.test_ext
    ~~~~~~~~~~~~~~~~~~~~

    Tests Dooku's ext-related stuff.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""

import mock

from dooku.ext import ExtensionManager

from . import DookuTestCase


class TestExtensionManager(DookuTestCase):

    @mock.patch('dooku.ext.pkg_resources.iter_entry_points', autospec=True)
    def setUp(self, iter_ep):
        """
        Prepare extensions for each testcase.
        """
        # Holy crap! The mock library can't work with "name" attribute,
        # so we need this tricks to workaround this.
        entry_points = [mock.Mock(), mock.Mock(), mock.Mock()]
        type(entry_points[0]).name = mock.PropertyMock(return_value='one')
        type(entry_points[1]).name = mock.PropertyMock(return_value='two')
        type(entry_points[2]).name = mock.PropertyMock(return_value='two')

        iter_ep.return_value = entry_points

        self.ext_manager = ExtensionManager('dooku.test')
        self.entry_points = entry_points

    def test_get(self):
        """
        The get method has to behave exactly like a dict's one.
        """
        self.assertEqual(
            self.ext_manager.get('one'), self.entry_points[0].load())
        self.assertEqual(
            self.ext_manager.get('two'), self.entry_points[1].load())
        self.assertNotEqual(
            self.ext_manager.get('two'), self.entry_points[2].load())

        self.assertIsNone(self.ext_manager.get('three'))
        self.assertEqual(self.ext_manager.get('three', 42), 42)

    def test_getall(self):
        """
        The getall method has to return a list of extensions for a given
        name. In case there're no extensions - the empty list has to be
        returned.
        """
        self.assertEqual(
            self.ext_manager.getall('one'), [self.entry_points[0].load()])
        self.assertEqual(
            self.ext_manager.getall('two'),
            [self.entry_points[1].load(), self.entry_points[2].load()])

        self.assertEqual(self.ext_manager.getall('three'), [])

    def test_getall_returns_copy(self):
        """
        The getall method has to return a list copy so its changes has
        no affect internal state.
        """
        res = self.ext_manager.getall('two')
        res.append(42)

        self.assertNotEqual(self.ext_manager.getall('two'), res)

    def test_getitem(self):
        """
        The __getitem__ has to behave exactly like a dict's one.
        """
        self.assertEqual(
            self.ext_manager['one'], self.entry_points[0].load())
        self.assertEqual(
            self.ext_manager['two'], self.entry_points[1].load())
        self.assertNotEqual(
            self.ext_manager['two'], self.entry_points[2].load())

        self.assertRaises(KeyError, lambda: self.ext_manager['three'])

    def test_names(self):
        """
        The names method has to return a set of extension names.
        """
        self.assertEqual(self.ext_manager.names(), set(['one', 'two']))

    def test_contains(self):
        """
        The __contains__ has to behave exactly like a dict's one.
        """
        self.assertIn('one', self.ext_manager)
        self.assertIn('two', self.ext_manager)
        self.assertNotIn('three', self.ext_manager)

    def test_iter(self):
        """
        The __iter__ has to return an iterator over all extensions where the
        iteration element is (name, extension).
        """
        self.assertEqual(set(i for i in self.ext_manager), set([
            ('one', self.entry_points[0].load()),
            ('two', self.entry_points[1].load()),
            ('two', self.entry_points[2].load()), ]))

    @mock.patch('dooku.ext.pkg_resources.iter_entry_points', autospec=True)
    def test_constructor_w_names(self, iter_ep):
        """
        If the names was passed to the constructor, only those extensions
        has to be loaded.
        """
        iter_ep.return_value = self.entry_points
        self.ext_manager = ExtensionManager('dooku.test', ['two'])

        self.assertEqual(set(i for i in self.ext_manager), set([
            ('two', self.entry_points[1].load()),
            ('two', self.entry_points[2].load()), ]))

    @mock.patch('dooku.ext.pkg_resources.iter_entry_points', autospec=True)
    def test_silent_false(self, iter_ep):
        """
        The constructor has to raise exceptions if silent is False.
        """
        self.entry_points[1].load.side_effect = ValueError('error')
        iter_ep.return_value = self.entry_points

        self.assertRaises(
            ValueError, lambda: ExtensionManager('dooku.test', silent=False))

    @mock.patch('dooku.ext.pkg_resources.iter_entry_points', autospec=True)
    def test_silent_true(self, iter_ep):
        """
        The constructor don't has to raise exceptions if silent is True.
        """
        self.entry_points[0].load.side_effect = ValueError('error')
        iter_ep.return_value = self.entry_points

        self.ext_manager = ExtensionManager('dooku.test', silent=True)

        self.assertEqual(set(i for i in self.ext_manager), set([
            ('two', self.entry_points[1].load()),
            ('two', self.entry_points[2].load()), ]))
        self.assertEqual(self.ext_manager.names(), set(['two']))
