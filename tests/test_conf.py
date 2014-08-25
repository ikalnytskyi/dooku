# coding: utf-8
"""
    dooku.tests.test_conf
    ~~~~~~~~~~~~~~~~~~~~~

    Tests Dooku's conf-related stuff.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
from dooku.conf import Conf

from . import DookuTestCase


class TestConf(DookuTestCase):

    def setUp(self):
        """
        Prepare source config for each testcase.
        """
        self.source_conf = {
            'root': {
                'one': {
                    'a': 1,
                    'b': 2,
                },

                'two': {
                    'c': 3,
                }
            }
        }

    def test_constructor_saves_dict(self):
        """
        The constructor has to save an input dict without changes.
        """
        conf = Conf(self.source_conf)
        self.assertEqual(self.source_conf, conf._data)

    def test_constructor_makes_copy(self):
        """
        The constructor has to make a copy of input dictionaries.
        """
        conf = Conf(self.source_conf)
        conf['non-root'] = 13
        conf['root.one.c'] = 42

        self.assertNotIn('non-root', self.source_conf)
        self.assertNotIn('c', self.source_conf['root']['one'])

    def test_constructor_custom_separator(self):
        """
        The constructor has to use a given separator, not a dot.
        """
        conf = Conf(self.source_conf, separator='#')

        self.assertEqual(conf['root#one#a'], conf['root']['one']['a'])
        self.assertEqual(conf.get('root#one#a'), conf['root']['one']['a'])

        self.assertEqual(conf['root#two#c'], conf['root']['two']['c'])
        self.assertEqual(conf.get('root#two#c'), conf['root']['two']['c'])

    def test_change_subconf(self):
        """
        Tests that changing some option via sub-conf instance leads
        to change this option in the main conf instance.
        """
        conf = Conf(self.source_conf)

        one_conf = conf['root.one']
        one_conf['a'] = 42

        self.assertEqual(one_conf['a'], 42)
        self.assertEqual(conf['root.one.a'], 42)

    def test_update(self):
        """
        The update has to be capable to make recursive update.
        """
        conf = Conf(self.source_conf)

        conf.update({
            'root': {
                'one': {'a': 42, 'z': 13},
                'three': [],
            },
            'non-root': [1, 2],
        })

        result = {
            'root': {
                'one': {'a': 42, 'b': 2, 'z': 13},
                'two': {'c': 3},
                'three': [],
            },
            'non-root': [1, 2],
        }

        self.assertEqual(conf._data, result)

    def test_update_with_conf(self):
        """
        The update has to be capable to make recursive update.
        """
        conf = Conf(self.source_conf)

        conf.update({
            'root': Conf({
                'one': {'a': 42, 'z': 13},
                'three': [],
            }),
            'non-root': [1, 2],
        })

        result = {
            'root': Conf({
                'one': {'a': 42, 'b': 2, 'z': 13},
                'two': {'c': 3},
                'three': [],
            }),
            'non-root': [1, 2],
        }

        self.assertEqual(conf._data, result)

    def test_getitem_simple_key(self):
        """
        The __getitem__ has to behave exactly like a dict's one.
        """
        conf = Conf(self.source_conf)

        self.assertEqual(
            conf['root'], self.source_conf['root'])
        self.assertEqual(
            conf['root']['one'], self.source_conf['root']['one'])
        self.assertEqual(
            conf['root']['one']['a'], self.source_conf['root']['one']['a'])
        self.assertEqual(
            conf['root']['one']['b'], self.source_conf['root']['one']['b'])
        self.assertEqual(
            conf['root']['two'], self.source_conf['root']['two'])
        self.assertEqual(
            conf['root']['two']['c'], self.source_conf['root']['two']['c'])

        self.assertIsInstance(conf['root'], Conf)
        self.assertIsInstance(conf['root']['one'], Conf)
        self.assertIsInstance(conf['root']['one']['a'], int)
        self.assertIsInstance(conf['root']['one']['b'], int)
        self.assertIsInstance(conf['root']['two'], Conf)
        self.assertIsInstance(conf['root']['two']['c'], int)

        self.assertRaises(KeyError, lambda: conf['non-root'])

    def test_getitem_compound_key(self):
        """
        The __getitem__ has to handle compund keys correctly.
        """
        conf = Conf(self.source_conf)

        self.assertEqual(
            conf['root.one'], self.source_conf['root']['one'])
        self.assertEqual(
            conf['root.one.a'], self.source_conf['root']['one']['a'])
        self.assertEqual(
            conf['root.one.b'], self.source_conf['root']['one']['b'])
        self.assertEqual(
            conf['root.two'], self.source_conf['root']['two'])
        self.assertEqual(
            conf['root.two.c'], self.source_conf['root']['two']['c'])

        self.assertIsInstance(conf['root.one'], Conf)
        self.assertIsInstance(conf['root.one.a'], int)
        self.assertIsInstance(conf['root.one.b'], int)
        self.assertIsInstance(conf['root.two'], Conf)
        self.assertIsInstance(conf['root.two.c'], int)

        self.assertRaises(KeyError, lambda: conf['root.three'])

    def test_get_simple_key(self):
        """
        The get method has to behave exactly like a dict's one.
        """
        conf = Conf(self.source_conf)

        self.assertEqual(
            conf.get('root'), self.source_conf['root'])
        self.assertEqual(
            conf.get('root').get('one'), self.source_conf['root']['one'])
        self.assertEqual(
            conf.get('non-root', 'default'), 'default')

        try:
            conf.get('non-root')
        except KeyError:
            self.fail('The `get` method MUST BE safe!')

    def test_get_compound_key(self):
        """
        The __getitem__ has to handle compund keys correctly.
        """
        conf = Conf(self.source_conf)

        self.assertEqual(
            conf.get('root.one'), self.source_conf['root']['one'])
        self.assertEqual(
            conf.get('root.one.a'), self.source_conf['root']['one']['a'])
        self.assertEqual(
            conf.get('root.one.b'), self.source_conf['root']['one']['b'])
        self.assertEqual(
            conf.get('root.two'), self.source_conf['root']['two'])
        self.assertEqual(
            conf.get('root.two.c'), self.source_conf['root']['two']['c'])
        self.assertEqual(
            conf.get('root.three', 'default'), 'default')

        try:
            conf.get('root.three')
        except KeyError:
            self.fail('The `get` method MUST BE safe!')

    def test_setitem_simple_key(self):
        """
        The __setitem__ has to behave exactly like a dict's one.
        """
        conf = Conf(self.source_conf)
        conf['non-root'] = 42
        conf['root']['three'] = 13

        self.assertEqual(conf._data['non-root'], 42)
        self.assertEqual(conf._data['root']['three'], 13)

    def test_setitem_compound_key(self):
        """
        The __setitem__ has to handle compund keys correctly.
        """
        conf = Conf(self.source_conf)

        try:
            conf['root.three'] = 42
            conf['root.four.d'] = 13
        except:
            self.fail('The __setitem__ MUST NOT fail!')

        self.assertEqual(conf._data['root']['three'], 42)
        self.assertEqual(conf._data['root']['four']['d'], 13)

    def test_delitem_simple_key(self):
        """
        The __detitem__ has to behave exactly like a dict's one.
        """
        conf = Conf(self.source_conf)

        del conf['root']['two']
        self.assertIn('root', conf)
        self.assertNotIn('two', conf['root'])

        del conf['root']
        self.assertNotIn('root', conf)

        def delconf(conf, key):
            del conf[key]
        self.assertRaises(KeyError, delconf, conf, 'non-root')

    def test_delitem_compound_key(self):
        """
        The __detitem__ has to handle compund keys correctly.
        """
        conf = Conf(self.source_conf)
        del conf['root.two']

        self.assertIn('root', conf)
        self.assertNotIn('root.two', conf)

        def delconf(conf, key):
            del conf[key]
        self.assertRaises(KeyError, delconf, conf, 'root.three')

    def test_contains_simple_key(self):
        """
        The __contains__ has to behave exactly like a dict's one.
        """
        conf = Conf(self.source_conf)

        self.assertIn('root', conf)
        self.assertIn('one', conf['root'])
        self.assertIn('two', conf['root'])

        self.assertNotIn('one', conf)
        self.assertNotIn('two', conf)

    def test_contains_compound_key(self):
        """
        The __contains__ has to handle compound keys correctly.
        """
        conf = Conf(self.source_conf)

        self.assertIn('root.one', conf)
        self.assertIn('root.two', conf)
        self.assertIn('root.one.a', conf)
        self.assertIn('root.one.b', conf)
        self.assertIn('root.two.c', conf)

        self.assertNotIn('root.one.c', conf)
        self.assertNotIn('root.three', conf)

    def test_iter(self):
        """
        The __iter__ has to behave exactly like a dict's one.
        """
        conf = Conf(self.source_conf)

        self.assertSequenceEqual(conf, self.source_conf)

    def test_len(self):
        """
        The __len__ has to behave exactly like a dict's one.
        """
        conf = Conf(self.source_conf)

        self.assertEqual(len(conf), len(self.source_conf))

    def test_str(self):
        """
        The __str__ has to behave exactly like a dict's one.
        """
        conf = Conf(self.source_conf)

        self.assertEqual(str(conf), str(conf._data))

    def test_format(self):
        """
        The __format__ has to behave exactly like a dict's one.
        """
        conf = Conf(self.source_conf)

        self.assertEqual("{0}".format(conf), str(conf))

    def test_eq_operator(self):
        """
        The __eq__ has to compare an instance with Confs and dicts.
        """
        conf_a = Conf(self.source_conf)
        conf_b = Conf(self.source_conf)

        self.assertEqual(conf_a, conf_b)
        self.assertEqual(conf_a, conf_b._data)

    def test_ne_operator(self):
        """
        The __ne__ has to compare an instance with Confs and dicts.
        """
        conf_a = Conf(self.source_conf)
        conf_b = Conf(self.source_conf)

        conf_b['non-root'] = 42
        self.assertNotEqual(conf_a, conf_b)
        self.assertNotEqual(conf_a, conf_b._data)
