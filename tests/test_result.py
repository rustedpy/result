from __future__ import annotations

import pytest

from result import Err, Ok, OkErr, Result, UnwrapError, as_async_result, as_result, is_err, is_ok

# ---------------------------------------------------------------------------
# Construction, repr, equality, hashing
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_ok(self) -> None:
        o = Ok(1)
        assert o._value == 1
        assert o.is_ok() is True
        assert o.is_err() is False

    def test_err(self) -> None:
        e = Err(2)
        assert e._value == 2
        assert e.is_ok() is False
        assert e.is_err() is True


class TestRepr:
    @pytest.mark.parametrize(
        ("result", "expected"),
        [
            (Ok(123), "Ok(123)"),
            (Ok("hello"), "Ok('hello')"),
            (Err(-1), "Err(-1)"),
            (Err("bad"), "Err('bad')"),
        ],
    )
    def test_repr(self, result: Ok[object] | Err[object], expected: str) -> None:
        assert repr(result) == expected

    def test_repr_roundtrip(self) -> None:
        for r in (Ok(123), Err(-1)):
            assert r == eval(repr(r))


class TestEquality:
    @pytest.mark.parametrize(
        ("a", "b", "eq"),
        [
            (Ok(1), Ok(1), True),
            (Ok(1), Ok(2), False),
            (Err(1), Err(1), True),
            (Err(1), Err(2), False),
            (Ok(1), Err(1), False),
            (Ok("0"), Ok(0), False),
            (Ok(1), "abc", False),
        ],
    )
    def test_eq(self, a: object, b: object, *, eq: bool) -> None:
        assert (a == b) is eq
        assert (a != b) is (not eq)


class TestHash:
    def test_deduplication(self) -> None:
        assert len({Ok(1), Err("2"), Ok(1), Err("2")}) == 2

    def test_ok_distinct(self) -> None:
        assert len({Ok(1), Ok(2)}) == 2

    def test_ok_err_same_inner_differ(self) -> None:
        assert len({Ok("a"), Err("a")}) == 2


# ---------------------------------------------------------------------------
# Accessors: ok(), err(), ok_value, err_value
# ---------------------------------------------------------------------------


class TestAccessors:
    def test_ok_ok(self) -> None:
        assert Ok("yay").ok() == "yay"

    def test_ok_err(self) -> None:
        assert Ok("yay").err() is None

    def test_err_ok(self) -> None:
        assert Err("nay").ok() is None

    def test_err_err(self) -> None:
        assert Err("nay").err() == "nay"

    def test_ok_value_property(self) -> None:
        assert Ok("val").ok_value == "val"

    def test_err_value_property(self) -> None:
        assert Err("val").err_value == "val"


# ---------------------------------------------------------------------------
# expect / expect_err
# ---------------------------------------------------------------------------


class TestExpect:
    def test_ok_expect(self) -> None:
        assert Ok("yay").expect("failure") == "yay"

    def test_err_expect_raises(self) -> None:
        with pytest.raises(UnwrapError):
            Err("nay").expect("failure")

    def test_err_expect_raises_with_base_exception(self) -> None:
        err = Err(ValueError("boom"))
        with pytest.raises(UnwrapError) as exc_info:
            err.expect("oh no")
        assert exc_info.value.__cause__ is err.err_value

    def test_err_expect_err(self) -> None:
        assert Err("nay").expect_err("hello") == "nay"

    def test_ok_expect_err_raises(self) -> None:
        with pytest.raises(UnwrapError):
            Ok("yay").expect_err("hello")


# ---------------------------------------------------------------------------
# unwrap / unwrap_err / unwrap_or / unwrap_or_else / unwrap_or_raise
# ---------------------------------------------------------------------------


class TestUnwrap:
    def test_ok_unwrap(self) -> None:
        assert Ok("yay").unwrap() == "yay"

    def test_err_unwrap_raises(self) -> None:
        with pytest.raises(UnwrapError):
            Err("nay").unwrap()

    def test_err_unwrap_chains_base_exception(self) -> None:
        original = ValueError("Some Error")
        res = Err(original)
        with pytest.raises(UnwrapError) as exc_info:
            res.unwrap()
        assert isinstance(exc_info.value.__cause__, ValueError)

    def test_ok_unwrap_err_raises(self) -> None:
        with pytest.raises(UnwrapError):
            Ok("yay").unwrap_err()

    def test_err_unwrap_err(self) -> None:
        assert Err("nay").unwrap_err() == "nay"


