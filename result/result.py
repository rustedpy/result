from typing import Generic, TypeVar, Union, Any, Optional, cast, overload, NoReturn


T = TypeVar("T")
E = TypeVar("E")


class Ok(Generic[T]):
    """
    A value that indicates success and which stores arbitrary data for the return value.
    """

    def __init__(self, value: T) -> None:
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

    def unwrap(self) -> T:
        """
        Return the value.
        """
        return self._value

    def unwrap_or(self, _default: T) -> T:
        """
        Return the value.
        """
        return self._value


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

    def unwrap(self) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        raise UnwrapError("Called `Result.unwrap()` on an `Err` value")

    def unwrap_or(self, default: T) -> T:
        """
        Return `default`.
        """
        return default


# define Result as a generic type alias for use
# in type annotations
"""
A simple `Result` type inspired by Rust.

Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
have been implemented, only the ones that make sense in the Python context.
"""
Result = Union[Ok[T], Err[E]]


class UnwrapError(Exception):
    pass
