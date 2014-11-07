# coding: utf-8
"""
    dooku.tests.test_datetime
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests Dooku's datetime library.

    :copyright: (c) 2014, Igor Kalnitsky
    :license: BSD, see LICENSE for details
"""
import re
import time
import datetime

from dooku.datetime import UTC, Local, to_iso8601
from . import DookuTestCase


class TestDatetimeTz(DookuTestCase):
    def test_utc_is_instance(self):
        """
        The UTC tz imlementation has to be an instance of built-in
        :class:`~datetime.tzinfo` class.
        """
        self.assertIsInstance(UTC, datetime.tzinfo)

    def test_local_is_instance(self):
        """
        The Local tz imlementation has to be an instance of built-in
        :class:`~datetime.tzinfo` class.
        """
        self.assertIsInstance(Local, datetime.tzinfo)

    def test_utc_timezone(self):
        """
        The UTC tz implementation has to meet next criteria:

        * utcoffset is 0 (there's no time shift)
        * dst is 0 (off)
        * datetime's timetuple and utctimetuple are equal
        """
        now = datetime.datetime.now(UTC)

        self.assertEqual(now.utcoffset(), datetime.timedelta(0))
        self.assertEqual(now.dst(), datetime.timedelta(0))
        self.assertEqual(now.utctimetuple(), now.timetuple())

    def test_local_timezone(self):
        """
        The Local tz implementation has to meet next criteria:

        * utcoffset has to be either time.timezone or time.altzone depends
          on time.daylight value;
        * dst has to be either 0 or difference between time.altzone and
          time.timezone;
        * datetime's timetuple and utctimetuple are not equal
        """
        l_dst = datetime.timedelta(0)
        l_timezone = datetime.timedelta(seconds=-time.timezone)

        if time.localtime().tm_isdst:
            l_dst = datetime.timedelta(seconds=time.altzone - time.timezone)
            l_timezone = datetime.timedelta(seconds=-time.altzone)

        now = datetime.datetime.now(Local)
        self.assertEqual(now.utcoffset(), l_timezone)
        self.assertEqual(now.dst(), l_dst)

    def test_local_utc_convertion(self):
        """
        UTC <-> Local timzone convertions should be consistent.
        """
        now = datetime.datetime.now(UTC)
        lcl = datetime.datetime.now(Local)

        self.assertEqual(
            now.astimezone(Local).astimezone(UTC), now)

        self.assertEqual(
            lcl.astimezone(UTC).astimezone(Local), lcl)


class TestDatetimeFormat(DookuTestCase):
    re_iso8601 = re.compile(
        r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,})?(Z|[-+]\d{2}:\d{2})$'
    )

    def test_re_iso8601(self):
        """
        The re_iso8601 regex has to work correct and without mistakes, since
        it's a judge of other test cases.
        """
        dataset = (
            # valid set
            ('2014-05-24T17:16:16Z', self.assertRegex),
            ('2014-05-24T17:16:16.42Z', self.assertRegex),
            ('2014-05-24T17:16:16.42+01:00', self.assertRegex),
            ('2014-05-24T17:16:16+01:00', self.assertRegex),
            ('2014-05-24T17:16:16-01:00', self.assertRegex),
            ('2014-05-24T17:16:16.42+01:00', self.assertRegex),
            ('2014-05-24T17:16:16.42-01:00', self.assertRegex),

            # invalid set
            ('2014-05-24T17:16', self.assertNotRegex),
            ('2014-05-24T17:16:16', self.assertNotRegex),
            ('2014-05-24T17:16:16.Z', self.assertNotRegex),
            ('2014-05-24T17:16:16.42', self.assertNotRegex),
            ('2014-05-24T17:16:16+01:001', self.assertNotRegex),
            ('2014-05-24T17:16:16+001:00', self.assertNotRegex),
            ('2014-05-24T17:16:16+01:1', self.assertNotRegex),
            ('2014-05-24T17:16:16+1:01', self.assertNotRegex),
            ('2014-05-24T17:16:16+1:1', self.assertNotRegex),
            ('2014-05-24T17:16:16+01:20Z', self.assertNotRegex),
        )

        for text, assert_fn in dataset:
            assert_fn(text, self.re_iso8601)

    def test_iso8601(self):
        """
        The to_iso8601 has to produce a valid output for naive datetime
        objects.
        """
        now = datetime.datetime.now()
        now = to_iso8601(now)

        self.assertRegex(now, self.re_iso8601)

    def test_iso8601_utc(self):
        """
        The to_iso8601 has to produce a valid output for aware datetime
        objects.
        """
        now = datetime.datetime.now(UTC)
        now = to_iso8601(now)

        self.assertRegex(now, self.re_iso8601)
        self.assertTrue(now.endswith('Z') or now.endswith('+00:00'))

    def test_iso8601_local(self):
        """
        The to_iso8601 has to produce a valid output for aware datetime
        objects.
        """
        now = datetime.datetime.now(Local)
        now = to_iso8601(now)

        self.assertRegex(now, self.re_iso8601)
        self.assertTrue(not now.endswith('Z'))
