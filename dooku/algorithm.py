# coding: utf-8
"""
    dooku.algorithm
    ~~~~~~~~~~~~~~~

    The module implements various algorithms for different purposes.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""


def any_of(pred, iterable):
    """
    Returns ``True`` if ``pred`` returns ``True`` for any of the elements in
    the ``iterable`` range, and ``False`` otherwise.

        >>> any_of(lambda x: x == 4, [1, 2, 3, 4])
        True

    :param pred: a predicate function to check a value from the iterable range
    :param iterable: an iterable range to check in
    :returns: ``True`` if ``pred`` returns ``True`` for any of the elements
    """
    return any((pred(i) for i in iterable))


def all_of(pred, iterable):
    """
    Returns ``True`` if ``pred`` returns ``True`` for all the elements in
    the ``iterable`` range or if the range is empty, and ``False`` otherwise.

        >>> all_of(lambda x: x % 2 == 0, [2, 4, 6, 8])
        True

    :param pred: a predicate function to check a value from the iterable range
    :param iterable: an iterable range to check in
    :returns: ``True`` if ``pred`` returns ``True`` for all the elements
    """
    return all((pred(i) for i in iterable))


def find_if(pred, iterable, default=None):
    """
    Returns a reference to the first element in the ``iterable`` range for
    which ``pred`` returns ``True``. If no such element is found, the
    function returns ``default``.

        >>> find_if(lambda x: x == 3, [1, 2, 3, 4])
        3

    :param pred: a predicate function to check a value from the iterable range
    :param iterable: an iterable range to check in
    :param default: a value that will be returned if no elements were found
    :returns: a reference to the first found element or default
    """
    return next((i for i in iterable if pred(i)), default)


def none_of(pred, iterable):
    """
    Returns ``True`` if ``pred`` returns ``False`` for all the elements in
    the ``iterable`` range or if the range is empty, and ``False`` otherwise.

        >>> none_of(lambda x: x % 2 == 0, [1, 3, 5, 7])
        True

    :param pred: a predicate function to check a value from the iterable range
    :param iterable: an iterable range to check in
    :returns: ``True`` if all elements don't satfisfy ``pred``
    """
    return all((not pred(i) for i in iterable))
