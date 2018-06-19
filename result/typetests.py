from typing import List, Optional

from .result import Result, Ok, Err


res1 = Result.Ok('hello')  # type: Result[str, int]
if res1.is_ok():
    ok = res1.ok()  # type: Optional[str]
    mapped_to_float = res1.map_or(1.0, lambda s: len(s) * 1.5)  # type: float
else:
    err = res1.err()  # type: Optional[int]
    mapped_to_list = res1.map_err(lambda e: [e]).err()  # type: Optional[List[int]]

# Test constructor functions
res2 = Ok()
res3 = Result.Ok()
res4 = Ok(42)
res5 = Result.Ok(23)
res6 = Err(1)
res7 = Result.Err(2)
