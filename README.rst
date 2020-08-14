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


.. contents:: Table of Contents


Description
-----------

The idea is that a result value can be either ``Ok(value)`` or ``Err(error)``,
with a way to differentiate between the two. ``Ok`` and ``Err`` are both classes
encapsulating an arbitrary value. ``Result[T, E]`` is a generic type alias for
``typing.Union[Ok[T], Err[E]]``. It will change code like this:

.. sourcecode:: python

    def validate_user(user: User) -> bool:
        """
        Check if user is valid, otherwise throws an exception
        """
        if not is_valid_username(user.name):
            # or if you're lucky a custom exception, UsernameInvalidError
            raise SomeGenericError('User\'s name is not valid')
        ... # other invalid checks and exceptions

        # Notice we never return false
        return true

    def get_user_by_email(email: str) -> User:
        """
        Gets user from DB or throws an exception if not found
        """
        if not user_exists(email):
            return DBError('User does not exist')

        user = get_user(email)
        return user

    try:
        user = get_user_by_email('ueli@example.com')
    except:
        raise RuntimeError('Could not fetch user')

    try:
        if validate_user(user):
            # do stuff with a valid user object
    except Exception as exc:
        # handle invalid user

To something like this:

.. sourcecode:: python

    from result import Ok, Err, Result

    # All possible errors for validation can be in a single place
    class ValidationError(Enum):
        InvalidUsername = auto(),
        InvalidEmail = auto(),
        BelowMinAge = auto(),

    def validate_user(details) -> Result[None, ValidationError]:
        # We don't need to care about implementation, we know what to expect!
        ...

    def get_user_by_email(email: str) -> Result[User, None]:
        # We don't need to care about implementation, we know what to expect!
        ...

    result = (get_user_by_email()
        .then(validate_user) # TODO: Should we add a `then` (or `and_then`) like Rust?
        .then(send_email_to_user) # TODO: what does send_mail_to_user return
    )
    # TODO: Finish this example
    if isinstance(result, Ok):
        ... # everything is okay, continue on
    else:
        if valdation_result.err() === ValidationError.InvalidUsername:
            ...
        if valdation_result.err() === ValidationError.InvalidEmail:
            ...

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


Purpose
-------

A result type provide a means of controlling program execution without
resorting to exceptions when something goes wrong and code execution can't
continue along the successful path. Or to put it another way, the result type
encodes a function's result which may have failed without returning ad-hoc
tuples, custom objects or custom exception to indicate to the caller function
failed somehow.

Why not use exceptions? Well, to list some shortcomings in no particular order,

- Require custom exceptions to indicate each possible failure case -- verbose,
  ad-hoc
- No guarantee caller is required to catch it -- runtime errors galore
- Failures implicitly propagate up without warning to locations not expecting
  them -- DB exception in a HTTP request handler?
- Runtime costs of throwing exceptions, much slower than returning a value --
  understandably a minor issue here as opposed to something like C++, since
  Python is no speed demon itself and due to the dynamic nature of Python
- Abuse and messy code...using exceptions in non-exceptional situations, stack
  traces everywhere, hard to predict program execution path due to automatic
  exception propagation upward

What's the alternative?

- Well defined return type and function API contract -- clear and upfront what
  the code does and what you should except back
- Facilitate and encourage caller to handle errors explicitly
- No error can propagate up multiple levels; each caller is encouraged to
  explicitly handle any possible errors instead of leaving it up to its own
  caller to deal with them when they maybe shouldn't have to or might cause
  them to understand lower level details than they should (leak implementation
  details and violate of separation of concerns)
- No need to guess all the possible exception you might encounter and need to
  handle


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
