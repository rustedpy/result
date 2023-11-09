from __future__ import annotations


import pytest

from result import Err, Ok, Result, do


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


@pytest.mark.asyncio
async def test_result_do_general_async() -> None:
    async def get_resx(is_suc: bool) -> Result[str, int]:
        return Ok("hello") if is_suc else Err(1)

    async def get_resy(is_suc: bool) -> Result[bool, int]:
        return Ok(True) if is_suc else Err(2)

    async def _get_output(is_suc1: bool, is_suc2: bool) -> Result[float, int]:
        resx, resy = await get_resx(is_suc1), await get_resy(is_suc2)
        out: Result[float, int] = do(
            Ok(len(x) + int(y) + 0.5)
            for x in resx
            for y in resy
        )
        return out

    assert await _get_output(True, True) == Ok(6.5)
    assert await _get_output(True, False) == Err(2)
    assert await _get_output(False, True) == Err(1)
    assert await _get_output(False, False) == Err(1)
