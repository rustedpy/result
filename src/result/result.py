from __future__ import annotations

import functools
import inspect
import sys
from typing import (
    Any,
    Callable,
    Generic,
    NoReturn,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

if sys.version_info[:2] >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec


T = TypeVar("T", covariant=True)  # Success type
E = TypeVar("E", covariant=True)  # Error type
U = TypeVar("U")
F = TypeVar("F")
P = ParamSpec("P")
R = TypeVar("R")
TBE = TypeVar("TBE", bound=BaseException)


class Ok(Generic[T]):
    """
    A value that indicates success and which stores arbitrary data for the return value.
    """

    _value: T
    __match_args__ = ("value",)
    __slots__ = ("_value",)

    @overload
    def __init__(self) -> None:
        ...  # pragma: no cover

    @overload
    def __init__(self, value: T) -> None:
        ...  # pragma: no cover

    def __init__(self, value: Any = True) -> None:
        self._value = value

    def __repr__(self) -> str:
        return "Ok({})".format(repr(self._value))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Ok) and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self._value))

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

    def ok(self) -> T:
        """
        Return the value.
        """
        return self._value

    def err(self) -> None:
        """
        Return `None`.
        """
        return None

    @property
    def value(self) -> T:
        """
        Return the inner value.
        """
        return self._value

    def expect(self, _message: str) -> T:
        """
        Return the value.
        """
        return self._value

    def expect_err(self, message: str) -> NoReturn:
        """
        Raise an UnwrapError since this type is `Ok`
        """
        raise UnwrapError(self, message)

    def unwrap(self) -> T:
        """
        Return the value.
        """
        return self._value

    def unwrap_err(self) -> NoReturn:
        """
        Raise an UnwrapError since this type is `Ok`
        """
        raise UnwrapError(self, "Called `Result.unwrap_err()` on an `Ok` value")

    def unwrap_or(self, _default: U) -> T:
        """
        Return the value.
        """
        return self._value

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        """
        Return the value.
        """
        return self._value

    def map(self, op: Callable[[T], U]) -> Result[U, E]:
        """
        The contained result is `Ok`, so return `Ok` with original value mapped to
        a new value using the passed in function.
        """
        return Ok(op(self._value))

    def map_or(self, default: U, op: Callable[[T], U]) -> U:
        """
        The contained result is `Ok`, so return the original value mapped to a new
        value using the passed in function.
        """
        return op(self._value)

    def map_or_else(
        self,
        default_op: Callable[[], U],
        op: Callable[[T], U]
    ) -> U:
        """
        The contained result is `Ok`, so return original value mapped to
        a new value using the passed in `op` function.
        """
        return op(self._value)

    def map_err(self, op: Callable[[E], F]) -> Result[T, F]:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return cast(Result[T, F], self)


class Err(Generic[E]):
    """
    A value that signifies failure and which stores arbitrary data for the error.
    """

    __match_args__ = ("value",)
    __slots__ = ("_value",)

    def __init__(self, value: E) -> None:
        self._value = value

    def __repr__(self) -> str:
        return "Err({})".format(repr(self._value))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Err) and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, self._value))

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

    def ok(self) -> None:
        """
        Return `None`.
        """
        return None

    def err(self) -> E:
        """
        Return the error.
        """
        return self._value

    @property
    def value(self) -> E:
        """
        Return the inner value.
        """
        return self._value

    def expect(self, message: str) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        raise UnwrapError(self, message)

    def expect_err(self, _message: str) -> E:
        """
        Return the inner value
        """
        return self._value

    def unwrap(self) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        raise UnwrapError(self, "Called `Result.unwrap()` on an `Err` value")

    def unwrap_err(self) -> E:
        """
        Return the inner value
        """
        return self._value

    def unwrap_or(self, default: U) -> U:
        """
        Return `default`.
        """
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        """
        The contained result is ``Err``, so return the result of applying
        ``op`` to the error value.
        """
        return op(self._value)

    def map(self, op: Callable[[T], U]) -> Result[U, E]:
        """
        Return `Err` with the same value
        """
        return cast(Result[U, E], self)

    def map_or(self, default: U, op: Callable[[T], U]) -> U:
        """
        Return the default value
        """
        return default

    def map_or_else(
        self,
        default_op: Callable[[], U],
        op: Callable[[T], U]
    ) -> U:
        """
        Return the result of the default operation
        """
        return default_op()

    def map_err(self, op: Callable[[E], F]) -> Result[T, F]:
        """
        The contained result is `Err`, so return `Err` with original error mapped to
        a new value using the passed in function.
        """
        return Err(op(self._value))


# define Result as a generic type alias for use
# in type annotations
"""
A simple `Result` type inspired by Rust.
Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
have been implemented, only the ones that make sense in the Python context.
"""
Result = Union[Ok[T], Err[E]]

"""
A type to use in `isinstance` checks.
This is purely for convenience sake, as you could also just write `isinstance(res, (Ok, Err))
"""
OkErr = (Ok, Err)


class UnwrapError(Exception):
    """
    Exception raised from ``.unwrap_<...>`` and ``.expect_<...>`` calls.

    The original ``Result`` can be accessed via the ``.result`` attribute, but
    this is not intended for regular use, as type information is lost:
    ``UnwrapError`` doesn't know about both ``T`` and ``E``, since it's raised
    from ``Ok()`` or ``Err()`` which only knows about either ``T`` or ``E``,
    not both.
    """

    _result: Result[Any, Any]

    def __init__(self, result: Result[Any, Any], message: str) -> None:
        self._result = result
        super().__init__(message)

    @property
    def result(self) -> Result[Any, Any]:
        """
        Returns the original result.
        """
        return self._result


def as_result(
    *exceptions: Type[TBE],
) -> Callable[[Callable[P, R]], Callable[P, Result[R, TBE]]]:
    """
    Make a decorator to turn a function into one that returns a ``Result``.

    Regular return values are turned into ``Ok(return_value)``. Raised
    exceptions of the specified exception type(s) are turned into ``Err(exc)``.
    """
    if not exceptions or not all(
        inspect.isclass(exception) and issubclass(exception, BaseException)
        for exception in exceptions
    ):
        raise TypeError("as_result() requires one or more exception types")

    def decorator(f: Callable[P, R]) -> Callable[P, Result[R, TBE]]:
        """
        Decorator to turn a function into one that returns a ``Result``.
        """

        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, TBE]:
            try:
                return Ok(f(*args, **kwargs))
            except exceptions as exc:
                return Err(exc)

        return wrapper

    return decorator
