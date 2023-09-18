from __future__ import annotations

from typing import Callable, Sequence, Any, Union

import pytest

from result import (
    Err,
    Ok,
    OkErr,
    Result,
    UnwrapError,
    MultiResult,
    FilterException,
)


def test_MultiResult_factories() -> None:
    x = Ok(1)
    y = Ok(2)
    z = Ok([1, 2, 3])
    instance = x | y | z

    assert instance.unwrap() == (1, 2, [1, 2, 3])
    assert instance.expect("errors present") == (1, 2, [1, 2, 3])
    assert instance.is_ok()


def test_eq() -> None:
    assert MultiResult(Ok(1), Ok("foo")) == MultiResult(Ok(1), Ok("foo"))
    assert MultiResult(Err(1), Ok([1, 2, 3])) == MultiResult(Err(1), Ok([1, 2, 3]))
    assert MultiResult(Ok(1)) != MultiResult(Err(1))
    assert MultiResult(Ok({"foo": "bar", 3: [1, 2, 3]})) == MultiResult(
        Ok({"foo": "bar", 3: [1, 2, 3]})
    )


def test_hash() -> None:
    # lists, sets, dicts ... are unhashable!
    hash1 = hash(MultiResult(Ok(1), Ok(1.1), Err("foo")))
    hash2 = hash(MultiResult(Ok(1), Ok(1.1), Err("foo")))
    assert hash1 == hash2

    hash3 = hash(MultiResult(Ok([1, 2, 3]), Ok({1, 2, 3}), Err("foo")))
    hash4 = hash(MultiResult(Ok([1, 2, 3]), Ok({1, 2, 3}), Err("foo")))
    assert hash3 == hash4


def test_repr() -> None:
    """
    ``repr()`` returns valid code if the wrapped value's ``repr()`` does as well.
    """
    o = Ok(123)
    n = Err(-1)
    mr = MultiResult(o, n)

    assert repr(mr) == "MultiResult(Ok(123),Err(-1))"
    assert mr == eval(repr(mr))

    mr = mr | Ok({"foo": [1, 2, 3], 3: {3: 1, 2: 9}})  # | Err(Exception("foobar"))
    # exception fails test
    assert mr == eval(repr(mr))


def test_ok_err_values() -> None:
    x = Ok("haha")
    y = Err("boo")
    mr = x | y

    assert mr.ok() == ("haha", None)
    assert mr.err() == (None, "boo")
    assert not mr.is_ok()
    assert mr.is_err()
    # at least 1 error


def test_err_value_is_exception() -> None:
    err = Err(ValueError("Some Error"))
    mr = MultiResult(err)

    assert mr.is_err()

    with pytest.raises(UnwrapError):
        mr.unwrap()

    try:
        mr.unwrap()
    except UnwrapError as e:
        cause = e.__cause__
        assert isinstance(cause, ValueError)


def test_filterexception_traceback() -> None:
    def foofilter(x: int) -> bool:
        return x > 0

    err = Ok(0) % foofilter

    assert err.is_err()
    exc = err.err()
    assert isinstance(exc, FilterException)

    fname = exc.function
    assert fname == "foofilter"


def test_unwrap() -> None:
    o = Ok("yay")
    n = Err("nay")
    z = Ok("foo")
    mrbad = o | n | z
    mrok = o | z

    assert mrok.unwrap() == ("yay", "foo")
    with pytest.raises(UnwrapError):
        mrbad.unwrap()


def test_unwrap_or() -> None:
    o = Ok("yay")
    n = Err("nay")
    z = Ok([1, 2, 3])
    mr = o | n | z

    defaults = ["some_default", "another_default", "some_default"]

    unwrap = mr.unwrap_or(defaults)
    assert unwrap[0] == "yay"
    assert unwrap[1] == "another_default"
    assert unwrap[2] == [1, 2, 3]


def test_unwrap_or_else() -> None:
    o = Ok("yay")
    n = Err("nay")
    z = Ok({1: 11, 2: "hello", 3: [1, 2, 3]})
    mr = o | n | z

    def default_op(results: Sequence[Result[Any, Any]]) -> list[Any]:
        out = []
        for res in results:
            if res.is_ok():
                out += [res.ok()]
            else:
                out += [str(res.err()).upper()]
        return out

    unwrap = mr.unwrap_or_else(default_op)
    assert unwrap[0] == "yay"
    assert unwrap[1] == "NAY"
    assert unwrap[2] == {1: 11, 2: "hello", 3: [1, 2, 3]}


