<!-- markdownlint-disable -->

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `result`




**Global Variables**
---------------
- **OkErr**

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L465"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `as_result`

```python
as_result(
    *exceptions: 'Type[TBE]'
) → Callable[[Callable[P, R]], Callable[P, Result[R, TBE]]]
```

Make a decorator to turn a function into one that returns a ``Result``. 

Regular return values are turned into ``Ok(return_value)``. Raised exceptions of the specified exception type(s) are turned into ``Err(exc)``. 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L497"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `as_async_result`

```python
as_async_result(
    *exceptions: 'Type[TBE]'
) → Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[Result[R, TBE]]]]
```

Make a decorator to turn an async function into one that returns a ``Result``. Regular return values are turned into ``Ok(return_value)``. Raised exceptions of the specified exception type(s) are turned into ``Err(exc)``. 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L530"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_ok`

```python
is_ok(result: 'Result[T, E]') → TypeGuard[Ok[T]]
```

A typeguard to check if a result is an Ok 

Usage: 

``` python
r: Result[int, str] = get_a_result()
if is_ok(r):
     r   # r is of type Ok[int]
elif is_err(r):
     r   # r is of type Err[str]
``` 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L547"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_err`

```python
is_err(result: 'Result[T, E]') → TypeGuard[Err[E]]
```

A typeguard to check if a result is an Err 

Usage: 

``` python
r: Result[int, str] = get_a_result()
if is_ok(r):
     r   # r is of type Ok[int]
elif is_err(r):
     r   # r is of type Err[str]
``` 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L564"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `do`

```python
do(gen: 'Generator[Result[T, E], None, None]') → Result[T, E]
```

Do notation for Result (syntactic sugar for sequence of `and_then()` calls). 



Usage: 

``` rust
// This is similar to
use do_notation::m;
let final_result = m! {
     x <- Ok("hello");
     y <- Ok(True);
     Ok(len(x) + int(y) + 0.5)
};
``` 

``` rust
final_result: Result[float, int] = do(
         Ok(len(x) + int(y) + 0.5)
         for x in Ok("hello")
         for y in Ok(True)
     )
``` 

NOTE: If you exclude the type annotation e.g. `Result[float, int]` your type checker might be unable to infer the return type. To avoid an error, you might need to help it with the type hint. 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L609"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `do_async`

```python
do_async(
    gen: 'Union[Generator[Result[T, E], None, None], AsyncGenerator[Result[T, E], None]]'
) → Result[T, E]
```

Async version of do. Example: 

``` python
final_result: Result[float, int] = await do_async(
     Ok(len(x) + int(y) + z)
         for x in await get_async_result_1()
         for y in await get_async_result_2()
         for z in get_sync_result_3()
     )
``` 

NOTE: Python makes generators async in a counter-intuitive way. 

``` python
# This is a regular generator:
     async def foo(): ...
     do(Ok(1) for x in await foo())
``` 

``` python
# But this is an async generator:
     async def foo(): ...
     async def bar(): ...
     do(
         Ok(1)
         for x in await foo()
         for y in await bar()
     )
``` 

We let users try to use regular `do()`, which works in some cases of awaiting async values. If we hit a case like above, we raise an exception telling the user to use `do_async()` instead. See `do()`. 

However, for better usability, it's better for `do_async()` to also accept regular generators, as you get in the first case: 

``` python
async def foo(): ...
     do(Ok(1) for x in await foo())
``` 

Furthermore, neither mypy nor pyright can infer that the second case is actually an async generator, so we cannot annotate `do_async()` as accepting only an async generator. This is additional motivation to accept either. 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Ok`
A value that indicates success and which stores arbitrary data for the return value. 

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'T') → None
```






---

#### <kbd>property</kbd> ok_value

Return the inner value. 

---

#### <kbd>property</kbd> value

Return the inner value. 

@deprecated Use `ok_value` or `err_value` instead. This method will be removed in a future version. 



---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L183"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'Callable[[T], Result[U, E]]') → Result[U, E]
```

The contained result is `Ok`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'Callable[[T], Awaitable[Result[U, E]]]') → Result[U, E]
```

The contained result is `Ok`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L76"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → None
```

Return `None`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(_message: 'str') → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(message: 'str') → NoReturn
```

Raise an UnwrapError since this type is `Ok` 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], None]') → Result[T, E]
```

Calls a function with the contained value if `Ok`. Returns the original result. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L212"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], None]') → Result[T, E]
```

Calls a function with the contained value if `Err`. Returns the original result. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[False]
```





---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L64"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[True]
```





