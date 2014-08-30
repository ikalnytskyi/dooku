.. _datetime:

dooku.datetime
==============

Dooku provides some missed primitives for datetime manipulating. This part
was born during Holocron_ development where we were needed to do next things:

* represent a :class:`~datetime.datetime` in ISO-8601 format;
* convert a :class:`~datetime.datetime` from local time to UTC and vice versa.

As for now that's the only things the Dooku can handle.

.. _Holocron: https://github.com/ikalnitsky/holocron


How To Use?
-----------

Simple! The datetime part of Dooku is fully compatible with the built-in
:mod:`datetime` module. Let me show you how it works. Just look at next
example::

    >>> import datetime
    >>> from dooku.datetime import UTC, Local, to_iso8601
    >>>
    >>> dt = datetime.datetime.now(UTC)
    >>> dt
    datetime.datetime(2014, 5, 29, 20, 22, 17, 426248, tzinfo=<...>)
    >>>
    >>> dt = dt.astimezone(Local)
    >>> dt
    datetime.datetime(2014, 5, 29, 23, 22, 17, 426248, tzinfo=<...>)
    >>>
    >>> to_iso8601(dt)
    '2014-05-29T23:22:17.426248+03:00'

I think that will give you a basic understanding of what's going on and how to
handle it, but later I'll provide more detail documentation.
