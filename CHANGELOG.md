# Changelog

This project follows semantic versioning.

Possible log types:

- `[added]` for new features.
- `[changed]` for changes in existing functionality.
- `[deprecated]` for once-stable features removed in upcoming releases.
- `[removed]` for deprecated features removed in this release.
- `[fixed]` for any bug fixes.
- `[security]` to invite users to upgrade in case of vulnerabilities.

## Unreleased

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

[Unreleased]: https://github.com/dbrgn/result/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/dbrgn/result/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/dbrgn/result/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/dbrgn/result/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/dbrgn/result/compare/v0.2.2...v0.3.0
[0.2.2]: https://github.com/dbrgn/result/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/dbrgn/result/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/dbrgn/result/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/dbrgn/result/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/dbrgn/result/compare/3ca7d83...v0.1.0
