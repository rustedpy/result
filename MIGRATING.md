# Migration guides

## 0.11.0 -> 0.12 migration

``.value`` is now deprecated. New code should use ``.ok_value`` on instances of
``Ok`` and ``.err_value`` on instances of ``Err``. Existing code using
``.value`` will continue to work, but will result in a deprecation warning being
logged. Users of this library are encouraged to migrate away from ``.value``
before it is removed in a future version.

## 0.10 -> 0.11 migration

The 0.11 migration includes one breaking change:

`Ok` now requires an explicit value during instantiation. Previously, if no
value was provides, a default value of `True` was implicitly used.

To retain this behavior you can change any no-argument instantiations with:

```diff
- r = Ok()
+ r = Ok(True)
```

## 0.5 -> 0.6 migration

The 0.6 migration includes two breaking changes and some useful new functionality:

1\. The `Result.Ok()` and `Result.Err()` class methods have been removed. 
These should be replaced by direct use of `Ok()` and `Err()`. As an example, the following code:

```python
from result import Result
res1 = Result.Ok('yay')
res2 = Result.Err('nay')
```

should be replaced by:

```python
from result import Ok, Err
res1 = Ok('yay')
res2 = Err('nay')
```

2\. Result is now a Union type between `Ok[T]` and `Err[E]`. As such, you cannot use `isinstance(res, Result)` anymore.
These should be replaced by `isinstance(res, OkErr)`. As an example, the following code:

```python
from result import Ok, Result
res = Ok('yay')
if isinstance(res, Result):
    print("Result type!")
``` 

should be replaced with:

```python
from result import Ok, OkErr
res = Ok('yay')
if isinstance(res, OkErr):
    print("Result type!")
```

3\. Because `Result` is now a union type MyPy can statically check the Result type.
 In previous versions MyPy saw the following types:

```python
r: Result[int, str] = Ok(2)
if r.is_ok():
    reveal_type(r.value) # returns Union[int, str]
```

but now, by using `isinstance`:

```python
r: Result[int, str] = Ok(2) # == Union[Ok[int], Err[str]]
if isinstance(r, Ok):
    reveal_type(r.value) # returns int
```

This allows for better type checking, but requires the use of `isinstance` instead of `is_ok()` or `is_err()`.
