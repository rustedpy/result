"""A Rust-like Result type for Python."""

from __future__ import annotations

import functools
import inspect
from collections.abc import AsyncGenerator, Awaitable, Callable, Generator, Iterator
from typing import (
    Any,
    Final,
    Generic,
    Literal,
    NoReturn,
    ParamSpec,
    TypeAlias,
    TypeVar,
    cast,
)

from typing_extensions import TypeIs

T_co = TypeVar("T_co", covariant=True)  # Success type
E_co = TypeVar("E_co", covariant=True)  # Error type
U = TypeVar("U")
F = TypeVar("F")
P = ParamSpec("P")
R = TypeVar("R")
TBE = TypeVar("TBE", bound=BaseException)


class Ok(Generic[T_co]):
    """An ``Ok`` value indicating success, storing arbitrary data for the return value."""

    __match_args__ = ("ok_value",)
    __slots__ = ("_value",)

    def __iter__(self) -> Iterator[T_co]:
        yield self._value

    def __init__(self, value: T_co) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Ok({self._value!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ok) and self._value == other._value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self._value))

    def is_ok(self) -> Literal[True]:
        """Return ``True`` because this is an ``Ok`` value."""
        return True

    def is_err(self) -> Literal[False]:
        """Return ``False`` because this is an ``Ok`` value."""
        return False

    def ok(self) -> T_co:
        """Convert from ``Result[T, E]`` to ``T | None``.

        Return the contained ``Ok`` value, discarding the error, if any.
        """
        return self._value

    def err(self) -> None:
        """Convert from ``Result[T, E]`` to ``E | None``.

        Return ``None``, discarding the success value.
        """
        return

    @property
    def ok_value(self) -> T_co:
        """The contained ``Ok`` value."""
        return self._value

    def expect(self, _message: str) -> T_co:
        """Return the contained ``Ok`` value.

        Because this is an ``Ok``, the *message* argument is unused.

        Raises:
            UnwrapError: Never raised for ``Ok``.

        """
        return self._value

    def expect_err(self, message: str) -> NoReturn:
        """Return the contained ``Err`` value.

        Raises:
            UnwrapError: Always, because this is an ``Ok`` value, with a
                message including the passed *message* and the ``Ok`` content.

        """
        raise UnwrapError(self, message)

    def unwrap(self) -> T_co:
        """Return the contained ``Ok`` value.

        Because this is an ``Ok``, this method never raises.

        Raises:
            UnwrapError: Never raised for ``Ok``.

        """
        return self._value

    def unwrap_err(self) -> NoReturn:
        """Return the contained ``Err`` value.

        Raises:
            UnwrapError: Always, because this is an ``Ok`` value.

        """
        raise UnwrapError(self, "Called `Result.unwrap_err()` on an `Ok` value")

    def unwrap_or(self, _default: U) -> T_co:
        """Return the contained ``Ok`` value or a provided default.

        The default value is ignored because this is an ``Ok``.
        """
        return self._value

    def unwrap_or_else(self, _op: object) -> T_co:
        """Return the contained ``Ok`` value or compute it from a callable.

        The callable is never invoked because this is an ``Ok``.
        """
        return self._value

    def unwrap_or_raise(self, _e: object) -> T_co:
        """Return the contained ``Ok`` value or raise the provided exception.

        The exception is never raised because this is an ``Ok``.
        """
        return self._value

    def map(self, op: Callable[[T_co], U]) -> Ok[U]:
        """Apply *op* to the contained ``Ok`` value.

        Map a ``Result[T, E]`` to ``Result[U, E]``, leaving an ``Err`` value untouched.
        """
        return Ok(op(self._value))

    async def map_async(self, op: Callable[[T_co], Awaitable[U]]) -> Ok[U]:
        """Async version of ``map``.

        Await the coroutine returned by *op* applied to the contained ``Ok`` value.
        """
        return Ok(await op(self._value))

    def map_or(self, _default: object, op: Callable[[T_co], U]) -> U:
        """Apply *op* to the contained ``Ok`` value, or return *default* if ``Err``.

        Since this is ``Ok``, *default* is ignored.
        """
        return op(self._value)

    def map_or_else(self, _default_op: object, op: Callable[[T_co], U]) -> U:
        """Apply *op* to a contained ``Ok`` value, or *default_op* to a contained ``Err``.

        Map a ``Result[T, E]`` to ``U``.
        """
        return op(self._value)

    def map_err(self, _op: object) -> Ok[T_co]:
        """Apply *op* to a contained ``Err`` value, leaving ``Ok`` untouched.

        Map a ``Result[T, E]`` to ``Result[T, F]``.
        """
        return self

    def and_then(self, op: Callable[[T_co], Result[U, E_co]]) -> Result[U, E_co]:
        """Call *op* if the result is ``Ok``, otherwise return the ``Err`` value of *self*.

        This function can be used for control flow based on ``Result`` values.
        """
        return op(self._value)

    async def and_then_async(
        self,
        op: Callable[[T_co], Awaitable[Result[U, E_co]]],
    ) -> Result[U, E_co]:
        """Async version of ``and_then``.

        Await the coroutine returned by *op* applied to the contained ``Ok`` value.
        """
        return await op(self._value)

    def or_else(self, _op: object) -> Ok[T_co]:
        """Call *op* if the result is ``Err``, otherwise return the ``Ok`` value of *self*.

        Since this is ``Ok``, *op* is never called.
        """
        return self

    def inspect(self, op: Callable[[T_co], Any]) -> Result[T_co, E_co]:
        """Call *op* with the contained value if ``Ok``.

        Return the original result unchanged.
        """
        op(self._value)
        return self

    def inspect_err(self, _op: Callable[[E_co], Any]) -> Result[T_co, E_co]:
        """Call *op* with the contained error if ``Err``.

        Return the original result unchanged. Since this is ``Ok``, *op* is not called.
        """
        return self


