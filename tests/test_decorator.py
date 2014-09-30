# coding: utf-8
"""
    dooku.tests.test_decorator
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests Dooku's decorator stuff.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""

from dooku.decorator import cached_property

from . import DookuTestCase


class TestCachedProperty(DookuTestCase):

    def setUp(self):
        """
        Creates a test class with a cached property.
        """
        class Foo(object):
            @cached_property
            def bar(self):
                return object()
        self.Foo = Foo

    def test_it_wraps(self):
        """
        Test that a method was converted to a cached_property.
        """
        self.assertIsInstance(self.Foo.bar, cached_property)

    def test_it_returns_the_same_instance(self):
        """
        Test that a cached property always returns the same instance.
        """
        foo = self.Foo()

        instance_a = foo.bar
        instance_b = foo.bar

        self.assertEqual(instance_a, instance_b)
        self.assertIs(instance_a, instance_b)

    def test_various_objects_have_various_instances(self):
        """
        Test that a cached property of various objects returns various
        instances.
        """
        foo_a = self.Foo()
        foo_b = self.Foo()

        instance_a = foo_a.bar
        instance_b = foo_b.bar

        self.assertNotEqual(instance_a, instance_b)
        self.assertIsNot(instance_a, instance_b)
