from __future__ import annotations


import pytest

from result import Err, Ok, Result, branching


@pytest.mark.parametrize(
    "x, y, expectation",
    [
        (Ok(1), Ok(2), Ok(3)),
        (Ok(1), Err("erm.."), Err("erm..")),
        (Ok("erm"), Ok("mm..."), Ok("ermmm...")),
    ],
)
def test_branching(x, y, expectation):
    def foo() -> Result[int, str]:
        return x

    def bar() -> Result[int, str]:
        return y

    @branching
    def sum() -> Result[int, str]:
        return Ok(foo().branch + bar().branch)

    assert sum() == expectation


def test_returning_result_vs_branching_equivalency():
    def _ok() -> Result[int, str]:
        return Ok(69)

    def _err() -> Result[int, str]:
        return Err(420)

    @branching
    def _ok_branching() -> Result[int, str]:
        def inner() -> Result[int, str]:
            return Ok(69)

        return Ok(inner().branch)

    @branching
    def _err_branching() -> Result[int, str]:
        def inner() -> Result[int, str]:
            return Err(420)

        return Ok(inner().branch)

    assert _ok() == _ok_branching()
    assert _err() == _err_branching()
