from __future__ import annotations


import pytest

from result import Err, Ok, Result, do, do_async


def test_result_do_general() -> None:
    def resx(is_suc: bool) -> Result[str, int]:
        return Ok("hello") if is_suc else Err(1)

    def resy(is_suc: bool) -> Result[bool, int]:
        return Ok(True) if is_suc else Err(2)

    def _get_output(is_suc1: bool, is_suc2: bool) -> Result[float, int]:
        out: Result[float, int] = do(
            Ok(len(x) + int(y) + 0.5) for x in resx(is_suc1) for y in resy(is_suc2)
        )
        return out

    assert _get_output(True, True) == Ok(6.5)
    assert _get_output(True, False) == Err(2)
    assert _get_output(False, True) == Err(1)
    assert _get_output(False, False) == Err(1)

    def _get_output_return_immediately(
        is_suc1: bool, is_suc2: bool
    ) -> Result[float, int]:
        return do(
            Ok(len(x) + int(y) + 0.5) for x in resx(is_suc1) for y in resy(is_suc2)
        )

    assert _get_output_return_immediately(True, True) == Ok(6.5)


@pytest.mark.asyncio
async def test_result_do_general_with_async_values() -> None:
    # Asyncio works with regular `do()` as long as you await
    # the async calls outside the `do()` expression.
    # This causes the generator to be a regular (not async) generator.
    async def aget_resx(is_suc: bool) -> Result[str, int]:
        return Ok("hello") if is_suc else Err(1)

    async def aget_resy(is_suc: bool) -> Result[bool, int]:
        return Ok(True) if is_suc else Err(2)

    async def _aget_output(is_suc1: bool, is_suc2: bool) -> Result[float, int]:
        resx, resy = await aget_resx(is_suc1), await aget_resy(is_suc2)
        out: Result[float, int] = do(
            Ok(len(x) + int(y) + 0.5) for x in resx for y in resy
        )
        return out

    assert await _aget_output(True, True) == Ok(6.5)
    assert await _aget_output(True, False) == Err(2)
    assert await _aget_output(False, True) == Err(1)
    assert await _aget_output(False, False) == Err(1)


@pytest.mark.asyncio
async def test_result_do_async_one_value() -> None:
    """This is a strange case where Python creates a regular
    (non async) generator despite an `await` inside the generator expression.
    For convenience, although this works with regular `do()`, we want to support this
    with `do_async()` as well."""

    async def aget_resx(is_suc: bool) -> Result[str, int]:
        return Ok("hello") if is_suc else Err(1)

    def get_resz(is_suc: bool) -> Result[float, int]:
        return Ok(0.5) if is_suc else Err(3)

    assert await do_async(Ok(len(x)) for x in await aget_resx(True)) == Ok(5)
    assert await do_async(Ok(len(x)) for x in await aget_resx(False)) == Err(1)

    async def _aget_output(is_suc1: bool, is_suc3: bool) -> Result[float, int]:
        return await do_async(
            Ok(len(x) + z) for x in await aget_resx(is_suc1) for z in get_resz(is_suc3)
        )

    assert await _aget_output(True, True) == Ok(5.5)
    assert await _aget_output(True, False) == Err(3)
    assert await _aget_output(False, True) == Err(1)
    assert await _aget_output(False, False) == Err(1)


