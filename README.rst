Result
======

.. image:: https://img.shields.io/travis/dbrgn/result/master.svg
    :alt: Build status
    :target: https://travis-ci.org/dbrgn/result

.. image:: https://img.shields.io/pypi/dm/result.svg
    :alt: PyPI Downloads
    :target: https://pypi.python.org/pypi/result

.. image:: https://img.shields.io/coveralls/dbrgn/result/master.svg
    :alt: Coverage
    :target: https://coveralls.io/github/dbrgn/result

A simple Result type `inspired by Rust <https://doc.rust-lang.org/std/result/>`__.

The idea is that a ``Result`` value can be either ``Ok(value)`` or ``Err(error)``,
with a way to differentiate between the two. It will change code like this:

.. sourcecode:: python

    def get_user_by_email(email):
        """
        Return the user instance or an error message.
        """
        if not user_exists(email):
            return None, 'User does not exist'
        if not user_active(email):
            return None, 'User is inactive'
        user = get_user(email)
        return user, None

    user, reason = get_user_by_email('ueli@example.com')
    if user is None:
        raise RuntimeError('Could not fetch user: %s' % reason)
    else:
        do_something(user)

To something like this:

.. sourcecode:: python

    from result import Ok, Err

    def get_user_by_email(email):
        """
        Return the user instance or an error message.
        """
        if not user_exists(email):
            return Err('User does not exist')
        if not user_active(email):
            return Err('User is inactive')
        user = get_user(email)
        return Ok(user)

    user_result = get_user_by_email(email)
    if user_result.is_ok():
        do_something(user_result.value)
    else: 
        raise RuntimeError('Could not fetch user: %s' user_result.value)

As this is Python and not Rust, you will lose some of the advantages that it
brings, like elegant combinations with the ``match`` statement. On the other
side, you don't have to return semantically unclear tuples anymore.

Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html) have
been implemented, only the ones that make sense in the Python context. You still
don't get any type safety, but some easier handling of types that can be OK or
not, without resorting to custom exceptions.


API
---

Creating an instance::

    >>> from result import Ok, Err
    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')

Or through the class methods::

    >>> from result import Result
    >>> res1 = Result.Ok('yay')
    >>> res2 = Result.Err('nay')

Checking whether a result is ok or not::

    >>> res = Ok('yay')
    >>> res.is_ok()
    True
    >>> res.is_err()
    False

Convert a Result to the value or ``None``::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.ok()
    'yay'
    >>> res2.ok()
    None

Convert a Result to the error or ``None``::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.err()
    None
    >>> res2.err()
    'nay'

Access the value directly, without any other checks (like ``unwrap()`` in Rust)::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.value
    'yay'
    >>> res2.value
    'nay'

Note that this is a property, you cannot assign to it. Results are immutable.

For your convenience, simply creating an `Ok` result without value is the same as using `True`::

    >>> res1 = Result.Ok()
    >>> res1.value
    True
    >>> res2 = Ok()
    >>> res2.value
    True


In case you're missing methods like ``unwrap_or(default)``, these can be
achieved by regular Python constructs::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.ok() or 'default'
    'yay'
    >>> res2.ok() or 'default'
    'default'


License
-------

MIT License
