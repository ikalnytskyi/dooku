====================================================
 Dooku: a set of libraries for the Force-sensitives
====================================================

|travis-ci|  |coveralls|

Dooku is a set of libraries for Python programming language that provides
various useful stuff that you might need in everyday usage. The idea is to
provide a set of libraries and useful functions, just like Boost_ does in
C++ world.

Dooku is a good not only as a set of libraries, it also may be used as a
some kind of incubator where various developers can test and evolve their
projects. So please **don't hesitate** to propose your library to be a
part of Dooku.

Feel the Force? Then try Dooku!

.. code:: bash

    $ [sudo] pip install dooku


Features
--------

Here is an incomplete list of features:

* Missed Python `algorithms`_.
* Convenient `configuration manager`_.
* `Datetime` helpers for managing timezones.
* Set of useful `decorators`_.
* Simple & powerful `extension manager`_.


Check out Dooku's documentation for further information -
http://dooku.readthedocs.org/.


What Do I Require?
------------------

Different parts of Dooku may have different requirements, but generally
requirements are:

* Python 2.7 or higher (+ PyPy / PyPy3)
* GNU/Linux, Unix, OS X, Windows


Why The Name Dooku?
-------------------

Dooku is an interesting character from the Star Wars franchise. He is
self-contained and powerful, exactly like this library itself.


.. Links

.. _Boost: http://www.boost.org
.. _algorithms: http://dooku.readthedocs.org/en/latest/algorithm.html
.. _configuration manager: http://dooku.readthedocs.org/en/latest/conf.html
.. _Datetime: http://dooku.readthedocs.org/en/latest/datetime.html
.. _decorators: http://dooku.readthedocs.org/en/latest/decorator.html
.. _extension manager: http://dooku.readthedocs.org/en/latest/ext.html

.. Images

.. |travis-ci| image::
       https://travis-ci.org/ikalnitsky/dooku.svg?branch=master
   :target: https://travis-ci.org/ikalnitsky/dooku
   :alt: Travis CI: continuous integration status

.. |coveralls| image::
       https://coveralls.io/repos/ikalnitsky/dooku/badge.png?branch=master
   :target: https://coveralls.io/r/ikalnitsky/dooku?branch=master
   :alt: Coverall: code coverage status