class TestUnwrapOr:
    def test_ok_returns_value(self) -> None:
        assert Ok("yay").unwrap_or("default") == "yay"

    def test_err_returns_default(self) -> None:
        assert Err("nay").unwrap_or("default") == "default"


class TestUnwrapOrElse:
    def test_ok_ignores_callable(self) -> None:
        assert Ok("yay").unwrap_or_else(str.upper) == "yay"

    def test_err_applies_callable(self) -> None:
        assert Err("nay").unwrap_or_else(str.upper) == "NAY"


class TestUnwrapOrRaise:
    def test_ok_returns_value(self) -> None:
        assert Ok("yay").unwrap_or_raise(ValueError) == "yay"

    def test_err_raises(self) -> None:
        with pytest.raises(ValueError, match="nay"):
            Err("nay").unwrap_or_raise(ValueError)


# ---------------------------------------------------------------------------
# map / map_async / map_or / map_or_else / map_err
# ---------------------------------------------------------------------------


class TestMap:
    def test_ok_map(self) -> None:
        assert Ok("yay").map(str.upper) == Ok("YAY")

    def test_err_map(self) -> None:
        assert Err("nay").map(str.upper) == Err("nay")

    @pytest.mark.asyncio
    async def test_ok_map_async(self) -> None:
        async def upper(s: str) -> str:
            return s.upper()

        assert (await Ok("yay").map_async(upper)) == Ok("YAY")

    @pytest.mark.asyncio
    async def test_err_map_async(self) -> None:
        async def upper(s: str) -> str:
            return s.upper()

        assert (await Err("nay").map_async(upper)) == Err("nay")


class TestMapOr:
    def test_ok(self) -> None:
        assert Ok("yay").map_or("hay", str.upper) == "YAY"

    def test_err(self) -> None:
        assert Err("nay").map_or("hay", str.upper) == "hay"


class TestMapOrElse:
    def test_ok(self) -> None:
        assert Ok("yay").map_or_else(lambda: "hay", str.upper) == "YAY"

    def test_err(self) -> None:
        assert Err("nay").map_or_else(lambda: "hay", str.upper) == "hay"


class TestMapErr:
    def test_ok(self) -> None:
        assert Ok("yay").map_err(str.upper) == Ok("yay")

    def test_err(self) -> None:
        assert Err("nay").map_err(str.upper) == Err("NAY")


# ---------------------------------------------------------------------------
# and_then / and_then_async / or_else
# ---------------------------------------------------------------------------


def _sq(i: int) -> Result[int, int]:
    return Ok(i * i)


def _to_err(i: int) -> Result[int, int]:
    return Err(i)


class TestAndThen:
    def test_ok_chain(self) -> None:
        assert Ok(2).and_then(_sq).and_then(_sq).ok() == 16

    def test_ok_then_err(self) -> None:
        assert Ok(2).and_then(_sq).and_then(_to_err).err() == 4

    def test_err_short_circuits(self) -> None:
        assert Err(3).and_then(_sq).and_then(_sq).err() == 3

    @pytest.mark.asyncio
    async def test_ok_chain_async(self) -> None:
        async def sq_async(i: int) -> Result[int, int]:
            return Ok(i * i)

        result = await (await Ok(2).and_then_async(sq_async)).and_then_async(sq_async)
        assert result.ok() == 16

    @pytest.mark.asyncio
    async def test_err_short_circuits_async(self) -> None:
        async def sq_async(i: int) -> Result[int, int]:
            return Ok(i * i)

        result = await (await Err(3).and_then_async(sq_async)).and_then_async(sq_async)
        assert result.err() == 3


class TestOrElse:
    def test_ok_returns_self(self) -> None:
        assert Ok(2).or_else(_sq).or_else(_sq).ok() == 2

    def test_err_applies_op(self) -> None:
        assert Err(3).or_else(_sq).or_else(_to_err).ok() == 9

    def test_err_chain(self) -> None:
        assert Err(3).or_else(_to_err).or_else(_to_err).err() == 3


# ---------------------------------------------------------------------------
# inspect / inspect_err
# ---------------------------------------------------------------------------


class TestInspect:
    def test_ok_calls_op(self) -> None:
        seen: list[int] = []
        result = Ok(42).inspect(seen.append)
        assert result == Ok(42)
        assert seen == [42]

    def test_err_skips_op(self) -> None:
        seen: list[int] = []
        result = Err("e").inspect(seen.append)
        assert result == Err("e")
        assert seen == []


