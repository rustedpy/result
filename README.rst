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

    def get_user_input() -> str:
        if random() > 0.5:
            raise IOError('Could not read input')
        return 'my name is alice'

    def extract_name_from_input(inp: str) -> str:
        p = re.compile('my name is (\\w+)')
        m = p.match(inp)
        if m is None:
            raise ValueError('Input is invalid')
        return m.group(1)

    def authorize_user(user: str) -> bool:
        return user == 'alice'

    try:
        inp = get_user_input()
        try:
            if authorize_user(extract_name_from_input(inp)):
                print('Hi! Welcome to the secret club')
            else:
                print('Stop! You are not authorized to enter.')
        except ValueError as e:
            print('Something went wrong while trying to extract name from input', e)
    except IOError as e:
        print('Something went wrong while trying to read user input', e)

To something like this:

.. sourcecode:: python

    class AppError(Enum):
        IOError = 1
        InvalidInput = 2
        AuthorizationError = 3

    def get_user_input() -> Result[str, AppError]:
        return Ok('my name is alice')

    def extract_name_from_input(inp: str) -> Result[str, AppError]:
        p = re.compile('my name is (\\w+)')
        m = p.match(inp)
        if m is None:
            return Err(AppError.InvalidInput)
        return Ok(m.group(1))

    def authorize_user(user: str) -> Result[bool, AppError]:
        if random() > 0.5:
            return Err(AppError.AuthorizationError)
        return Ok(user == 'alice')

    auth_check = (get_user_input()
        .and_then(extract_name_from_input)
        .and_then(authorize_user))  # type: Result[bool, AppError]

    if isinstance(auth_check, Ok):
        authorized = auth_check.ok()
        if authorized:
            print('Hi! Welcome to the secret club')
        else:
            print('Stop! You are not authorized to enter.')
    else:
        print('Something went wrong', auth_check.err())

As this is Python and not Rust, you will lose some of the advantages that it
brings, like elegant combinations with the ``match`` statement. On the other
side, you don't have to return semantically unclear tuples anymore or rely on
exception for control flow. Of course a lot of Python code still throws
exceptions which you can't control and in those cases ``try/except`` is still
your friend.

Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html) have
been implemented, only the ones that make sense in the Python context. By using
``isinstance`` to check for ``Ok`` or ``Err`` you get type safe access to the
contained value when using `MyPy <https://mypy.readthedocs.io/>`__ to typecheck
your code. All of this in a package allowing easier handling of values that can
be OK or not, without resorting to custom exceptions.


Purpose
-------

A result type provide a means of controlling program execution without
resorting to exceptions when something goes wrong and code execution can't
continue along the successful path. Or to put it another way, the result type
encodes a function's result which may have failed without having to use ad-hoc
tuples, custom objects or custom exception to indicate to the caller function
failed somehow.

Why not use exceptions? Well, to list some shortcomings in no particular order,

- Custom exceptions required to indicate each possible failure case -- verbose,
  ad-hoc
- No guarantee caller is going to catch your exception -- runtime errors galore
- Exceptions implicitly propagate up, without warning, to function higher in
  the call stack probably not expecting them -- DB exception in a HTTP request
  handler?
- Runtime costs of throwing exceptions; much slower than returning a value --
  understandably a smaller issue here as opposed to something like C++, since
  Python itself is no speed demon
- Abuse and messy code -- using exceptions in non-exceptional situations, stack
  traces everywhere, harder for programmer to predict program execution path
  due to automatic exception propagation upward and difficult to predict what
  exception might be thrown if not document well

What's the alternative?

- (In combination with type annotations) Well defined return type and function
  API contract -- clear and upfront what the code does and what you should
  except back
- Facilitate and encourage caller to handle errors explicitly
- No error can implicitly or inadvertently propagate up multiple levels -- each
  caller is encouraged to explicitly handle errors instead of leaving it up to
  some function higher in the stack trace to deal with them
  - The propagation of exceptions is often a leak of implementation details and
    a violation of separation of concerns


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


See ``result.py`` source for full API.


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
