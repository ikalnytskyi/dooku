# coding: utf-8
"""
    dooku.conf
    ~~~~~~~~~~

    The module provides a useful class to deal with configuration data.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
import copy
import itertools


class Conf(object):
    """
    A :class:`dict` wrapper that extends its functionality.

    The class was designed with one purpose: to provide the more convenient
    way to interact with dictionary instances that keep some configuration
    data. In many ways it behaves exactly like a dictionary, but unlike the
    last one it can be accessed by a *compound key* and supports *recursive
    update*.

    A Compound Key is a key that consists of two or more keys that allow
    you to retrieve value from subnode of subnode. For example, we have
    the following structure ::

        { 'ukraine': {
            'kharkiv': {
              'timezone': 'UTC+2', }, }, }

    and you want to get the timezone's value with one query. Well, with
    compound keys you can do it this way ::

        timezone = conf['ukraine.kharkiv.timezone']

    instead of usual ::

        timezone = conf['ukraine']['kharkiv']['timezone']

    On the other hand we have a usual dictionary behaviour:

    * a ``KeyError`` exception will be thrown in case of key absence
    * a :meth:`get` method is provided to retrieve values safely

    The class overrides an :meth:`update` method so it can be used to
    recursively update values. For example, we have the following structure ::

        { 'ukraine': {
            'kharkiv': {
              'timezone': 'UTC+2', }, }, }

    and want to update it with next one ::

        { 'ukraine': {
            'kharkiv': {
              'population': '1 427 000', }, }, }

    In vanilla Python's dictionary we will have the same result as statement
    above since it completely overwrites top-level keys, but our class can
    handle it properly and merge it automatically, so we will have next
    result ::

        { 'ukraine': {
            'kharkiv': {
              'timezone': 'UTC+2',
              'population': '1 427 000', }, }, }

    :param confs:
        A list of dictionaries to create a Conf instance based on it.
        Each next dictionary overrides settings from the previous one.
    :param separator:
        A character that's used as separator in compound keys
    """

    #: this character will be used as a separator in case you don't
    #: set a new one explicitly
    default_separator = '.'

    def __init__(self, *confs, **options):
        self._data = {}
        self._separator = options.get('separator', self.default_separator)

        for conf in confs:
            self.update(copy.deepcopy(conf))

    def update(self, iterable={}, **kwargs):
        """
        Updates recursively a self with a given iterable.

        TODO: rewrite this ugly stuff
        """
        def _merge(a, *args):
            for key, value in itertools.chain(*args):
                if key in a and isinstance(value, (dict, Conf)):
                    value = _merge(a[key], value.items())
                a[key] = value
            return a

        # adopt iterable sequence to unified interface: (key, value)
        if isinstance(iterable, (dict, Conf)):
            iterable = iterable.items()

        # iterate and update values
        _merge(self._data, iterable, kwargs.items())

    def items(self):
        """
        Returns an iterator of a sequence of pairs ``(key, value)``, just
        like it works for ``dict``.

        :returns: (iter) an iterator of a sequence of key-value pairs
        """
        return self._data.items()

    def get(self, compound_key, default=None):
        """
        Returns a value that's associated with a given compound key.

        Unlike :meth:`__getitem__`, the method provides fallback to default
        in case key doesn't exist.

        :param compound_key: (str) a key for retrieving value
        :param default: (object) a default value
        :returns: (object) retrieved value if key exists; otherwise - default
        """
        try:
            value = self[compound_key]
        except KeyError:
            value = default
        return value

    def __getitem__(self, compound_key):
        """
        Returns a value that's associated with a given compound key.

        :param compound_key: (str) a key for retrieving value
        :returns: (object) retrieved value if key exists
        :raises KeyError: a given key does not exist
        """
        conf = self._data

        for key in compound_key.split(self._separator):
            conf = conf[key]

        # We need to return dict as Conf instance to make possible use Conf's
        # features on it. The returned object is used exactly like a wrapper,
        # since it doesn't make a full copy of a given dict.
        if isinstance(conf, dict):
            rv = Conf(separator=self._separator)
            rv._data = conf
            return rv

        return conf

    def __setitem__(self, compound_key, value):
        """
        Sets a value for given option.

        :param compound_key: (str) an option to change
        :param value: (object) a value to set
        :raises KeyError: an option doesn't exist
        """
        conf = self._data
        keys = compound_key.split(self._separator)
        for key in keys[:-1]:
            if key not in conf:
                conf[key] = {}
            conf = conf[key]
        conf[keys[-1]] = value

    def __delitem__(self, compound_key):
        """
        Remove a given compound key from the instance.

        :param compound_key: (str) a key to delete
        """
        conf = self._data
        keys = compound_key.split(self._separator)
        for key in keys[:-1]:
            conf = conf[key]
        del conf[keys[-1]]

    def __contains__(self, compound_key):
        """
        Checks if a given compound key exists.

        :param compound_key: (str) a key to check
        :returns: (bool) True if exists; otherwise - False
        """
        try:
            self[compound_key]
        except KeyError:
            return False
        return True

    def __eq__(self, other):
        """
        Equality operator implementation makes us possible to compare
        Conf instances with other Conf instances, or even dictionaries.

        :param other: (dict, Conf) an instance to compare with
        :returns: True if `self` is equal to `other`; otherwise - False
        """
        if isinstance(other, dict):
            return self._data == other
        elif isinstance(other, Conf):
            return self._data == other._data
        return False

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, repr(self._data))
