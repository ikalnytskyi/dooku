# coding: utf-8
"""
    dooku.conf
    ~~~~~~~~~~

    The module provides a useful class to deal with configuration data.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
import json
import copy
import collections
import itertools

# In real world there's a common practice to keep settings in YAMLs, since
# it's very readable. But unfortunately the PyYAML module (which provides
# stuff for loading YAMLs) isn't a part of Python standard library, so
# we need to try load it safely. In case of success - the global name should
# represent the module itself; otherwise - it should be None.
try:
    import yaml
except ImportError:
    yaml = None


class Conf(collections.MutableMapping):
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

    In addition to compound keys and update method, the class provides two
    helpers - :meth:`from_json` and :meth:`from_yaml` - for loading and
    updating a Conf instance from files. ::

        conf = Conf(default_conf)
        conf.from_json('path/to/user/conf.json')

    .. note:: You have to install ``PyYAML`` before using :meth:`from_yaml`.

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

    def from_json(self, filename, encoding='utf-8', silent=False):
        """
        Updates recursively the value in the the config from a JSON file.

        :param filename: (str) the filename of the JSON file
        :param silent: (bool) fails silently if something wrong with json file

        .. versionadded:: 0.3.0
        """
        conf = {}
        try:
            with open(filename, encoding=encoding) as f:
                conf = json.load(f)
        except Exception:
            if not silent:
                raise
        self.update(conf)

    def from_yaml(self, filename, encoding='utf-8', silent=False):
        """
        Updates recursively the value in the the config from a YAML file.

        The method requires the PyYAML to be installed.

        :param filename: (str) the filename of the YAML file
        :param silent: (bool) fails silently if something wrong with yaml file

        .. versionadded:: 0.3.0
        """
        if not yaml:
            raise AttributeError(
                'You need to install PyYAML before using this method!')

        conf = {}
        try:
            with open(filename, encoding=encoding) as f:
                conf = yaml.load(f)
        except Exception:
            if not silent:
                raise
        self.update(conf)

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

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, repr(self._data))
