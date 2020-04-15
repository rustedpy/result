Result
======

.. image:: https://img.shields.io/github/workflow/status/dbrgn/result/CI/master
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/dbrgn/result/actions?query=workflow%3ACI+branch%3Amaster

.. image:: https://codecov.io/gh/dbrgn/result/branch/master/graph/badge.svg
    :alt: Coverage
    :target: https://codecov.io/gh/dbrgn/result

A simple Result type for Python 3 `inspired by Rust
<https://doc.rust-lang.org/std/result/>`__, fully type annotated.

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
don't get any type safety at runtime, but some easier handling of types that can
be OK or not, without resorting to custom exceptions.


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

Checking whether a result is ``Ok`` or not::

    >>> res = Ok('yay')
    >>> res.is_ok()
    True
    >>> res.is_err()
    False

Convert a ``Result`` to the value or ``None``::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.ok()
    'yay'
    >>> res2.ok()
    None

Convert a ``Result`` to the error or ``None``::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.err()
    None
    >>> res2.err()
    'nay'

Access the value directly, without any other checks::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.value
    'yay'
    >>> res2.value
    'nay'

Note that this is a property, you cannot assign to it. Results are immutable.

For your convenience, simply creating an ``Ok`` result without value is the same as using ``True``::

    >>> res1 = Result.Ok()
    >>> res1.value
    True
    >>> res2 = Ok()
    >>> res2.value
    True

The ``unwrap`` method returns the value if ``Ok`` and ``unwrap_err`` method
returns the error value if ``Err``, otherwise it raises an ``UnwrapError``::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.unwrap()
    'yay'
    >>> res2.unwrap()
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "C:\project\result\result.py", line 107, in unwrap
        return self.expect("Called `Result.unwrap()` on an `Err` value")
    File "C:\project\result\result.py", line 101, in expect
        raise UnwrapError(message)
    result.result.UnwrapError: Called `Result.unwrap()` on an `Err` value
    >>> res1.unwrap_err()
    Traceback (most recent call last):
    ...
    >>>res2.unwrap_err()
    'nay'


A custom error message can be displayed instead by using ``expect`` and ``expect_err``::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.expect('not ok')
    'yay'
    >>> res2.expect('not ok')
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "C:\project\result\result.py", line 101, in expect
        raise UnwrapError(message)
    result.result.UnwrapError: not ok
    >>> res1.expect_err('not err')
    Traceback (most recent call last):
    ...
    >>> res2.expect_err('not err')
    'nay'

A default value can be returned instead by using ``unwrap_or``::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> res1.unwrap_or('default')
    'yay'
    >>> res2.unwrap_or('default')
    'default'

Values and errors can be mapped using ``map``, ``map_or``, ``map_or_else`` and
``map_err``::

   >>> Ok(1).map(lambda x: x + 1)
   Ok(2)
   >>> Err('nay').map(lambda x: x + 1)
   Err('nay')
   >>> Ok(1).map_or(-1, lambda x: x + 1)
   2
   >>> Err(1).map_or(-1, lambda x: x + 1)
   -1
   >>> Ok(1).map_or_else(lambda: 3, lambda x: x + 1)
   2
   >>> Err('nay').map_or_else(lambda: 3, lambda x: x + 1)
   3
   >>> Ok(1).map_err(lambda x: x + 1)
   Ok(1)
   >>> Err(1).map_err(lambda x: x + 1)
   Err(2)


License
-------

MIT License
