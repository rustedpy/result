# Result

[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/rustedpy/result/ci.yml?branch=master)](https://github.com/rustedpy/result/actions/workflows/ci.yml?query=branch%3Amaster)
[![Coverage](https://codecov.io/gh/rustedpy/result/branch/master/graph/badge.svg)](https://codecov.io/gh/rustedpy/result)

A simple Result type for Python 3 [inspired by
Rust](https://doc.rust-lang.org/std/result/), fully type annotated.

## Installation

Latest release:

``` sh
$ pip install result
```

Latest GitHub `master` branch version:

``` sh
$ pip install git+https://github.com/rustedpy/result
```

## Summary

The idea is that a result value can be either `Ok(value)` or
`Err(error)`, with a way to differentiate between the two. `Ok` and
`Err` are both classes encapsulating an arbitrary value. `Result[T, E]`
is a generic type alias for `typing.Union[Ok[T], Err[E]]`. It will
change code like this:

``` python
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
```

To something like this:

``` python
from result import Ok, Err, Result, is_ok, is_err

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
if isinstance(user_result, Ok): # or `is_ok(user_result)`
    # type(user_result.ok_value) == User
    do_something(user_result.ok_value)
else: # or `elif is_err(user_result)`
    # type(user_result.err_value) == str
    raise RuntimeError('Could not fetch user: %s' % user_result.err_value)
```

Note that `.ok_value` exists only on an instance of `Ok` and
`.err_value` exists only on an instance of `Err`.

And if you're using python version `3.10` or later, you can use the
elegant `match` statement as well:

``` python
from result import Result, Ok, Err

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Err("Cannot divide by zero")
    return Ok(a // b)

values = [(10, 0), (10, 5)]
for a, b in values:
    match divide(a, b):
        case Ok(value):
            print(f"{a} // {b} == {value}")
        case Err(e):
            print(e)
```

Not all methods
(<https://doc.rust-lang.org/std/result/enum.Result.html>) have been
implemented, only the ones that make sense in the Python context. By
using `isinstance` to check for `Ok` or `Err` you get type safe access
to the contained value when using [MyPy](https://mypy.readthedocs.io/)
to typecheck your code. All of this in a package allowing easier
handling of values that can be OK or not, without resorting to custom
exceptions.

## API

Auto generated API docs are also available at
[./docs/README.md](./docs/README.md).

Creating an instance:

``` python
>>> from result import Ok, Err
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
```

Checking whether a result is `Ok` or `Err`. You can either use `is_ok`
and `is_err` type guard **functions** or `isinstance`. This way you get
type safe access that can be checked with MyPy. The `is_ok()` or
`is_err()` **methods** can be used if you don't need the type safety
with MyPy:

``` python
>>> res = Ok('yay')
>>> isinstance(res, Ok)
True
>>> is_ok(res)
True
>>> isinstance(res, Err)
False
>>> is_err(res)
False
>>> res.is_ok()
True
>>> res.is_err()
False
```

You can also check if an object is `Ok` or `Err` by using the `OkErr`
type. Please note that this type is designed purely for convenience, and
should not be used for anything else. Using `(Ok, Err)` also works fine:

``` python
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
```

Convert a `Result` to the value or `None`:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.ok()
'yay'
>>> res2.ok()
None
```

Convert a `Result` to the error or `None`:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.err()
None
>>> res2.err()
'nay'
```

Access the value directly, without any other checks:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.ok_value
'yay'
>>> res2.err_value
'nay'
```

Note that this is a property, you cannot assign to it. Results are
immutable.

When the value inside is irrelevant, we suggest using `None` or a
`bool`, but you're free to use any value you think works best. An
instance of a `Result` (`Ok` or `Err`) must always contain something. If
you're looking for a type that might contain a value you may be
interested in a [maybe](https://github.com/rustedpy/maybe).

The `unwrap` method returns the value if `Ok` and `unwrap_err` method
returns the error value if `Err`, otherwise it raises an `UnwrapError`:

``` python
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
```

A custom error message can be displayed instead by using `expect` and
`expect_err`:

``` python
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
```

A default value can be returned instead by using `unwrap_or` or
`unwrap_or_else`:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.unwrap_or('default')
'yay'
>>> res2.unwrap_or('default')
'default'
>>> res1.unwrap_or_else(str.upper)
'yay'
>>> res2.unwrap_or_else(str.upper)
'NAY'
```

The `unwrap` method will raised an `UnwrapError`. A custom exception can
be raised by using the `unwrap_or_raise` method instead:

``` python
>>> res1 = Ok('yay')
>>> res2 = Err('nay')
>>> res1.unwrap_or_raise(ValueError)
'yay'
>>> res2.unwrap_or_raise(ValueError)
ValueError: nay
```

Values and errors can be mapped using `map`, `map_or`, `map_or_else` and
`map_err`:

``` python
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
```

To save memory, both the `Ok` and `Err` classes are ‘slotted’, i.e. they
define `__slots__`. This means assigning arbitrary attributes to
instances will raise `AttributeError`.

### `as_result` Decorator

The `as_result()` decorator can be used to quickly turn ‘normal’
functions into `Result` returning ones by specifying one or more
exception types:

``` python
@as_result(ValueError, IndexError)
def f(value: int) -> int:
    if value == 0:
        raise ValueError  # becomes Err
    elif value == 1:
        raise IndexError  # becomes Err
    elif value == 2:
        raise KeyError  # raises Exception
    else:
        return value  # becomes Ok

res = f(0)  # Err[ValueError()]
res = f(1)  # Err[IndexError()]
res = f(2)  # raises KeyError
res = f(3)  # Ok[3]
```

`Exception` (or even `BaseException`) can be specified to create a
‘catch all’ `Result` return type. This is effectively the same as `try`
followed by `except Exception`, which is not considered good practice in
most scenarios, and hence this requires explicit opt-in.

Since `as_result` is a regular decorator, it can be used to wrap
existing functions (also from other libraries), albeit with a slightly
unconventional syntax (without the usual `@`):

``` python
import third_party

x = third_party.do_something(...)  # could raise; who knows?

safe_do_something = as_result(Exception)(third_party.do_something)

res = safe_do_something(...)  # Ok(...) or Err(...)
if isinstance(res, Ok):
    print(res.ok_value)
```

### Do notation

Do notation is syntactic sugar for a sequence of `and_then()` calls.
Much like the equivalent in Rust or Haskell, but with different syntax.
Instead of `x <- Ok(1)` we write `for x in Ok(1)`. Since the syntax is
generator-based, the final result must be the first line, not the last.

``` python
final_result: Result[int, str] = do(
    Ok(x + y)
    for x in Ok(1)
    for y in Ok(2)
)
```

Note that if you exclude the type annotation,
`final_result: Result[float, int] = ...`, your type checker may be
unable to infer the return type. To avoid an errors or warnings from
your type checker, you should add a type hint when using the `do`
function.

This is similar to Rust's [m!
macro](https://docs.rs/do-notation/latest/do_notation/):

``` rust
use do_notation::m;
let r = m! {
    x <- Some(1);
    y <- Some(2);
    Some(x + y)
};
```

Note that if your do statement has multiple <span
class="title-ref">for\`s, you can access an identifier bound in a
previous \`for</span>. Example:

``` python
my_result: Result[int, str] = do(
    f(x, y, z)
    for x in get_x()
    for y in calculate_y_from_x(x)
    for z in calculate_z_from_x_y(x, y)
)
```

You can use `do()` with awaited values as follows:

``` python
async def process_data(data) -> Result[int, str]:
    res1 = await get_result_1(data)
    res2 = await get_result_2(data)
    return do(
        Ok(x + y)
        for x in res1
        for y in res2
    )
```

However, if you want to await something inside the expression, use
`do_async()`:

``` python
async def process_data(data) -> Result[int, str]:
    return do_async(
        Ok(x + y)
        for x in await get_result_1(data)
        for y in await get_result_2(data)
    )
```

Troubleshooting `do()` calls:

``` python
TypeError("Got async_generator but expected generator")
```

Sometimes regular `do()` can handle async values, but this error means
you have hit a case where it does not. You should use `do_async()` here
instead.

## Contributing

These steps should work on any Unix-based system (Linux, macOS, etc) with Python
and `make` installed. On Windows, you will need to refer to the Python
documentation (linked below) and reference the `Makefile` for commands to run
from the non-unix shell you're using on Windows.

1. Setup and activate a virtual environment. See [Python docs][pydocs-venv] for more
   information about virtual environments and setup.
2. Run `make install` to install dependencies
3. Switch to a new git branch and make your changes
4. Test your changes:
  - `make test`
  - `make lint`
  - You can also start a Python REPL and import `result`
5. Update documentation
  - Edit any relevant docstrings, markdown files
  - Run `make docs`
6. Add an entry to the [changelog](./CHANGELOG.md)
5. Git commit all your changes and create a new PR.

[pydocs-venv]: https://docs.python.org/3/library/venv.html

## FAQ

-   **Why do I get the "Cannot infer type argument" error with MyPy?**

There is [a bug in MyPy](https://github.com/python/mypy/issues/230)
which can be triggered in some scenarios. Using `if isinstance(res, Ok)`
instead of `if res.is_ok()` will help in some cases. Otherwise using
[one of these
workarounds](https://github.com/python/mypy/issues/3889#issuecomment-325997911)
can help.

## License

MIT License