def test_unwrap_or_raise() -> None:
    o = Ok("yay")
    n = Err("nay")
    z = Ok("foo")
    mrbad = o | n | z
    mrok = o | z

    assert mrok.unwrap_or_raise(ValueError) == ("yay", "foo")

    with pytest.raises(ValueError) as exc_info:
        mrbad.unwrap_or_raise(ValueError)
    assert exc_info.value.args == ("nay",)


def test_map() -> None:
    o = Ok("yay")
    n = Err("nay")
    z = Ok([1, 2, 3])

    def mysum(x: list[int]) -> int:
        return sum(x)

    assert (o @ str.upper).ok() == "YAY"
    assert (n @ str.upper).err() == "nay"
    assert (z @ mysum).ok() == 6

    num = Ok(3)
    errnum = Err(2)

    assert (num @ str).ok() == "3"
    assert (errnum @ str).err() == 2

    mrbad = o | n | z | num | errnum
    resbad = mrbad > (lambda x: x)
    assert resbad.is_err()

    def fnc(o: str, z: list[int], num: int) -> str:
        return str(o) + str(sum(z)) + str(num)

    res = o | z | num > fnc
    assert res.is_ok()
    assert res.unwrap() == "yay63"


def test_map_or() -> None:
    o = Ok("yay")
    n = Err("nay")
    mrbad = o | n

    alternative = Ok("haystack")

    def fnc(o: str, n: int) -> Ok[str]:
        return Ok("".join([o, str(n)]))

    assert mrbad.map_or(alternative, fnc).ok() == "haystack"

    num = Ok(3)
    mrgood = o | num
    assert mrgood.map_or(alternative, fnc).ok() == "yay3"


def test_map_or_else() -> None:
    o = Ok("yay")
    n = Err("nay")
    mrbad = o | n

    def default_op() -> str:
        return "baad"

    def fnc(o: str, n: str) -> str:
        return "".join((o, str(n)))

    assert mrbad.map_or_else(default_op, fnc) == "baad"

    num = Ok(3)
    mrgood = o | num

    assert mrgood.map_or_else(default_op, fnc) == "yay3"


def test_and_then() -> None:
    """MultiResult doesnt have and_then.
    its purpose is to be consumed."""


def test_or_else() -> None:
    def fix_mr(mr: MultiResult) -> MultiResult:
        return MultiResult(
            *[
                res if res.is_ok() else Ok(res._value + i + 2)
                for i, res in enumerate(mr.results)
            ]
        )

    x = Ok(2).or_else(sq).or_else(sq)  # good
    y = Ok(2).or_else(to_err).or_else(sq)  # good

    assert x.is_ok()
    assert y.is_ok()

    mrgood = x | y
    mrres = mrgood.or_else(fix_mr)
    unwrap = mrres.unwrap()
    assert unwrap == (2, 2)

    w = Err(3).or_else(sq).or_else(to_err)  # good
    z = Err(3).or_else(to_err).or_else(to_err)  # bad

    mrbad = x.and_then(sq) | w | z
    mrres2 = mrbad.or_else(fix_mr)
    unwrap2 = mrres2.unwrap()
    assert unwrap2 == (4, 9, 7)


def test_isinstance_result_type() -> None:
    def add1(x: int) -> int:
        return x + 1

    def div2(x: int) -> float:
        return x / 2

    o = Ok(2) @ add1 @ div2
    n = Err(1) @ add1
    assert isinstance(o, OkErr)
    assert isinstance(n, OkErr)


def test_error_context() -> None:
    n = Err("nay")
    m = Err(13)
    o = Err(Exception("foo"))
    mr = n | m | o

    with pytest.raises(UnwrapError) as exc_info:
        mr.unwrap()
    exc = exc_info.value
    assert exc.result is n
    # MultiResult unwrap raises the first encountered exception


def test_slots() -> None:
    """
    Ok and Err have slots, so assigning arbitrary attributes fails.
    """
    mr = MultiResult()
    with pytest.raises(AttributeError):
        mr.some_arbitrary_attribute = 1  # type: ignore[attr-defined]


def test_function_piping() -> None:
    def good(value: int) -> int:
        return value

    def bad(value: int) -> int:
        raise ValueError

    good_result = Ok(123) @ good
    bad_result = Ok(123) @ bad

    assert isinstance(good_result, Ok)
    assert good_result.unwrap() == 123
    assert isinstance(bad_result, Err)
    assert isinstance(bad_result.unwrap_err(), ValueError)


def test_piping_type_checking_simple() -> None:
    def f(a: int) -> int:
        return a

    res: Result[int, Exception]
    res = Ok(123) @ f  # No mypy error here. But piping assumes general Exceptions
    #    --> something to make better
    assert res.ok() == 123