class _DoError(Exception):
    """Signal to ``do()`` that the result is an ``Err``, short-circuiting the generator."""

    def __init__(self, err: Err[Any]) -> None:
        self.err: Err[Any] = err


class Err(Generic[E_co]):
    """An ``Err`` value signifying failure, storing arbitrary data for the error."""

    __match_args__ = ("err_value",)
    __slots__ = ("_value",)

    def __iter__(self) -> Iterator[NoReturn]:
        def _iter() -> Iterator[NoReturn]:
            raise _DoError(self)
            # This yield is syntactically required to make _iter a generator
            # function, but it is never reached because _DoError is always
            # raised first.  Suppressing the unreachable diagnostic is the only
            # viable option — Python requires the yield keyword to be present
            # for the function to be recognised as a generator.
            yield  # type: ignore[unreachable]

        return _iter()

    def __init__(self, value: E_co) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Err({self._value!r})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Err) and self._value == other._value

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, self._value))

    def is_ok(self) -> Literal[False]:
        """Return ``False`` because this is an ``Err`` value."""
        return False

    def is_err(self) -> Literal[True]:
        """Return ``True`` because this is an ``Err`` value."""
        return True

    def ok(self) -> None:
        """Convert from ``Result[T, E]`` to ``T | None``.

        Return ``None``, discarding the error value.
        """
        return

    def err(self) -> E_co:
        """Convert from ``Result[T, E]`` to ``E | None``.

        Return the contained ``Err`` value, discarding the success value, if any.
        """
        return self._value

    @property
    def err_value(self) -> E_co:
        """The contained ``Err`` value."""
        return self._value

    def expect(self, message: str) -> NoReturn:
        """Return the contained ``Ok`` value.

        Raises:
            UnwrapError: Always, because this is an ``Err`` value, with a
                message including the passed *message* and the ``Err`` content.

        """
        exc = UnwrapError(
            self,
            f"{message}: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

    def expect_err(self, _message: str) -> E_co:
        """Return the contained ``Err`` value.

        Because this is an ``Err``, the *message* argument is unused.

        Raises:
            UnwrapError: Never raised for ``Err``.

        """
        return self._value

    def unwrap(self) -> NoReturn:
        """Return the contained ``Ok`` value.

        Raises:
            UnwrapError: Always, because this is an ``Err`` value, with a
                message provided by the ``Err`` content.

        """
        exc = UnwrapError(
            self,
            f"Called `Result.unwrap()` on an `Err` value: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

    def unwrap_err(self) -> E_co:
        """Return the contained ``Err`` value.

        Because this is an ``Err``, this method never raises.

        Raises:
            UnwrapError: Never raised for ``Err``.

        """
        return self._value

    def unwrap_or(self, default: U) -> U:
        """Return the contained ``Ok`` value or a provided default.

        The contained ``Err`` value is discarded.
        """
        return default

    def unwrap_or_else(self, op: Callable[[E_co], T_co]) -> T_co:
        """Return the contained ``Ok`` value or compute it from a callable.

        The callable *op* is applied to the contained ``Err`` value.
        """
        return op(self._value)

    def unwrap_or_raise(self, e: type[TBE]) -> NoReturn:
        """Return the contained ``Ok`` value or raise the provided exception.

        The exception *e* is instantiated with the ``Err`` value and raised.
        """
        raise e(self._value)

    def map(self, _op: object) -> Err[E_co]:
        """Apply *op* to the contained ``Ok`` value.

        Map a ``Result[T, E]`` to ``Result[U, E]``, leaving an ``Err`` value untouched.
        """
        return self

    async def map_async(self, _op: object) -> Err[E_co]:
        """Async version of ``map``.

        Return the ``Err`` value untouched.
        """
        return self

    def map_or(self, default: U, _op: object) -> U:
        """Apply *op* to the contained ``Ok`` value, or return *default* if ``Err``.

        Since this is ``Err``, *op* is ignored and *default* is returned.
        """
        return default

    def map_or_else(self, default_op: Callable[[], U], _op: object) -> U:
        """Apply *op* to a contained ``Ok`` value, or *default_op* to a contained ``Err``.

        Map a ``Result[T, E]`` to ``U``.
        """
        return default_op()

    def map_err(self, op: Callable[[E_co], F]) -> Err[F]:
        """Apply *op* to a contained ``Err`` value, leaving ``Ok`` untouched.

        Map a ``Result[T, E]`` to ``Result[T, F]``.
        """
        return Err(op(self._value))

    def and_then(self, _op: object) -> Err[E_co]:
        """Call *op* if the result is ``Ok``, otherwise return the ``Err`` value of *self*.

        This function can be used for control flow based on ``Result`` values.
        """
        return self

    async def and_then_async(self, _op: object) -> Err[E_co]:
        """Async version of ``and_then``.

        Return the ``Err`` value untouched.
        """
        return self

    def or_else(self, op: Callable[[E_co], Result[T_co, F]]) -> Result[T_co, F]:
        """Call *op* if the result is ``Err``, otherwise return the ``Ok`` value of *self*.

        Since this is ``Err``, *op* is called with the error value.
        """
        return op(self._value)

    def inspect(self, _op: Callable[[T_co], Any]) -> Result[T_co, E_co]:
        """Call *op* with the contained value if ``Ok``.

        Return the original result unchanged. Since this is ``Err``, *op* is not called.
        """
        return self

    def inspect_err(self, op: Callable[[E_co], Any]) -> Result[T_co, E_co]:
        """Call *op* with the contained error if ``Err``.

        Return the original result unchanged.
        """
        op(self._value)
        return self


Result: TypeAlias = Ok[T_co] | Err[E_co]
"""A simple ``Result`` type inspired by Rust.

Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
have been implemented, only the ones that make sense in the Python context.
"""

OkErr: Final = (Ok, Err)
"""A type to use in ``isinstance`` checks.

This is purely for convenience sake, as you could also just write
``isinstance(res, (Ok, Err))``.
"""


class UnwrapError(Exception):
    """Exception raised from ``.unwrap_<...>`` and ``.expect_<...>`` calls.

    The original ``Result`` can be accessed via the ``.result`` attribute, but
    this is not intended for regular use, as type information is lost:
    ``UnwrapError`` doesn't know about both ``T`` and ``E``, since it's raised
    from ``Ok()`` or ``Err()`` which only knows about either ``T`` or ``E``,
    not both.
    """

    _result: Result[object, object]

    def __init__(self, result: Result[object, object], message: str) -> None:
        self._result = result
        super().__init__(message)

    @property
    def result(self) -> Result[Any, Any]:
        """Return the original result."""
        return self._result


def as_result(
    *exceptions: type[TBE],
) -> Callable[[Callable[P, R]], Callable[P, Result[R, TBE]]]:
    """Make a decorator to turn a function into one that returns a ``Result``.

    Regular return values are turned into ``Ok(return_value)``. Raised
    exceptions of the specified exception type(s) are turned into ``Err(exc)``.
    """
    if not exceptions or not all(
        inspect.isclass(exception) and issubclass(exception, BaseException)
        for exception in exceptions
    ):
        msg = "as_result() requires one or more exception types"
        raise TypeError(msg)

    def decorator(f: Callable[P, R]) -> Callable[P, Result[R, TBE]]:
        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, TBE]:
            try:
                return Ok(f(*args, **kwargs))
            except exceptions as exc:
                return Err(exc)

        return wrapper

    return decorator


def as_async_result(
    *exceptions: type[TBE],
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[Result[R, TBE]]]]:
    """Make a decorator to turn an async function into one that returns a ``Result``.

    Regular return values are turned into ``Ok(return_value)``. Raised
    exceptions of the specified exception type(s) are turned into ``Err(exc)``.
    """
    if not exceptions or not all(
        inspect.isclass(exception) and issubclass(exception, BaseException)
        for exception in exceptions
    ):
        msg = "as_result() requires one or more exception types"
        raise TypeError(msg)

    def decorator(
        f: Callable[P, Awaitable[R]],
    ) -> Callable[P, Awaitable[Result[R, TBE]]]:
        @functools.wraps(f)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, TBE]:
            try:
                return Ok(await f(*args, **kwargs))
            except exceptions as exc:
                return Err(exc)

        return async_wrapper

    return decorator


