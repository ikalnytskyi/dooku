.. _datetime:

Datetime Helpers
================

Dooku provides some missed primitives for datetime manipulating. This part
was born during Holocron_ development where we were needed to do next things:

* represent a :class:`~datetime.datetime` in ISO-8601 format;
* convert a :class:`~datetime.datetime` from local time to UTC and vice versa.

.. _Holocron: https://github.com/ikalnitsky/holocron


Timezones
---------

.. autodata:: dooku.datetime.UTC
   :annotation:
.. autodata:: dooku.datetime.Local
   :annotation:


Formatters
----------

.. autofunction:: dooku.datetime.to_iso8601
.. autofunction:: dooku.datetime.to_rfc3339