class TestInspectErr:
    def test_err_calls_op(self) -> None:
        seen: list[str] = []
        result = Err("e").inspect_err(seen.append)
        assert result == Err("e")
        assert seen == ["e"]

    def test_ok_skips_op(self) -> None:
        seen: list[str] = []
        result = Ok(42).inspect_err(seen.append)
        assert result == Ok(42)
        assert seen == []


# ---------------------------------------------------------------------------
# isinstance / OkErr
# ---------------------------------------------------------------------------


class TestOkErr:
    def test_ok_is_instance(self) -> None:
        assert isinstance(Ok("yay"), OkErr)

    def test_err_is_instance(self) -> None:
        assert isinstance(Err("nay"), OkErr)

    def test_other_is_not(self) -> None:
        assert not isinstance(1, OkErr)


# ---------------------------------------------------------------------------
# UnwrapError.result
# ---------------------------------------------------------------------------


class TestUnwrapError:
    def test_result_attribute(self) -> None:
        n = Err("nay")
        with pytest.raises(UnwrapError) as exc_info:
            n.unwrap()
        assert exc_info.value.result is n


# ---------------------------------------------------------------------------
# Slots
# ---------------------------------------------------------------------------


class TestSlots:
    def test_ok_no_dict(self) -> None:
        with pytest.raises(AttributeError):
            Ok("yay").arbitrary = 1  # type: ignore[attr-defined]

    def test_err_no_dict(self) -> None:
        with pytest.raises(AttributeError):
            Err("nay").arbitrary = 1  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Pattern matching
# ---------------------------------------------------------------------------


class TestPatternMatching:
    def test_ok(self) -> None:
        o: Result[str, int] = Ok("yay")
        match o:
            case Ok(value):
                assert value == "yay"
            case _:
                pytest.fail("Expected Ok match")

    def test_err(self) -> None:
        n: Result[int, str] = Err("nay")
        match n:
            case Err(value):
                assert value == "nay"
            case _:
                pytest.fail("Expected Err match")


# ---------------------------------------------------------------------------
# is_ok / is_err type guards
# ---------------------------------------------------------------------------


class TestTypeGuards:
    def test_is_ok(self) -> None:
        r: Result[int, str] = Ok(1)
        assert is_ok(r) is True
        assert is_err(r) is False

    def test_is_err(self) -> None:
        r: Result[int, str] = Err("e")
        assert is_ok(r) is False
        assert is_err(r) is True


# ---------------------------------------------------------------------------
# as_result / as_async_result
# ---------------------------------------------------------------------------


class TestAsResult:
    def test_success(self) -> None:
        @as_result(ValueError)
        def good(value: int) -> int:
            return value

        result = good(123)
        assert isinstance(result, Ok)
        assert result.unwrap() == 123

    def test_caught_exception(self) -> None:
        @as_result(IndexError, ValueError)
        def bad(value: int) -> int:
            raise ValueError(value)

        result = bad(123)
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), ValueError)

    def test_uncaught_exception_propagates(self) -> None:
        @as_result(ValueError)
        def f() -> int:
            raise IndexError

        with pytest.raises(IndexError):
            f()

    def test_no_exception_types_raises(self) -> None:
        with pytest.raises(TypeError, match="requires one or more exception types"):

            @as_result()
            def f() -> int:
                return 1

    def test_non_exception_type_raises(self) -> None:
        with pytest.raises(TypeError, match="requires one or more exception types"):

            @as_result("not an exception type")  # type: ignore[arg-type]
            def f() -> int:
                return 1


class TestAsAsyncResult:
    @pytest.mark.asyncio
    async def test_success(self) -> None:
        @as_async_result(ValueError)
        async def good(value: int) -> int:
            return value

        result = await good(123)
        assert isinstance(result, Ok)
        assert result.unwrap() == 123

    @pytest.mark.asyncio
    async def test_caught_exception(self) -> None:
        @as_async_result(IndexError, ValueError)
        async def bad(value: int) -> int:
            raise ValueError(value)

        result = await bad(123)
        assert isinstance(result, Err)
        assert isinstance(result.unwrap_err(), ValueError)

    def test_no_exception_types_raises(self) -> None:
        with pytest.raises(TypeError, match="requires one or more exception types"):

            @as_async_result()
            async def f() -> int:
                return 1

    def test_non_exception_type_raises(self) -> None:
        with pytest.raises(TypeError, match="requires one or more exception types"):

            @as_async_result("not an exception type")  # type: ignore[arg-type]
            async def f() -> int:
                return 1