def is_ok(result: Result[T_co, E_co]) -> TypeIs[Ok[T_co]]:
    """Check whether *result* is ``Ok`` (typeguard).

    Usage::

        r: Result[int, str] = get_a_result()
        if is_ok(r):
            r   # r is of type Ok[int]
        elif is_err(r):
            r   # r is of type Err[str]
    """
    return result.is_ok()


def is_err(result: Result[T_co, E_co]) -> TypeIs[Err[E_co]]:
    """Check whether *result* is ``Err`` (typeguard).

    Usage::

        r: Result[int, str] = get_a_result()
        if is_ok(r):
            r   # r is of type Ok[int]
        elif is_err(r):
            r   # r is of type Err[str]
    """
    return result.is_err()


def do(gen: Generator[Result[T_co, E_co], None, None]) -> Result[T_co, E_co]:
    """Do notation for Result (syntactic sugar for sequence of ``and_then()`` calls).

    Usage::

        final_result: Result[float, int] = do(
            Ok(len(x) + int(y) + 0.5)
            for x in Ok("hello")
            for y in Ok(True)
        )

    NOTE: If you exclude the type annotation e.g. ``Result[float, int]``
    your type checker might be unable to infer the return type.
    To avoid an error, you might need to help it with the type hint.
    """
    try:
        return next(gen)
    except _DoError as e:
        return cast("Err[E_co]", e.err)
    except TypeError as te:
        if "'async_generator' object is not an iterator" in str(te):
            msg = (
                "Got async_generator but expected generator."
                "See the section on do notation in the README."
            )
            raise TypeError(msg) from te
        raise


