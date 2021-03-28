from typing import List, Optional

from .result import Result, Ok, Err


res1: Result[str, int] = Ok('hello')
if isinstance(res1, Ok):
    ok: Ok[str] = res1
    okValue: str = res1.ok()
    mapped_to_float: float = res1.map_or(1.0, lambda s: len(s) * 1.5)
else:
    err: Err[int] = res1
    errValue: int = err.err()
    mapped_to_list: Optional[List[int]] = res1.map_err(lambda e: [e]).err()

# Test constructor functions
res1 = Ok()
res2 = Ok(42)
res3 = Err(1)
