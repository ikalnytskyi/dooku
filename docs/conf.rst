.. _conf:

dooku.conf
==========

Dooku has simple and powerful wrapper around :class:`dict` that provides
the more convenient way too interact with ``dict`` instances that keep some
configuration data.

The main feature is to provide so called `compound key` support that allows
you to get desirable value with one request, no matter how deep it::

    path = conf['holocron.paths.output']

The above line will get a value from a ``dict`` like

::

    {
        'holocron': {
            'paths': {
                'output': 'path/to/output'
            }
        }
    }

and will throw a ``KeyError`` exception in case the key is absent.


How To Use?
-----------

You can use it exactly like a ``dict``, but with possibilities to specify
compound keys::

    from dooku.conf import Conf

    conf = Conf({
        'holocron': {
            'paths': {
                'output': 'path/to/output'
            }
        }
    })

    # You can use the conf instance in a dict manner, since
    # it tries to be dict compatible. To retrieve a value use
    # the bracket syntax or "get" method.

    path_a = conf['holocron.paths.output']          # ok
    path_b = conf.get('holocron.paths.output')      # ok

    path_c = conf['holocron.paths.input']           # raises KeyError
    path_d = conf.get('holocron.paths.input')       # returns None

    # you can check an option for existance
    if 'holocron.settings' in conf:
        pass

You can change a separate character in case you don't like a dot (``.``).
In order to get it done just pass a ``separator`` option to ``Conf``'s
constructor::

    conf = Conf(data, separator='@')
    conf['root@child@subchild'] = 'some value'


Options
-------

Here is the list of options that you can pass to Conf constructor:

===============   =====================================================
 ``*args``         a list of dict instances that will be wrapped
---------------   -----------------------------------------------------
 ``separator``     a separator character that's used in compound keys
===============   =====================================================
