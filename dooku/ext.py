# coding: utf-8
"""
    dooku.ext
    ~~~~~~~~~

    The module provides things that are allow you to load dynamically
    extensions. The idea is based on Python's ``entry_points``.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""

from __future__ import absolute_import

import itertools
import pkg_resources


class ExtensionManager(object):
    """
    Load and manage your extensions with fun!

    The class was designed to provide minimal functionality to interact
    with extension collections. In many ways it works similar to
    stevedore_, but unlike the last one it operates with *exported beings*
    and doesn't create instances for those beings.

    Well, what it means for you? It means...

    * You can discover and load extensions from a given namespace.
    * You can get extension (exported being) by name.
    * You can iterate over discovered and loaded extensions.
    * You can check whether extension is loaded or not.

    Behind the class lies an idea to discover extensions by means of
    `entry_points`_. So the first thing you have to do is to declare
    your plugin in ``setup.py`` and then install it::

        setup(
            # ...
            entry_points={
                'my_plugin_namespace': [
                    'plugin_name = my_package.my_plugin:MyPluginClass',
                ]
            }
        )

    After plugin installation it becomes available for discovering and
    loading, so you probably want to get it::

        from dooku.ext import ExtensionManager

        for name, extension in ExtensionManager('my_plugin_namespace'):
            # name is plugin_name
            # extension is MyPluginClass

    You also can load plugins selectively. Look at class parameters for
    details.

    :param namespace:
        A namespace to import from as string.
    :param names:
        A list of objects to import; imports all if ``None``. If passed
        it specifies an order of imports.
    :param silent:
        Skip loading errors if ``True``; otherwise - throw exception.

    .. _stevedore:    https://stevedore.readthedocs.org/
    .. _entry_points: https://pythonhosted.org/setuptools/setuptools.html
                      #dynamic-discovery-of-services-and-plugins
    """
    def __init__(self, namespace, names=None, silent=False):
        #: `name` <-> `extensions list` map
        #:
        #: Since extension is an exported object and know nothing about
        #: it's name, we have to save this info here for further usage.
        self._extensions = {}

        # if names is passed, let's discover extensions in passed order
        if names is not None:
            entrypoints = itertools.chain.from_iterable(
                pkg_resources.iter_entry_points(namespace, name)
                for name in names)
        else:
            entrypoints = pkg_resources.iter_entry_points(namespace)

        # load extensions
        for entrypoint in entrypoints:
            try:
                ext = entrypoint.load()

                self._extensions.setdefault(entrypoint.name, [])
                self._extensions[entrypoint.name].append(ext)
            except Exception:
                if not silent:
                    raise

    def get(self, name, default=None):
        """
        Returns an extension instance with a given name.

        In case there are few extensions with a given name, the first one
        will be returned. If no extensions with a given name are exist,
        the `default` value will be returned.

        :param name: (str) an extension name
        :param default: (object) a fallback value
        :returns: (object) an extension instance
        """
        try:
            value = self[name]
        except KeyError:
            value = default
        return value

    def getall(self, name):
        """
        Returns an extension instances with a given name.

        If no extensions with a given name are exist, an empty list will
        be returned.

        :param name: (str) an extension name
        :returns: (list of object) a list of extension instances
        """
        # we're interested to return a copy to protect us
        # from unexpected modifications
        return list(self._extensions.get(name, []))

    def names(self):
        """
        Returns a list of plugin names that were loaded.

        :returns: (set) plugin names
        """
        # convert dict_keys type to set
        return set(self._extensions.keys())

    def __getitem__(self, name):
        """
        Returns an extension instance with a given name.

        In case there are few extensions with a given name, the first one
        will be returned.

        :param name: (str) an extension name
        :returns: (object) an extension instance
        """
        # we always have at least one item in the list
        return self._extensions[name][0]

    def __contains__(self, name):
        """
        Tests whether exist an extension with a given name or not.

        :param name: (str) an extension name
        :returns: (bool) True if exist; otherwise - False
        """
        return name in self._extensions

    def __iter__(self):
        """
        Returns an iterator to extensions collection.

        :returns: (object) an iterator over extensions
        """
        for key in self._extensions:
            for value in self._extensions[key]:
                yield key, value
