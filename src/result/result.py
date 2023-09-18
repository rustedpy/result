from __future__ import annotations

import functools
import inspect
import sys
from warnings import warn
from typing import (
    Any,
    Awaitable,
    Callable,
    Final,
    Generic,
    Literal,
    NoReturn,
    Type,
    TypeVar,
    Union,
)
from collections.abc import Sequence

if sys.version_info >= (3, 10):
    from typing import ParamSpec, TypeAlias, TypeGuard
else:
    from typing_extensions import ParamSpec, TypeAlias, TypeGuard

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self


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

    __match_args__ = ("ok_value",)
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def __repr__(self) -> str:
        return "Ok({})".format(repr(self._value))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Ok) and self._value == other._value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self._value))

    def is_ok(self) -> Literal[True]:
        return True

    def is_err(self) -> Literal[False]:
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

        @deprecated Use `ok_value` or `err_value` instead. This method will be
        removed in a future version.
        """
        warn(
            "Accessing `.value` on Result type is deprecated, please use "
            + "`.ok_value` or '.err_value' instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._value

    @property
    def ok_value(self) -> T:
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

    def unwrap_or_else(self, op: object) -> T:
        """
        Return the value.
        """
        return self._value

    def unwrap_or_raise(self, e: object) -> T:
        """
        Return the value.
        """
        return self._value

    def map(self, op: Callable[[T], U]) -> Ok[U]:
        """
        The contained result is `Ok`, so return `Ok` with original value mapped to
        a new value using the passed in function.
        """
        return Ok(op(self._value))

    def map_or(self, default: object, op: Callable[[T], U]) -> U:
        """
        The contained result is `Ok`, so return the original value mapped to a new
        value using the passed in function.
        """
        return op(self._value)

    def map_or_else(self, default_op: object, op: Callable[[T], U]) -> U:
        """
        The contained result is `Ok`, so return original value mapped to
        a new value using the passed in `op` function.
        """
        return op(self._value)

    def map_err(self, op: object) -> Ok[T]:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return self

    def and_then(self, op: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """
        The contained result is `Ok`, so return the result of `op` with the
        original value passed in
        """
        return op(self._value)

    def or_else(self, op: object) -> Ok[T]:
        """
        The contained result is `Ok`, so return `Ok` with the original value
        """
        return self

    # piping
    def __matmul__(self, op: Callable[[T], U]) -> Result[U, Exception]:
        """
        Piping operator, which returns Err on exception encounter.

        Example:
            res: Result = Ok(2) @ (lambda x: x**2) @ (lambda x: x+1)
            assert res.unwrap() == 5
        """

        try:
            return Ok(op(self._value))
        except Exception as exc:
            fnc = op.__name__
            lastVal = self.ok_value
            exc.args = tuple([a for a in exc.args] + [f"{fnc=}", f"{lastVal=}"])
            return Err(exc)

    async def __ge__(self, op: Callable[[T], Awaitable[U]]) -> Result[U, Exception]:
        """
        Piping for async functions.
        The operator CANNOT chain without await

        Example:
            async def foo(x): return x+1
            x = Ok(2) >= foo
            result = await x
            assert result == Ok(3)

            ## can be inlined with parentheses, but make sure to LEAVE SPECE AFTER AWAIT
            y = await (await ( Ok(2) >= foo ) @ (lambda x: x+1) >= foo)
            assert y == Ok(5)
        """

        try:
            result = await op(self._value)
            return Ok(result)
        except Exception as exc:
            fnc = op.__name__
            lastVal = self.ok_value
            exc.args = tuple([a for a in exc.args] + [f"{fnc=}", f"{lastVal=}"])
            return Err(exc)

    def __mod__(self, op: Callable[[T], bool]) -> Result[T, FilterException]:
        """
        pipe filter; TRUE => keep the Ok value

        filtered values are treated as errors
        see below the FilterException

        Example:
            res: Result = Ok(2) @ (lambda x: x**2) % (lambda x: x>10) @ (lambda x: x+1)
            assert isinstance(res, Err)
            assert res._value._result == Ok(4)
                ## traceback on where it stopped in the chain
            assert res. (..traceback..) .`reason` == 'filtered out'
                ## mark, that it was deliberately filtered
        """

        if op(self._value):
            return self
        else:
            err = FilterException(self, op.__name__)
            return Err(err)

    def __or__(self, other: Result[Any, Any]) -> MultiResult:
        """
        Joining operator.
        If not specified manually, the Result needs to initialize MultiResult instance.

        Example:
            mres: MultiResult = Ok(2) | Ok(12)
            assert tuple(mres.results) == tuple([ Ok(2) , Ok(12) ])
        """
        return MultiResult(self, other)


class Err(Generic[E]):
    """
    A value that signifies failure and which stores arbitrary data for the error.
    """

    __match_args__ = ("err_value",)
    __slots__ = ("_value",)

    def __init__(self, value: E) -> None:
        self._value = value

    def __repr__(self) -> str:
        return "Err({})".format(repr(self._value))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Err) and self._value == other._value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, self._value))

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
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

        @deprecated Use `ok_value` or `err_value` instead. This method will be
        removed in a future version.
        """
        warn(
            "Accessing `.value` on Result type is deprecated, please use "
            + "`.ok_value` or '.err_value' instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._value

    @property
    def err_value(self) -> E:
        """
        Return the inner value.
        """
        return self._value

    def expect(self, message: str) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        exc = UnwrapError(
            self,
            f"{message}: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

    def expect_err(self, _message: str) -> E:
        """
        Return the inner value
        """
        return self._value

    def unwrap(self) -> NoReturn:
        """
        Raises an `UnwrapError`.
        """
        exc = UnwrapError(
            self,
            f"Called `Result.unwrap()` on an `Err` value: {self._value!r}",
        )
        if isinstance(self._value, BaseException):
            raise exc from self._value
        raise exc

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

    def unwrap_or_raise(self, e: Type[TBE]) -> NoReturn:
        """
        The contained result is ``Err``, so raise the exception with the value.
        """
        raise e(self._value)

    def map(self, op: object) -> Err[E]:
        """
        Return `Err` with the same value
        """
        return self

    def map_or(self, default: U, op: object) -> U:
        """
        Return the default value
        """
        return default

    def map_or_else(self, default_op: Callable[[], U], op: object) -> U:
        """
        Return the result of the default operation
        """
        return default_op()

    def map_err(self, op: Callable[[E], F]) -> Err[F]:
        """
        The contained result is `Err`, so return `Err` with original error mapped to
        a new value using the passed in function.
        """
        return Err(op(self._value))

    def and_then(self, op: object) -> Err[E]:
        """
        The contained result is `Err`, so return `Err` with the original value
        """
        return self

    def or_else(self, op: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """
        The contained result is `Err`, so return the result of `op` with the
        original value passed in
        """
        return op(self._value)

    # piping
    def __matmul__(self, op: Callable[[T], U]) -> Result[U, E]:
        """
        Piping operator,
        already an Error, so just returns self.

        Example:
            assert Err(2) @ (lambda x:x**2) == Err(2)
        """
        return self

    async def __ge__(self, op: Callable[[T], Awaitable[U]]) -> Result[U, E]:
        """
        Piping for async functions.
        Just returns self, but needs to be awaited to have the same behavoiur as the Ok variant.
        The operator CANNOT chain without await

        Example:
            async def foo(x): return x+1
            x = Err('foo') >= foo
            result = await x
            assert result == Err('foo')

            ## can be inlined with parentheses, but make sure to LEAVE SPECE AFTER AWAIT
            y = await (await ( Err('bar') >= foo ) @ (lambda x: x+1) >= foo)
            assert y == Err('bar')

        """
        return self

    def __mod__(self, op: Callable[[T], bool]) -> Result[T, E]:
        """
        pipe filter.
        filtered values are treaded as errors
        returns self, since it's already an error
        """
        return self

    def __or__(self, other: Result[Any, Any]) -> MultiResult:
        """
        Joining operator.
        If not specified manually, the Result needs to initialize MultiResult instance.

        Example:
            mres: MultiResult = Ok(2) | Ok(12)
            assert tuple(mres.results) == tuple([ Ok(2) , Ok(12) ])
        """
        return MultiResult(self, other)


class MultiResult:
    """
    A Result class for storing (joining) multiple results to use in multivariate functions.
    The multivariate operator has the lower priority so it gets evaluated AFTER:
        - single argument functions ( Result @ fnc -> Result )
        - result joining ( Result | Result -> MultiResult )
        - finally then: ( MultiResult > multivarfnc -> Result )
        - similarly for async: ( MultiResult >= async multifnc -> coroutine )
            ... this needs to be awaited
    """

    __match_args__ = ("results",)
    __slots__ = ("results",)

    def __init__(self, *results: Result[Any, Any]) -> None:
        self.results = list(results)

    def __repr__(self) -> str:
        results = [str(res) for res in self.results]
        return "MultiResult(" + ",".join(results) + ")"

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, MultiResult)
            and (n := len(self.results)) == len(other.results)
            and all(self.results[i] == other.results[i] for i in range(n))
        )

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        """
        hash by repr if normal fails
        """
        try:
            return hash(tuple(hash(res) for res in self.results))
        except Exception:
            return hash(repr(self))

    def is_ok(self) -> bool:
        return all([res.is_ok() for res in self.results])

    def is_err(self) -> bool:
        return not self.is_ok()

    def ok(self) -> tuple[Any, ...]:
        """
        Return the ok values or Nones for errors.

        Example:
            assert ( Ok(2) | Ok('foobar') | Err('magnets')  ).ok() == (2,'foobar',None)
        """
        return tuple(res.ok() for res in self.results)

    def err(self) -> tuple[Any, ...]:
        """
        returns the error values or Nones for oks.

        Example:
            assert ( Ok(2) | Ok('foobar') | Err('magnets')  ).err() == (None,None,'magnets')
        """
        return tuple(res.err() for res in self.results)

    def expect(self, _message: str) -> tuple[Any, ...]:
        """
        Attempts to return tuple of values.

        Raises:
            UnwrapError with `_message` if any element fails
        """
        return tuple(res.expect(_message) for res in self.results)

    def expect_err(self, _message: str) -> Exception:
        """
        If successfully unwraps, raises.
        Otherwise returns the (first?) error.
        """
        try:
            val = self.unwrap()
            raise UnwrapError(Ok(val), _message)
        except Exception as e:
            return e

    def unwrap(self) -> tuple[Any, ...]:
        """
        Attempts to return tuple of values.

        Raises:
            UnwrapError with `_message` if any element fails
        """
        return tuple(res.unwrap() for res in self.results)

    def unwrap_error(self) -> tuple[Any, ...]:
        if self.is_ok():
            raise UnwrapError(
                Ok(self.unwrap()), "Called `Result.unwrap_err()` on an `Ok` value"
            )
        return self.err()

    def unwrap_or(self, _default: Sequence[Any]) -> tuple[Any, ...]:
        """
        Tries to unwrap as much as possible, returns relevant `_default` on partial fails.
        `_default` needs to be at least the result length.

        Example:
            multi = Ok(3) | Err('foo')
            assert multi.unwrap_or( [42, 69, 13,14,15,...] ) == (3,69)
        """
        return tuple(res.unwrap_or(_default[i]) for i, res in enumerate(self.results))

    def unwrap_or_else(
        self, op: Callable[[Sequence[Result[Any, Any]]], U]
    ) -> tuple[Any, ...] | U:
        """
        Tries to unwrap, returns relevant `op` on fail.
        `op` takes sequence of results as argument.

        Example:
            def _log_errors(results) -> None:
                log([f'unwrap_fail, {res.err()}' for res in results if res.is_err()])
            multi = Ok(3) | Err('foo')
            assert multi.unwrap_or( log_errors ) == None
        """
        if self.is_ok():
            return self.unwrap()
        else:
            return op(self.results)

    def unwrap_or_raise(self, e: Type[TBE]) -> tuple[Any, ...]:
        """
        Return the value.
        if any element fails, it raises according to its error value.
        """
        return tuple(res.unwrap_or_raise(e) for res in self.results)

    def map(self, op: Callable[..., U]) -> Result[U, Exception]:
        """
        unwraps and maps

        """
        try:
            return Ok(op(*self.unwrap()))
        except Exception as e:
            return Err(e)

    def map_or(self, default: U, op: Callable[..., U]) -> U:
        """
        Tries to map, otherwise returns the default object.
        """
        if self.is_ok():
            return op(*self.unwrap())
        else:
            return default

    def map_or_else(self, default_op: Callable[[], U], op: Callable[..., U]) -> U:
        """
        Tries to map, otherwise performs and returns the default `op`.
        """
        if self.is_ok():
            return op(*self.unwrap())
        else:
            return default_op()

    def map_err(self, op: Callable[[Sequence[Any]], F]) -> Result[tuple[Any, ...], F]:
        """
        Creates Result from the MultiResult.
        This operation joins several results into a tuple one.
        If no error is present, turn into unwrapped Ok.
        If any error is present, turn into simple error.
        """
        if self.is_err():
            return Err(op(self.err()))
        else:
            return Ok(self.unwrap())

    def or_else(self, op: Callable[[Self], Self]) -> Self:
        """
        this operation ensures that the output is OkMultiResult
        tries to return self if its ok
        otherwise calls and returns the multiresult from fnc
        """
        if self.is_ok():
            return self
        else:
            return op(self)

    # piping
    def __or__(self, result: Result[U, E]) -> Self:
        """
        operator that appends new result to the multiresult list

        Example:
            multires: MultiResult = Ok(12)\
                @ (lambda x:x-10) | Ok('hello') | Ok([1,2,3]) @ (lambda x:sum(x))

            assert multires.unwrap() == (2, 'hello', 6)
            assert multires.ok()     == (2, 'hello', 6)
            assert multires.err()    == (None,None,None)
        """
        self.results += [result]
        return self

    def __gt__(self, op: Callable[..., U]) -> Result[U, Exception]:
        """
        operator which performs mapping of internal vals through the `op`
        expects sinngular return value

        Example:
            res: Result = Ok(1) | Ok(2) > (lambda x,y: x+y)
            assert res.unwrap() == 3

            res2: Result = Ok(1) | Err(exc) > (lambda x,y: ...)
            assert isinstance(res2, Err)
        """
        try:
            vals = [res.unwrap() for res in self.results]
            return Ok(op(*vals))
        except Exception:
            errmsg = "err_elements:" + ", ".join(
                [str(res) for res in self.results if res.is_err()]
            )
            fnc = op.__name__
            errlist = ["erroneous input", f"{fnc=}", errmsg]
            return Err(Exception(*errlist))

    async def __ge__(self, op: Callable[..., Awaitable[U]]) -> Result[U, Exception]:
        """
        async pipe
        operator which performs mapping of internal vals through the `op`
        The operator CANNOT chain without await

        Example:
            async def foo(x,y): return x*y
            res = await(
                Ok(2) @ (lambda x: x*2)
                | Ok(4) @ (lambda x: x-1)
                >= foo
                )
            assert res == Ok(12)
        """
        try:
            vals = [res.unwrap() for res in self.results]
            return Ok(await op(*vals))
        except Exception:
            errmsg = "err_elements:" + ", ".join(
                [str(res) for res in self.results if res.is_err()]
            )
            fnc = op.__name__
            errlist = ["erroneous input", f"{fnc=}", errmsg]
            return Err(Exception(*errlist))


# define Result as a generic type alias for use
# in type annotations
"""
A simple `Result` type inspired by Rust.
Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
have been implemented, only the ones that make sense in the Python context.
"""
Result: TypeAlias = Union[Ok[T], Err[E]]

"""
A type to use in `isinstance` checks.
This is purely for convenience sake, as you could also just write `isinstance(res, (Ok, Err))
"""
OkErr: Final = (Ok, Err)


# errors and exceptions


class UnwrapError(Exception):
    """
    Exception raised from ``.unwrap_<...>`` and ``.expect_<...>`` calls.

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
        """
        Returns the original result.
        """
        return self._result


class FilterException(Exception):
    """
    Exception raised from filter pipe.
    `function` > the name of the filter function

    The original ``Result`` can be accessed via the ``.result`` attribute, but
    this is not intended for regular use, as type information is lost:
    ``UnwrapError`` doesn't know about both ``T`` and ``E``, since it's raised
    from ``Ok()`` or ``Err()`` which only knows about either ``T`` or ``E``,
    not both.
    """

    __match_args__ = ("function",)
    __slots__ = ("function",)

    _result: Result[object, object]
    function: str

    def __init__(self, result: Result[object, object], function_name: str, *message: str) -> None:
        super().__init__(f"Filtered out by `{function_name}` function.", *message)
        self._result = result
        self.function = function_name

    @property
    def result(self) -> Result[Any, Any]:
        """
        Returns the original result.
        """
        return self._result

    def __repr__(self) -> str:
        return f"Filtered by `{self.function}` function."


# wrappers


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


def as_async_result(
    *exceptions: Type[TBE],
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[Result[R, TBE]]]]:
    """
    Make a decorator to turn an async function into one that returns a ``Result``.
    Regular return values are turned into ``Ok(return_value)``. Raised
    exceptions of the specified exception type(s) are turned into ``Err(exc)``.
    """
    if not exceptions or not all(
        inspect.isclass(exception) and issubclass(exception, BaseException)
        for exception in exceptions
    ):
        raise TypeError("as_result() requires one or more exception types")

    def decorator(
        f: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[Result[R, TBE]]]:
        """
        Decorator to turn a function into one that returns a ``Result``.
        """

        @functools.wraps(f)
        async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[R, TBE]:
            try:
                return Ok(await f(*args, **kwargs))
            except exceptions as exc:
                return Err(exc)

        return async_wrapper

    return decorator


def is_ok(result: Result[T, E]) -> TypeGuard[Ok[T]]:
    """A typeguard to check if a result is an Ok

    Usage:
    >>> r: Result[int, str] = get_a_result()
    >>> if is_ok(r):
    >>>     r   # r is of type Ok[int]
    >>> elif is_err(r):
    >>>     r   # r is of type Err[str]
    """
    return result.is_ok()


def is_err(result: Result[T, E]) -> TypeGuard[Err[E]]:
    """A typeguard to check if a result is an Err

    Usage:
    >>> r: Result[int, str] = get_a_result()
    >>> if is_ok(r):
    >>>     r   # r is of type Ok[int]
    >>> elif is_err(r):
    >>>     r   # r is of type Err[str]
    """
    return result.is_err()
