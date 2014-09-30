# coding: utf-8
"""
    dooku.decorator
    ~~~~~~~~~~~~~~~

    The module tries to implements various useful decorators for different
    purposes. It's very poor now, but it's planned to be extended.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""


class cached_property(object):
    """
    Decorator that converts a method into a lazy property.

    The method wrapped is called the first time to retrieve the result and
    then that calculated result is used the next time you access the value::

        class Holocron(object):

            @cached_property
            def jinja_env(self):
                # (create and configure jinja environment)
                return jinja_env


    .. admonition:: Implementation details

        The property is implemented as non-data descriptor. That's mean, the
        descriptor is invoked if there's no entry with the same name in the
        instance's ``__dict__``.

        This trick helps us to get rid of the function call overhead.
    """
    def __init__(self, func):
        self.func = func

        self.__name__ = func.__name__
        self.__module__ = func.__module__
        self.__doc__ = func.__doc__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        if self.__name__ not in obj.__dict__:
            obj.__dict__[self.__name__] = self.func(obj)
        return obj.__dict__[self.__name__]