@pytest.mark.asyncio
async def test_result_do_async_general() -> None:
    async def aget_resx(is_suc: bool) -> Result[str, int]:
        return Ok("hello") if is_suc else Err(1)

    async def aget_resy(is_suc: bool) -> Result[bool, int]:
        return Ok(True) if is_suc else Err(2)

    def get_resz(is_suc: bool) -> Result[float, int]:
        return Ok(0.5) if is_suc else Err(3)

    async def _aget_output(
        is_suc1: bool, is_suc2: bool, is_suc3: bool
    ) -> Result[float, int]:
        out: Result[float, int] = await do_async(
            Ok(len(x) + int(y) + z)
            for x in await aget_resx(is_suc1)
            for y in await aget_resy(is_suc2)
            for z in get_resz(is_suc3)
        )
        return out

    assert await _aget_output(True, True, True) == Ok(6.5)
    assert await _aget_output(True, False, True) == Err(2)
    assert await _aget_output(False, True, True) == Err(1)
    assert await _aget_output(False, False, True) == Err(1)

    assert await _aget_output(True, True, False) == Err(3)
    assert await _aget_output(True, False, False) == Err(2)
    assert await _aget_output(False, True, False) == Err(1)
    assert await _aget_output(False, False, False) == Err(1)

    async def _aget_output_return_immediately(
        is_suc1: bool, is_suc2: bool, is_suc3: bool
    ) -> Result[float, int]:
        return await do_async(
            Ok(len(x) + int(y) + z)
            for x in await aget_resx(is_suc1)
            for y in await aget_resy(is_suc2)
            for z in get_resz(is_suc3)
        )

    assert await _aget_output_return_immediately(True, True, True) == Ok(6.5)


@pytest.mark.asyncio
async def test_result_do_async_further_processing() -> None:
    async def aget_resx(is_suc: bool) -> Result[str, int]:
        return Ok("hello") if is_suc else Err(1)

    async def aget_resy(is_suc: bool) -> Result[bool, int]:
        return Ok(True) if is_suc else Err(2)

    def get_resz(is_suc: bool) -> Result[float, int]:
        return Ok(0.5) if is_suc else Err(3)

    async def process_xyz(x: str, y: bool, z: float) -> Result[float, int]:
        return Ok(len(x) + int(y) + z)

    async def _aget_output(
        is_suc1: bool, is_suc2: bool, is_suc3: bool
    ) -> Result[float, int]:
        out: Result[float, int] = await do_async(
            Ok(w)
            for x in await aget_resx(is_suc1)
            for y in await aget_resy(is_suc2)
            for z in get_resz(is_suc3)
            for w in await process_xyz(x, y, z)
        )
        return out

    assert await _aget_output(True, True, True) == Ok(6.5)
    assert await _aget_output(True, False, True) == Err(2)
    assert await _aget_output(False, True, True) == Err(1)
    assert await _aget_output(False, False, True) == Err(1)

    assert await _aget_output(True, True, False) == Err(3)
    assert await _aget_output(True, False, False) == Err(2)
    assert await _aget_output(False, True, False) == Err(1)
    assert await _aget_output(False, False, False) == Err(1)


@pytest.mark.asyncio
async def test_result_do_general_with_async_values_inline_error() -> None:
    """
    Due to subtle behavior, `do()` works in certain cases involving async
    calls but not others. We surface a more helpful error to the user
    in cases where it doesn't work indicating to use `do_async()` instead.
    Contrast this with `test_result_do_general_with_async_values()`
    in which using `do()` works with async functions as long as
    their return values are resolved outside the `do()` expression.
    """

    async def aget_resx(is_suc: bool) -> Result[str, int]:
        return Ok("hello") if is_suc else Err(1)

    async def aget_resy(is_suc: bool) -> Result[bool, int]:
        return Ok(True) if is_suc else Err(2)

    def get_resz(is_suc: bool) -> Result[float, int]:
        return Ok(0.5) if is_suc else Err(3)

    with pytest.raises(TypeError) as excinfo:
        do(
            Ok(len(x) + int(y) + z)
            for x in await aget_resx(True)
            for y in await aget_resy(True)
            for z in get_resz(True)
        )

    assert (
        "Got async_generator but expected generator.See the section on do notation in the README."
    ) in excinfo.value.args[0]


@pytest.mark.asyncio
async def test_result_do_async_swap_order() -> None:
    def foo() -> Result[int, str]:
        return Ok(1)

    async def bar() -> Result[int, str]:
        return Ok(2)

    result1: Result[int, str] = await do_async(
        Ok(x + y)
        # x first
        for x in foo()
        # then y
        for y in await bar()
    )

    result2: Result[int, str] = await do_async(
        Ok(x + y)
        # y first
        for y in await bar()
        # then x
        for x in foo()
    )

    assert result1 == result2 == Ok(3)