---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L147"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'Callable[[T], U]') → Ok[U]
```

The contained result is `Ok`, so return `Ok` with original value mapped to a new value using the passed in function. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L154"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'Callable[[T], Awaitable[U]]') → Ok[U]
```

The contained result is `Ok`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'object') → Ok[T]
```

The contained result is `Ok`, so return `Ok` with the original value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'object', op: 'Callable[[T], U]') → U
```

The contained result is `Ok`, so return the original value mapped to a new value using the passed in function. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L170"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'object', op: 'Callable[[T], U]') → U
```

The contained result is `Ok`, so return original value mapped to a new value using the passed in `op` function. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L199"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'object') → Ok[T]
```

The contained result is `Ok`, so return `Ok` with the original value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → NoReturn
```

Raise an UnwrapError since this type is `Ok` 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(_default: 'U') → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L135"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'object') → T
```

Return the value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(e: 'object') → T
```

Return the value. 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L219"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DoException`
This is used to signal to `do()` that the result is an `Err`, which short-circuits the generator and returns that Err. Using this exception for control flow in `do()` allows us to simulate `and_then()` in the Err case: namely, we don't call `op`, we just return `self` (the Err). 

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L228"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(err: 'Err[E]') → None
```









---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L232"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Err`
A value that signifies failure and which stores arbitrary data for the error. 

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L248"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(value: 'E') → None
```






---

#### <kbd>property</kbd> err_value

Return the inner value. 

---

#### <kbd>property</kbd> value

Return the inner value. 

@deprecated Use `ok_value` or `err_value` instead. This method will be removed in a future version. 



---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L391"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then`

```python
and_then(op: 'object') → Err[E]
```

The contained result is `Err`, so return `Err` with the original value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L397"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `and_then_async`

```python
and_then_async(op: 'object') → Err[E]
```

The contained result is `Err`, so return `Err` with the original value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L275"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `err`

```python
err() → E
```

Return the error. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L304"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect`

```python
expect(message: 'str') → NoReturn
```

Raises an `UnwrapError`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L316"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `expect_err`

```python
expect_err(_message: 'str') → E
```

Return the inner value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L410"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect`

```python
inspect(op: 'Callable[[T], None]') → Result[T, E]
```

Calls a function with the contained value if `Ok`. Returns the original result. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L416"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `inspect_err`

```python
inspect_err(op: 'Callable[[E], None]') → Result[T, E]
```

Calls a function with the contained value if `Err`. Returns the original result. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L266"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_err`

```python
is_err() → Literal[True]
```





---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L263"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_ok`

```python
is_ok() → Literal[False]
```





---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L359"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map`

```python
map(op: 'object') → Err[E]
```

Return `Err` with the same value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L365"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_async`

```python
map_async(op: 'object') → Err[E]
```

The contained result is `Ok`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L384"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_err`

```python
map_err(op: 'Callable[[E], F]') → Err[F]
```

The contained result is `Err`, so return `Err` with original error mapped to a new value using the passed in function. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L372"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or`

```python
map_or(default: 'U', op: 'object') → U
```

Return the default value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L378"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `map_or_else`

```python
map_or_else(default_op: 'Callable[[], U]', op: 'object') → U
```

Return the result of the default operation 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L269"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ok`

```python
ok() → None
```

Return `None`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L403"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `or_else`

```python
or_else(op: 'Callable[[E], Result[T, F]]') → Result[T, F]
```

The contained result is `Err`, so return the result of `op` with the original value passed in 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L322"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap`

```python
unwrap() → NoReturn
```

Raises an `UnwrapError`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L334"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_err`

```python
unwrap_err() → E
```

Return the inner value 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L340"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or`

```python
unwrap_or(default: 'U') → U
```

Return `default`. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L346"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_else`

```python
unwrap_or_else(op: 'Callable[[E], T]') → T
```

The contained result is ``Err``, so return the result of applying ``op`` to the error value. 

---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L353"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `unwrap_or_raise`

```python
unwrap_or_raise(e: 'Type[TBE]') → NoReturn
```

The contained result is ``Err``, so raise the exception with the value. 


---

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L440"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UnwrapError`
Exception raised from ``.unwrap_<...>`` and ``.expect_<...>`` calls. 

The original ``Result`` can be accessed via the ``.result`` attribute, but this is not intended for regular use, as type information is lost: ``UnwrapError`` doesn't know about both ``T`` and ``E``, since it's raised from ``Ok()`` or ``Err()`` which only knows about either ``T`` or ``E``, not both. 

<a href="https://github.com/rustedpy/result/blob/main/src/result/result.py#L453"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(result: 'Result[object, object]', message: 'str') → None
```






---

#### <kbd>property</kbd> result

Returns the original result. 






---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
