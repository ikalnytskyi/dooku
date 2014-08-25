# coding: utf-8
"""
    dooku.ext
    ~~~~~~~~~

    The module provides things that are allow you to load dynamically
    extensions. The idea is based on Python's ``entry_points``.

    The provided stuff is similar to stevedore_, but more lightweight
    and user-friendly.

    .. _stevedore: http://stevedore.readthedocs.org/

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
import pkg_resources


class ExtensionManager(object):
    """
    The ExtensionManager is designed to load and manage your extensions.

    The aim is to provide minimal functionality to interact with extension
    collection. Please note,  the class interacts only with the exported
    beings, so it doesn't try to create instances for those beings or
    something like that.

    What you can to do with this class?

    * load extensions from a given namespace (using names or not);
    * get extension object by name (w/ raising exception or not);
    * iterate over loaded extensions
    * check whether extension is loaded or not

    :param namespace: (str) a namespace to import from
    :param names: (list) a list of objects to import; imports all if ``None``
    :param silent: (bool) skip loading errors if ``True``
    """
    def __init__(self, namespace, names=None, silent=False):
        #: `name` <-> `extensions list` map
        #:
        #: Since extension is an exported object and know nothing about
        #: it's name, we have to save this info here for further usage.
        self._extensions = {}

        # search for extensions in a given namespace
        for entry_point in pkg_resources.iter_entry_points(namespace):
            if names is not None and entry_point.name not in names:
                continue

            try:
                ext = entry_point.load()

                if entry_point.name not in self._extensions:
                    self._extensions[entry_point.name] = []
                self._extensions[entry_point.name].append(ext)

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
