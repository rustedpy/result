<!-- markdownlint-disable -->

# API Overview

## Modules

- [`result`](./result.md#module-result)

## Classes

- [`result.DoException`](./result.md#class-doexception): This is used to signal to `do()` that the result is an `Err`,
- [`result.Err`](./result.md#class-err): A value that signifies failure and which stores arbitrary data for the error.
- [`result.Ok`](./result.md#class-ok): A value that indicates success and which stores arbitrary data for the return value.
- [`result.UnwrapError`](./result.md#class-unwraperror): Exception raised from ``.unwrap_<...>`` and ``.expect_<...>`` calls.

## Functions

- [`result.as_async_result`](./result.md#function-as_async_result): Make a decorator to turn an async function into one that returns a ``Result``.
- [`result.as_result`](./result.md#function-as_result): Make a decorator to turn a function into one that returns a ``Result``.
- [`result.do`](./result.md#function-do): Do notation for Result (syntactic sugar for sequence of `and_then()` calls).
- [`result.do_async`](./result.md#function-do_async): Async version of do. Example:
- [`result.is_err`](./result.md#function-is_err): A typeguard to check if a result is an Err
- [`result.is_ok`](./result.md#function-is_ok): A typeguard to check if a result is an Ok


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
