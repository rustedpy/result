# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
from typing import Generic, TypeVar, Union, Any, Optional, cast, overload


E = TypeVar("E")
T = TypeVar("T")
A = TypeVar("A")


class Result(Generic[E, T]):
    """
    A simple `Result` type inspired by Rust.

    Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
    have been implemented, only the ones that make sense in the Python context.
    """
    def __init__(self, is_ok, value, force=False):
        # type: (bool, Union[E, T], bool) -> None
        """Do not call this constructor, use the Ok or Err class methods instead.

        There are no type guarantees on the value if this is called directly.

        Args:
            is_ok: If this represents an ok result
            value: The value inside the result
            force: Force creation of the object. This is false by default to prevent accidentally
                creating instance of a Result in an unsafe way.
        """
        if force is not True:
            raise RuntimeError("Don't instantiate a Result directly. "
                               "Use the Ok(value) and Err(error) class methods instead.")
        else:
            self._is_ok = is_ok
            self._value = value

    def __eq__(self, other):
        # type: (Any) -> bool
        return (self.__class__ == other.__class__ and
                self.is_ok() == cast(Result, other).is_ok() and
                self._value == other._value)

    def __ne__(self, other):
        # type: (Any) -> bool
        return not (self == other)

    def __hash__(self):
        # type: () -> int
        return hash((self.is_ok(), self._value))

    def __repr__(self):
        # type: () -> str
        if self.is_ok():
            return str("Ok({})").format(repr(self._value))
        else:
            return str("Err({})").format(repr(self._value))

    @classmethod
    @overload
    def Ok(cls):
        # type: () -> Result[E, bool]
        pass

    @classmethod
    @overload
    def Ok(cls, value):
        # type: (T) -> Result[E, T]
        pass

    @classmethod
    def Ok(cls, value=True):
        # type: (Any) -> Result[E, Any]
        return cls(is_ok=True, value=value, force=True)

    @classmethod
    def Err(cls, error):
        # type: (E) -> Result[E, T]
        return cls(is_ok=False, value=error, force=True)

    def is_ok(self):
        # type: () -> bool
        return self._is_ok

    def is_err(self):
        # type: () -> bool
        return not self._is_ok

    def ok(self):
        # type: () -> Optional[T]
        """
        Return the value if it is an `Ok` type. Return `None` if it is an `Err`.
        """
        return cast(T, self._value) if self.is_ok() else None

    def err(self):
        # type: () -> Optional[E]
        """
        Return the error if this is an `Err` type. Return `None` otherwise.
        """
        return cast(E, self._value) if self.is_err() else None

    @property
    def value(self):
        # type: () -> Union[E, T]
        """
        Return the inner value. This might be either the ok or the error type.
        """
        return self._value

    # TODO: Implement __iter__ for destructuring


@overload
def Ok():
    # type: () -> Result[E, bool]
    pass


@overload
def Ok(value):
    # type: (T) -> Result[E, T]
    pass


def Ok(value=True):
    # type: (Any) -> Result[E, Any]
    """
    Shortcut function to create a new Result.
    """
    return Result.Ok(value)


def Err(error):
    # type: (E) -> Result[E, T]
    """
    Shortcut function to create a new Result.
    """
    return Result.Err(error)
