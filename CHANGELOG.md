# Changelog

This project follows semantic versioning.

Possible log types:

- `[added]` for new features.
- `[changed]` for changes in existing functionality.
- `[deprecated]` for once-stable features removed in upcoming releases.
- `[removed]` for deprecated features removed in this release.
- `[fixed]` for any bug fixes.
- `[security]` to invite users to upgrade in case of vulnerabilities.

## [Unreleased]

- `[changed]` changed `as_result` so it can work with both generators and functions
- `[changed]` changed `as_async_result` so it can work with both async generators and async functions

## [0.16.1] - 2024-02-29

- `[fixed]` PyPI not showing description (#176)

## [0.16.0] - 2023-12-23

- `[added]` Add `map_async` for async functions (#165)
- `[fixed]` Add `do_async()` to handle edge case in `do()` involving multiple inlined awaits (#149)
- `[added]` Add support for Python 3.12 (#157)

## [0.15.0] - 2023-12-04

- `[added]` Add `do` function to support Haskell-style do-notation (#149)

## [0.14.0] - 2023-11-10

- `[added]` `is_ok` and `is_err` type guard functions as alternatives to `isinstance` checks (#69)
- `[added]` Add `and_then_async` for async functions (#148)

## [0.13.1] - 2023-07-19

- `[fixed]`  Use `self._value` instead of deprecated `self.value` in `Err.expect` and `Err.unwrap` to avoid raising a warning (#133)

## [0.13.0] - 2023-07-15

- `[changed]` Include captured `Err` value when `expect` and `unwrap` are called and an `UnwrapError` is raised (#98, #132)

## [0.12.0] - 2023-06-11

- `[removed]` Drop support for Python 3.7 (#126)
- `[fixed]` Pattern matching deprecation warning (#128)
- `[changed]` Minor internal implementation details (#129, #130)

## [0.11.0] - 2023-06-11

- `[changed]` `Ok` now requires an explicit value during instantiation. Please
  check out [MIGRATING.md], it will guide you through the necessary change in
  your codebase.
- `[deprecated]` `value` property to access the inner value (#37, #121)
- `[added]` `ok_value` and `err_value` to access the inner value more safely (#37, #121)

## [0.10.0] - 2023-04-29

- `[fixed]` Make python version check PEP 484 compliant (#118)
- `[added]` `as_async_result` decorator to turn regular async functions into
  `Result` returning ones (#116)

## [0.9.0] - 2022-12-09

- `[added]` Implement `unwrap_or_raise` (#95)
- `[added]` Add support for Python 3.11 (#107)
- `[changed]` Narrowing of return types on methods of `Err` and `Ok`. (#106)
- `[fixed]` Fix failing type inference for `Result.map` and similar method
  unions (#106)

## [0.8.0] - 2022-04-17

- `[added]` `as_result` decorator to turn regular functions into
  `Result` returning ones (#33, 71)
- `[removed]` Drop support for Python 3.6 (#49)
- `[added]` Implement `unwrap_or_else` (#74), `and_then` (#90) and `or_else` (#90)

## [0.7.0] - 2021-11-19

- `[removed]` Drop support for Python 3.5 (#34)
- `[added]` Add support for Python 3.9 and 3.10 (#50)
- `[changed]` Make the `Ok` type covariant in regard to its wrapped type `T`.
  Likewise for `Err` in regard to `E`. This should result in more intuitive
  type checking behaviour. For instance, `Err[TypeError]` will get recognized
  as a subtype of `Err[Exception]` by type checkers. See [PEP 438] for a
  detailed explanation of covariance and its implications.
- `[added]` Add support for Python 3.10 pattern matching (#47)
- `[changed]` `Ok` and `Err` now define `__slots__` to save memory (#55, #58)
- `[changed]` The generic type of `UnwrapError.result` now explicitly specifies `Any` (#67)

[PEP 438]: https://www.python.org/dev/peps/pep-0483/#covariance-and-contravariance

## [0.6.0] - 2021-03-17

**IMPORTANT:** This release a big API refactoring to make the API more type
safe. Unfortunately this means some breaking changes. Please check out
[MIGRATING.md], it will guide you through the necessary changes in your
codebase.


- [changed] Split result type into `Ok` and `Err` classes (#17, #27)
- [deprecated] Python 3.4 support is deprecated and will be removed in the next
  release

## [0.5.0] - 2020-03-03

 - [added] Implement `map`, `map_err`, `map_or` and `map_or_else` (#19)
 - [added] Add `unwrap_err` and `expect_err` methods (#26)
 - [changed] Type annotations: Change parameter order
   from `Result[E, T]` to `Result[T, E]` to match Rust/OCaml/F# (#7)

## [0.4.1] - 2020-02-17

 - [added] Add `py.typed` for PEP561 package compliance (#16)

## [0.4.0] - 2019-04-17

 - [added] Add `unwrap`, `unwrap_or` and `expect` (#9)
 - [removed] Drop support for Python 2 and 3.3
 - [changed] Only install typing dependency for Python <3.5

## [0.3.0] - 2017-07-12

 - [added] This library is now fully type annotated (#4, thanks @tyehle)
 - [added] Implementations for `__ne__`, `__hash__` and `__repr__`
 - [deprecated] Python 2 support is deprecated and will be removed in the 0.4 release

## [0.2.2] - 2016-09-21

 - [added] `__eq__` magic method

## [0.2.0] - 2016-05-05

 - [added] Convenience default: `Ok()` == `Ok(True)`

## [0.1.1] - 2015-12-14

 - [fixed] Import bugfix

## [0.1.0] - 2015-12-14

 - Initial version

[MIGRATING.md]: https://github.com/rustedpy/result/blob/main/MIGRATING.md
[Unreleased]: https://github.com/rustedpy/result/compare/v0.16.1...HEAD
[0.16.1]: https://github.com/rustedpy/result/compare/v0.16.0...v0.16.1
[0.16.0]: https://github.com/rustedpy/result/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/rustedpy/result/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/rustedpy/result/compare/v0.13.1...v0.14.0
[0.13.1]: https://github.com/rustedpy/result/compare/v0.13.0...v0.13.1
[0.13.0]: https://github.com/rustedpy/result/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/rustedpy/result/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/rustedpy/result/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/rustedpy/result/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/rustedpy/result/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/rustedpy/result/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/rustedpy/result/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/rustedpy/result/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/rustedpy/result/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/rustedpy/result/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/rustedpy/result/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/rustedpy/result/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/rustedpy/result/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/rustedpy/result/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/rustedpy/result/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/rustedpy/result/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/rustedpy/result/compare/3ca7d83...v0.1.0
