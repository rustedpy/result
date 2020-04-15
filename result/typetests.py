from typing import List, Optional

from .result import Result, Ok, Err


res1 = Ok('hello')  # type: Result[str, int]
if isinstance(res1, Ok):
    ok = res1  # type: Ok[str]
    okValue = res1.ok()  # type: str
    mapped_to_float = res1.map_or(1.0, lambda s: len(s) * 1.5)  # type: float
else:
    err = res1  # type: Err[int]
    errValue = err.err()  # type: int
    mapped_to_list = res1.map_err(lambda e: [e]).err()  # type: Optional[List[int]]

# Test constructor functions
res1 = Ok()
res2 = Ok(42)
res3 = Err(1)
