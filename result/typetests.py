from typing import Any, List, Optional

from .result import Result, Ok, Err


# Test constructor functions
res1 = Ok()  # type: Result[Any, Any]
res2 = Ok(42)  # type: Result[int, Any]
res3 = Err(1)  # type: Result[Any, int]

res4 = Ok('hello')  # type: Result[str, int]
if isinstance(res4, Ok):
    ok = res4  # type: Ok[str]
    okValue = res4.ok()  # type: str
    mapped_to_float = res4.map_or(1.0, lambda s: len(s) * 1.5)  # type: float
else:
    err = res4  # type: Err[int]
    errValue = err.err()  # type: int
    mapped_to_list = res4.map_err(lambda e: [e]).err()  # type: Optional[List[int]]


# Test mapping
map_str_42 = Ok(42).map(str)  # type: Result[str, None]
map_str_42_float = Ok(42).map(str).map(float)  # type: Result[float, Any]
map_str_42_float_err = Ok(42).map_err(str).map(float)  # type: Result[float, str]


# Test and_then
and_then_str_42 = Ok(42).and_then(lambda x: Ok(str(x)))  # type: Result[str, None]


def f(x: int) -> Result[str, Any]:
    return Ok(str(x))


and_then_str_42_float = Ok(42).and_then(f)  # type: Result[str, Any]
