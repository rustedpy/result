from typing import Callable, Generic, TypeVar, Union, Any, cast, overload, NoReturn

T = TypeVar("T")  # Success type
E = TypeVar("E")  # Error type
U = TypeVar("U")
F = TypeVar("F")


class Ok(Generic[T]):
    """
    A value that indicates success and which stores arbitrary data for the return value.
    """

    @overload
    def __init__(self) -> None:
        pass

    @overload
    def __init__(self, value: T) -> None:
        self._value = value

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
        raise UnwrapError(message)

    def unwrap(self) -> T:
        """
        Return the value.
        """
        return self._value

    def unwrap_err(self) -> NoReturn:
        """
        Raise an UnwrapError since this type is `Ok`
        """
        raise UnwrapError("Called `Result.unwrap_err()` on an `Ok` value")

    def unwrap_or(self, _default: T) -> T:
        """
        Return the value.
        """
        return self._value

    def map(self, op: Callable[[T], U]) -> 'Result[U, E]':
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

    def map_err(self, op: Callable[[E], F]) -> 'Result[T, F]':
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return cast(Result[T, F], self)


class Err(Generic[E]):
    """
    A value that signifies failure and which stores arbitrary data for the error.
    """

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
        raise UnwrapError(message)

    def expect_err(self, _message: str) -> E:
        """
        Return the inner value
        """
        return self._value

    def unwrap(self) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        raise UnwrapError("Called `Result.unwrap()` on an `Err` value")

    def unwrap_err(self) -> E:
        """
        Return the inner value
        """
        return self._value

    def unwrap_or(self, default: T) -> T:
        """
        Return `default`.
        """
        return default

    def map(self, op: Callable[[T], U]) -> 'Result[U, E]':
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

    def map_err(self, op: Callable[[E], F]) -> 'Result[T, F]':
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
    pass
