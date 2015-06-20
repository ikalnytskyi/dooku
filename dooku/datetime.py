# coding: utf-8
"""
    dooku.datetime
    ~~~~~~~~~~~~~~

    The package provides some helper things that you might need for datetime
    manipulations: formatters and tz classes.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""

from __future__ import absolute_import

import re
import time
import datetime


def to_iso8601(dt, tz=None):
    """
    Returns an ISO-8601 representation of a given datetime instance.

        >>> to_iso8601(datetime.datetime.now())
        '2014-10-01T23:21:33.718508Z'

    :param dt: a :class:`~datetime.datetime` instance
    :param tz: a :class:`~datetime.tzinfo` to use; if None - use a default one
    """
    if tz is not None:
        dt = dt.replace(tzinfo=tz)
    iso8601 = dt.isoformat()

    # Naive datetime objects usually don't have info about timezone.
    # Let's assume it's UTC and add Z to the end.
    if re.match(r'.*(Z|[+-]\d{2}:\d{2})$', iso8601) is None:
        iso8601 += 'Z'

    return iso8601

#: The RFC-3339 is a profile (subset) of more complex ISO-8601. So it's
#: just an alias for :func:`to_iso8601` function.
to_rfc3339 = to_iso8601


class UTC(datetime.tzinfo):
    """
    Implements a UTC :class:`datetime.tzinfo`.

    You can use it to attach timezone information to datetime instances.
    Such information becomes useful if you want to represent a datetime
    instance in various timezone notations.

    Example:

        >>> from dooku.datetime import UTC
        >>> dt = datetime.datetime.now(UTC)
        >>> dt
        datetime.datetime(2014, 5, 29, 20, 22, 17, 426248, tzinfo=<...>)

    """
    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC'
UTC = UTC()


class Local(datetime.tzinfo):
    """
    Implements a Local :class:`datetime.tzinfo`.

    You can use it to attach timezone information to datetime instances.
    Such information becomes useful if you want to represent a datetime
    instance in various timezone notations.

    Example:

        >>> from dooku.datetime import UTC, Local
        >>> dt = datetime.datetime.now(UTC)
        >>> dt
        datetime.datetime(2014, 5, 29, 20, 22, 17, 426248, tzinfo=<...>)
        >>>
        >>> dt = dt.astimezone(Local)
        >>> dt
        datetime.datetime(2014, 5, 29, 23, 22, 17, 426248, tzinfo=<...>)
    """
    @staticmethod
    def _is_dst(dt):
        """
        Returns True if a given datetime object represents a time with
        DST shift.
        """
        # we can't use `dt.timestamp()` here since it requires a `utcoffset`
        # and we don't want to get into a recursive loop
        localtime = time.localtime(time.mktime((
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.weekday(),
            0,              # day of the year
            -1              # dst
        )))
        return localtime.tm_isdst > 0

    def utcoffset(self, dt):
        if self._is_dst(dt):
            return datetime.timedelta(seconds=-time.altzone)
        return datetime.timedelta(seconds=-time.timezone)

    def dst(self, dt):
        """
        Returns a difference in seconds between standard offset and
        dst offset.
        """
        if not self._is_dst(dt):
            return datetime.timedelta(0)

        offset = time.timezone - time.altzone
        return datetime.timedelta(seconds=-offset)

    def tzname(self, dt):
        return time.tzname[self._is_dst(dt)]
Local = Local()
