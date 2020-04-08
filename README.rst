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

The idea is that a result value can be either ``Ok(value)`` or ``Err(error)``,
with a way to differentiate between the two. ``Ok`` and ``Err`` are both classes
encapsulating an arbitrary value. ``Result[T, E]`` is a generic type alias for
``typing.Union[Ok[T], Err[E]]``. It will change code like this:

.. sourcecode:: python

    def get_user_by_email(email: str) -> Tuple[Optional[User], Optional[str]]:
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

    from result import Ok, Err, Result

    def get_user_by_email(email: str) -> Result[User, str]:
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
    if isinstance(user_result, Ok):
        # type(user_result.value) == User
        do_something(user_result.value)
    else:
        # type(user_result.value) == str
        raise RuntimeError('Could not fetch user: %s' % user_result.value)

As this is Python and not Rust, you will lose some of the advantages that it
brings, like elegant combinations with the ``match`` statement. On the other
side, you don't have to return semantically unclear tuples anymore.

Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html) have
been implemented, only the ones that make sense in the Python context. By using
``isinstance`` to check for ``Ok`` or ``Err`` you get type safe access to the
contained value when using `MyPy <https://mypy.readthedocs.io/>`__ to typecheck
your code. All of this in a package allowing easier handling of values that can
be OK or not, without resorting to custom exceptions.


API
---

Creating an instance::

    >>> from result import Ok, Err
    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')

Checking whether a result is ``Ok`` or ``Err``. With ``isinstance`` you get type safe
access that can be checked with MyPy. The ``is_ok()`` or ``is_err()`` methods can be
used if you don't need the type safety with MyPy::

    >>> res = Ok('yay')
    >>> isinstance(res, Ok)
    True
    >>> isinstance(res, Err)
    False
    >>> res.is_ok()
    True
    >>> res.is_err()
    False

You can also check if an object is ``Ok`` or ``Err`` by using the ``OkErr`` type.
Please note that this type is designed purely for convenience, and should not be used
for anything else. Using ``(Ok, Err)`` also works fine::

    >>> res1 = Ok('yay')
    >>> res2 = Err('nay')
    >>> isinstance(res1, OkErr)
    True
    >>> isinstance(res2, OkErr)
    True
    >>> isinstance(1, OkErr)
    False
    >>> isinstance(res1, (Ok, Err))
    True

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

    >>> res1 = Ok()
    >>> res1.value
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


FAQ
-------


- **Why do I get the "Cannot infer type argument" error with MyPy?**

There is `a bug in MyPy
<https://github.com/python/mypy/issues/230>`_ which can be triggered in some scenarios.
Using ``if isinstance(res, Ok)`` instead of ``if res.is_ok()`` will help in some cases.
Otherwise using `one of these workarounds
<https://github.com/python/mypy/issues/3889#issuecomment-325997911>`_ can help.



License
-------

MIT License