def test_compound_types() -> None:
    def f(a: int, b: int) -> list[int]:
        out = [b * i for i in range(a)]
        return out

    res: Result[list[int], Exception]
    res = Ok(5) | Ok(10) > f

    assert isinstance(res, Ok)
    assert res.ok() == [0, 10, 20, 30, 40]


def test_filtering() -> None:
    from result import FilterException

    x1 = Ok(2)
    x2 = Ok(3)
    y1 = x1 @ add1 % iseven
    y2 = x2 @ add1 % iseven

    assert isinstance(y1, Err)
    assert isinstance(y2, Ok)
    assert y2.ok() == 4

    with pytest.raises(FilterException):
        raise y1.err()


def test_generators() -> None:
    xs = [Ok(i) @ square @ add1 @ mod2 @ add2 @ square for i in range(10)]

    mr = MultiResult(*xs)
    assert mr.is_ok()

    unwrap = mr.unwrap()
    assert unwrap == (9, 4, 9, 4, 9, 4, 9, 4, 9, 4)


def test_generator_with_filter() -> None:
    xs = [
        res
        for i in range(10)
        if (
            res := Ok(i)
            @ add2
            @ cube
            % iseven  # filter -> only even (i+2)**3 will remain
            @ mod2
            @ add2
            @ add2
            @ square
            % ge10  # filter -> only those <= 10 here will remain
            @ sub1
            @ cube
        ).is_ok()  # the final check which will remove all Errors
    ]

    mr = MultiResult(*xs)
    assert mr.is_ok()

    unwrap = mr.unwrap()
    assert unwrap == (3375, 3375, 3375, 3375, 3375)


def test_larger_multivar_function() -> None:
    """
    do not remove the errors apriori at this time
    """
    from math import isclose

    xs = [Ok(i) @ add1 @ square % ge10 @ div1 @ add1 @ cube for i in range(10)]

    mr = MultiResult(*xs)
    assert mr.is_err()

    clean_xs = [x for x in xs if x.is_ok()]
    mrgood = MultiResult(*clean_xs)
    assert mrgood.is_ok()
    unwrap = mrgood.unwrap()

    assert len(unwrap) == 7

    def mysum(*x: float) -> float:
        return sum(x)

    res: Result[float, Exception]
    res = mrgood > mysum
    assert res.is_ok()
    value = res.ok()
    assert value is not None
    assert isclose(value, 7.58, abs_tol=1e-2)


@pytest.mark.asyncio
async def test_async_pipes_simple() -> None:
    async def good(value: int) -> int:
        return value

    async def bad(value: int) -> int:
        raise ValueError

    good_result = await (Ok(123) >= good)
    bad_result = await (Ok(123) >= bad)

    assert isinstance(good_result, Ok)
    assert good_result.unwrap() == 123
    assert isinstance(bad_result, Err)
    assert isinstance(bad_result.unwrap_err(), ValueError)


@pytest.mark.asyncio
async def test_async_multivar_pipe() -> None:
    from math import isclose

    async def fnc(x: int, y: float, z: float) -> float:
        return (x + y) / z

    res = await (Ok(5) | Ok(2.5) | Ok(0.5) >= fnc)

    assert isinstance(res, Ok)
    assert isclose(res.ok(), 15)


Number = Union[float, int]

##############################################################
# function declarations for mypy testing
##############################################################


def tee(x: Number) -> Number:
    print(f"{x=}")
    return x


# functions
def square(x: Number) -> Number:
    return x * x


def cube(x: Number) -> Number:
    return x * x * x


def mod2(x: Number) -> Number:
    return x % 2


def div1(x: Number) -> Number:
    return 1 / x


def add1(x: Number) -> Number:
    return x + 1


def sub1(x: Number) -> Number:
    return x - 1


def div10(x: Number) -> Number:
    return x / 10


def add2(x: Number) -> Number:
    return x + 2


# filters
def le50(x: Number) -> bool:
    return x <= 50


def ge10(x: Number) -> bool:
    return x >= 10


def iseven(x: Number) -> bool:
    return x % 2 == 0


def sq(i: int) -> Result[int, int]:
    return Ok(i * i)


def to_err(i: int) -> Result[int, int]:
    return Err(i)


# Lambda versions of the same functions, just for test/type coverage
sq_lambda: Callable[[int], Result[int, int]] = lambda i: Ok(i * i)
to_err_lambda: Callable[[int], Result[int, int]] = lambda i: Err(i)