async def do_async(
    gen: Generator[Result[T_co, E_co], None, None] | AsyncGenerator[Result[T_co, E_co], None],
) -> Result[T_co, E_co]:
    """Async version of ``do()``.

    Usage::

        final_result: Result[float, int] = await do_async(
            Ok(len(x) + int(y) + z)
            for x in await get_async_result_1()
            for y in await get_async_result_2()
            for z in get_sync_result_3()
        )

    NOTE: Python makes generators async in a counter-intuitive way.

    ::

        # This is a regular generator:
        async def foo(): ...
        do(Ok(1) for x in await foo())

    ::

        # But this is an async generator:
        async def foo(): ...
        async def bar(): ...
        do(
            Ok(1)
            for x in await foo()
            for y in await bar()
        )

    We let users try to use regular ``do()``, which works in some cases
    of awaiting async values. If we hit a case like above, we raise
    an exception telling the user to use ``do_async()`` instead.
    See ``do()``.

    However, for better usability, it's better for ``do_async()`` to also accept
    regular generators, as you get in the first case::

        async def foo(): ...
        do(Ok(1) for x in await foo())

    Furthermore, neither mypy nor pyright can infer that the second case is
    actually an async generator, so we cannot annotate ``do_async()``
    as accepting only an async generator. This is additional motivation
    to accept either.
    """
    try:
        if isinstance(gen, AsyncGenerator):
            return await gen.__anext__()
        return next(gen)
    except _DoError as e:
        return cast("Err[E_co]", e.err)
