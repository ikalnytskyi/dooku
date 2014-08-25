# coding: utf-8
"""
    dooku.conf
    ~~~~~~~~~~

    The module provides a useful class to deal with configuration data.
    More info here - :class:`~dooku.conf.Conf`.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
import copy
import itertools


class Conf(object):
    """
    A :class:`dict` wrapper that extends its functionality.

    The class was designed with one purpose: to provide the more convinient
    way to interact with a `dict` instance that keeps some configuration data.
    In many ways it behaves exactly like a `dict`, but unlike the last one
    its key may be a compound::

        output_path = conf['holocron.paths.output']

    The above line will get a value of the following structure from a dict::

        {
            'holocron': {
                'paths': {
                    'output': 'path/to/output'
                }
            }
        }

    If a requested value is missing, the fallback to default can be achieved
    by using :meth:`get`::

        theme_path = conf.get('holocron.paths.theme', 'path/to/default/theme')

    The constructor receives a list of dictionaries to create a conf based
    on it. By default a compound key separator is a dot, but you can change
    it by passing a seperator option to Conf's constructor::

        conf = Conf(default_conf, user_conf, separator='#')

    :param confs: (list of dict|Conf) a list of conf data to be wrapped
    :param separator: (str) a char that's used as separator in composite keys
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
