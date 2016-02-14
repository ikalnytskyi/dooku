# coding: utf-8
"""
    dooku.tests.test_ext
    ~~~~~~~~~~~~~~~~~~~~

    Tests Dooku's ext-related stuff.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""

import os
import pkg_resources
import mock

from dooku.ext import ExtensionManager

from . import DookuTestCase


class One(object):
    pass


class Two(object):
    pass


class NewTwo(object):
    pass


class TestExtensionManager(DookuTestCase):

    # namespace to be used to export extensions via entry points
    namespace = 'dooku.tests'

    def _get_entry_points(self, names, load_fn=None):
        """
        Prepares and returns named mocks with optional .load function.
        """
        rv = []

        for name in names:
            rv.append(mock.Mock())
            if load_fn is not None:
                type(rv[-1]).load = load_fn
            # Holy crap! The mock library can't work with "name"
            # attribute, so we need this trick as workaround.
            type(rv[-1]).name = name

        return rv

    def setUp(self):
        # create a fake distribution that will be used to export some
        # extensions via entry points
        fake_dist_1 = pkg_resources.Distribution(
            project_name='fake_project_1',
            version='0.1',
            location=os.path.dirname(__file__))
        fake_dist_2 = pkg_resources.Distribution(
            project_name='fake_project_2',
            version='0.1',
            location=os.path.dirname(__file__))

        # unfortunately, there's no public api for registring new entry
        # points so no choice but use internal one
        fake_dist_1._ep_map = {
            self.namespace: {
                'one': pkg_resources.EntryPoint.parse(
                    'one = %s:One' % __name__, dist=fake_dist_1),
                'two': pkg_resources.EntryPoint.parse(
                    'two = %s:Two' % __name__, dist=fake_dist_1),
            }}
        fake_dist_2._ep_map = {
            self.namespace: {
                'two': pkg_resources.EntryPoint.parse(
                    'two = %s:NewTwo' % __name__, dist=fake_dist_2),
            }}

        # register fake distributions within pkg_resources
        pkg_resources.working_set.add(fake_dist_1)
        pkg_resources.working_set.add(fake_dist_2)

        self.ext_manager = ExtensionManager(self.namespace)

    def test_get(self):
        """
        The get method has to behave exactly like a dict's one.
        """
        self.assertEqual(self.ext_manager.get('one'), One)
        self.assertEqual(self.ext_manager.get('two'), Two)
        self.assertNotEqual(self.ext_manager.get('two'), NewTwo)

        self.assertIsNone(self.ext_manager.get('three'))
        self.assertEqual(self.ext_manager.get('three', 42), 42)

    def test_getall(self):
        """
        The getall method has to return a list of extensions for a given
        name. In case there're no extensions - the empty list has to be
        returned.
        """
        self.assertEqual(self.ext_manager.getall('one'), [One])
        self.assertEqual(self.ext_manager.getall('two'), [Two, NewTwo])

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
        self.assertEqual(self.ext_manager['one'], One)
        self.assertEqual(self.ext_manager['two'], Two)
        self.assertNotEqual(self.ext_manager['two'], NewTwo)

        self.assertRaises(KeyError, lambda: self.ext_manager['three'])

    def test_names(self):
        """
        The names method has to return a set of extension names.
        """
        self.assertCountEqual(self.ext_manager.names(), ['one', 'two'])

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
        self.assertCountEqual([i for i in self.ext_manager], [
            ('one', One),
            ('two', Two),
            ('two', NewTwo), ])

    def test_constructor_w_names(self):
        """
        If the names was passed to the constructor, only those extensions
        has to be loaded.
        """
        self.ext_manager = ExtensionManager(self.namespace, ['two'])

        self.assertCountEqual([i for i in self.ext_manager], [
            ('two', Two),
            ('two', NewTwo), ])

    @mock.patch('dooku.ext.pkg_resources.iter_entry_points', autospec=True)
    def test_keep_load_order(self, iter_ep):
        """
        The constructor has to load extensions is passed order.
        """
        order = []

        def load_trap(self, *args):
            order.append(self.name)

        entry_points = self._get_entry_points(['a', 'b', 'c'], load_trap)
        iter_ep.side_effect = [
            [entry_points[2]],
            [entry_points[0]],
            [entry_points[1]], ]

        self.ext_manager = ExtensionManager(self.namespace, ['c', 'a', 'b'])
        self.assertEqual(order, ['c', 'a', 'b'])

    @mock.patch('dooku.ext.pkg_resources.iter_entry_points', autospec=True)
    def test_silent_false(self, iter_ep):
        """
        The constructor has to raise exceptions if silent is False.
        """
        entry_points = self._get_entry_points(['a', 'b', 'c'])
        entry_points[1].load.side_effect = ValueError('error')

        iter_ep.return_value = entry_points

        self.assertRaises(
            ValueError,
            lambda: ExtensionManager(self.namespace, silent=False))

    @mock.patch('dooku.ext.pkg_resources.iter_entry_points', autospec=True)
    def test_silent_true(self, iter_ep):
        """
        The constructor don't has to raise exceptions if silent is True.
        """
        entry_points = self._get_entry_points(['a', 'b', 'c'])
        entry_points[0].load.side_effect = ValueError('error')

        iter_ep.return_value = entry_points

        self.ext_manager = ExtensionManager(self.namespace, silent=True)

        self.assertEqual(set(i for i in self.ext_manager), set([
            ('b', entry_points[1].load()),
            ('c', entry_points[2].load()), ]))
        self.assertCountEqual(self.ext_manager.names(), ['b', 'c'])
