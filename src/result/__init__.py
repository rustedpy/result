"""A Rust-like Result type for Python."""

from .result import (
    Err,
    Ok,
    OkErr,
    Result,
    UnwrapError,
    as_async_result,
    as_result,
    do,
    do_async,
    is_err,
    is_ok,
)

__all__ = [
    "Err",
    "Ok",
    "OkErr",
    "Result",
    "UnwrapError",
    "as_async_result",
    "as_result",
    "do",
    "do_async",
    "is_err",
    "is_ok",
]
