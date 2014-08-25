# coding: utf-8
"""
    dooku.algorithm
    ~~~~~~~~~~~~~~~

    The module tries to implements various algorithms for different
    purposes. It's very poor now, but it's planned to be extended.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""


def any_of(pred, iterable):
    """
    Returns ``True`` if ``pred`` returns ``True`` for any of the elements in
    the ``iterable`` range, and ``False`` otherwise.

    :param pred: a predicate function to check a value from the iterable range
    :param iterable: an iterable range to check in
    :returns: ``True`` if ``pred`` returns ``True`` for any of the elements
    """
    return any((pred(i) for i in iterable))


def all_of(pred, iterable):
    """
    Returns ``True`` if ``pred`` returns ``True`` for all the elements in
    the ``iterable`` range or if the range is empty, and ``False`` otherwise.

    :param pred: a predicate function to check a value from the iterable range
    :param iterable: an iterable range to check in
    :returns: ``True`` if ``pred`` returns ``True`` for all the elements
    """
    return all((pred(i) for i in iterable))


def none_of(pred, iterable):
    """
    Returns ``True`` if ``pred`` returns ``False`` for all the elements in
    the ``iterable`` range or if the range is empty, and ``False`` otherwise.

    :param pred: a predicate function to check a value from the iterable range
    :param iterable: an iterable range to check in
    :returns: ``True`` if all elements don't satfisfy ``pred``
    """
    return all((not pred(i) for i in iterable))


def find_if(pred, iterable, default=None):
    """
    Returns a reference to the first element in the ``iterable`` range for
    which ``pred`` returns ``True``. If no such element is found, the
    function returns ``default``.

    :param pred: a predicate function to check a value from the iterable range
    :param iterable: an iterable range to check in
    :param default: a value that will be returned if no elements were found
    :returns: a reference to the first found element or default
    """
    return next((i for i in iterable if pred(i)), default)
