from __future__ import annotations

import pytest

from result import Err, Ok, Result, do, do_async

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _resx(is_suc: bool) -> Result[str, int]:
    return Ok("hello") if is_suc else Err(1)


def _resy(is_suc: bool) -> Result[bool, int]:
    return Ok(True) if is_suc else Err(2)


def _resz(is_suc: bool) -> Result[float, int]:
    return Ok(0.5) if is_suc else Err(3)


async def _aresx(is_suc: bool) -> Result[str, int]:
    return Ok("hello") if is_suc else Err(1)


async def _aresy(is_suc: bool) -> Result[bool, int]:
    return Ok(True) if is_suc else Err(2)


# ---------------------------------------------------------------------------
# Synchronous do()
# ---------------------------------------------------------------------------


class TestDo:
    @pytest.mark.parametrize(
        ("s1", "s2", "expected"),
        [
            (True, True, Ok(6.5)),
            (True, False, Err(2)),
            (False, True, Err(1)),
            (False, False, Err(1)),
        ],
    )
    def test_do(self, s1: bool, s2: bool, expected: Result[float, int]) -> None:
        result: Result[float, int] = do(
            Ok(len(x) + int(y) + 0.5) for x in _resx(s1) for y in _resy(s2)
        )
        assert result == expected

    @pytest.mark.asyncio
    async def test_do_async_generator_error(self) -> None:
        """do() raises a helpful TypeError when given an async generator."""

        async def _aget(is_suc: bool) -> Result[str, int]:
            return Ok("hello") if is_suc else Err(1)

        async def _bget(is_suc: bool) -> Result[bool, int]:
            return Ok(True) if is_suc else Err(2)

        with pytest.raises(TypeError, match="Got async_generator"):
            do(Ok(len(x) + int(y)) for x in await _aget(True) for y in await _bget(True))

    def test_do_reraises_other_type_error(self) -> None:
        """do() re-raises TypeErrors not related to async generators."""

        def bad_gen() -> Result[int, int]:  # type: ignore[misc]
            msg = "something else"
            raise TypeError(msg)
            yield Ok(1)  # type: ignore[unreachable]

        with pytest.raises(TypeError, match="something else"):
            do(bad_gen())


# ---------------------------------------------------------------------------
# Async do_async()
# ---------------------------------------------------------------------------


class TestDoAsync:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("s1", "s2", "expected"),
        [
            (True, True, Ok(6.5)),
            (True, False, Err(2)),
            (False, True, Err(1)),
            (False, False, Err(1)),
        ],
    )
    async def test_do_async(self, s1: bool, s2: bool, expected: Result[float, int]) -> None:
        result: Result[float, int] = await do_async(
            Ok(len(x) + int(y) + 0.5) for x in await _aresx(s1) for y in await _aresy(s2)
        )
        assert result == expected

    @pytest.mark.asyncio
    async def test_do_async_with_sync_generator(self) -> None:
        """do_async() also accepts regular (non-async) generators."""
        result: Result[float, int] = await do_async(
            Ok(len(x) + int(y) + 0.5) for x in _resx(True) for y in _resy(True)
        )
        assert result == Ok(6.5)

    @pytest.mark.asyncio
    async def test_do_async_mixed_sync_async(self) -> None:
        result: Result[float, int] = await do_async(
            Ok(len(x) + int(y) + z)
            for x in await _aresx(True)
            for y in await _aresy(True)
            for z in _resz(True)
        )
        assert result == Ok(6.5)

    @pytest.mark.asyncio
    async def test_do_async_err_short_circuits(self) -> None:
        result: Result[float, int] = await do_async(
            Ok(len(x) + int(y) + z)
            for x in await _aresx(False)
            for y in await _aresy(True)
            for z in _resz(True)
        )
        assert result == Err(1)

    @pytest.mark.asyncio
    async def test_do_async_one_await(self) -> None:
        """Single await in generator expression — Python makes this a regular generator."""
        assert await do_async(Ok(len(x)) for x in await _aresx(True)) == Ok(5)
        assert await do_async(Ok(len(x)) for x in await _aresx(False)) == Err(1)

    @pytest.mark.asyncio
    async def test_do_async_swap_order(self) -> None:
        def foo() -> Result[int, str]:
            return Ok(1)

        async def bar() -> Result[int, str]:
            return Ok(2)

        r1: Result[int, str] = await do_async(Ok(x + y) for x in foo() for y in await bar())
        r2: Result[int, str] = await do_async(Ok(x + y) for y in await bar() for x in foo())
        assert r1 == r2 == Ok(3)

    @pytest.mark.asyncio
    async def test_do_async_further_processing(self) -> None:
        async def process(x: str, y: bool, z: float) -> Result[float, int]:
            return Ok(len(x) + int(y) + z)

        result: Result[float, int] = await do_async(
            Ok(w)
            for x in await _aresx(True)
            for y in await _aresy(True)
            for z in _resz(True)
            for w in await process(x, y, z)
        )
        assert result == Ok(6.5)

    @pytest.mark.asyncio
    async def test_do_async_pre_resolved_values(self) -> None:
        """Async values resolved before do() — results in a regular generator."""
        resx = await _aresx(True)
        resy = await _aresy(True)
        result: Result[float, int] = do(Ok(len(x) + int(y) + 0.5) for x in resx for y in resy)
        assert result == Ok(6.5)
