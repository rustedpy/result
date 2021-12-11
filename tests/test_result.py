import pytest

from result import Err, Ok, OkErr, Result, UnwrapError


def test_ok_factories() -> None:
    instance = Ok(1)
    assert instance._value == 1
    assert instance.is_ok() is True


def test_err_factories() -> None:
    instance = Err(2)
    assert instance._value == 2
    assert instance.is_err() is True


def test_eq() -> None:
    assert Ok(1) == Ok(1)
    assert Err(1) == Err(1)
    assert Ok(1) != Err(1)
    assert Ok(1) != Ok(2)
    assert Err(1) != Err(2)
    assert not (Ok(1) != Ok(1))
    assert Ok(1) != "abc"
    assert Ok("0") != Ok(0)


def test_hash() -> None:
    assert len({Ok(1), Err("2"), Ok(1), Err("2")}) == 2
    assert len({Ok(1), Ok(2)}) == 2
    assert len({Ok("a"), Err("a")}) == 2


def test_repr() -> None:
    """
    ``repr()`` returns valid code if the wrapped value's ``repr()`` does as well.
    """
    o = Ok(123)
    n = Err(-1)

    assert repr(o) == "Ok(123)"
    assert o == eval(repr(o))

    assert repr(n) == "Err(-1)"
    assert n == eval(repr(n))


def test_ok() -> None:
    res = Ok('haha')
    assert res.is_ok() is True
    assert res.is_err() is False
    assert res.value == 'haha'


def test_err() -> None:
    res = Err(':(')
    assert res.is_ok() is False
    assert res.is_err() is True
    assert res.value == ':('


def test_ok_method() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.ok() == 'yay'
    assert n.ok() is None  # type: ignore[func-returns-value]


def test_err_method() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.err() is None  # type: ignore[func-returns-value]
    assert n.err() == 'nay'


def test_no_arg_ok() -> None:
    top_level: Result[None, None] = Ok()
    assert top_level.is_ok() is True
    assert top_level.ok() is True


def test_expect() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.expect('failure') == 'yay'
    with pytest.raises(UnwrapError):
        n.expect('failure')


def test_expect_err() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert n.expect_err('hello') == 'nay'
    with pytest.raises(UnwrapError):
        o.expect_err('hello')


def test_unwrap() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.unwrap() == 'yay'
    with pytest.raises(UnwrapError):
        n.unwrap()


def test_unwrap_err() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert n.unwrap_err() == 'nay'
    with pytest.raises(UnwrapError):
        o.unwrap_err()


def test_unwrap_or() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.unwrap_or('some_default') == 'yay'
    assert n.unwrap_or('another_default') == 'another_default'


def test_unwrap_or_else() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.unwrap_or_else(str.upper) == 'yay'
    assert n.unwrap_or_else(str.upper) == 'NAY'


def test_map() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.map(str.upper).ok() == 'YAY'
    assert n.map(str.upper).err() == 'nay'

    num = Ok(3)
    errnum = Err(2)
    assert num.map(str).ok() == '3'
    assert errnum.map(str).err() == 2


def test_map_or() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.map_or('hay', str.upper) == 'YAY'
    assert n.map_or('hay', str.upper) == 'hay'

    num = Ok(3)
    errnum = Err(2)
    assert num.map_or('-1', str) == '3'
    assert errnum.map_or('-1', str) == '-1'


def test_map_or_else() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.map_or_else(lambda: 'hay', str.upper) == 'YAY'
    assert n.map_or_else(lambda: 'hay', str.upper) == 'hay'

    num = Ok(3)
    errnum = Err(2)
    assert num.map_or_else(lambda: '-1', str) == '3'
    assert errnum.map_or_else(lambda: '-1', str) == '-1'


def test_map_err() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert o.map_err(str.upper).ok() == 'yay'
    assert n.map_err(str.upper).err() == 'NAY'


def test_isinstance_result_type() -> None:
    o = Ok('yay')
    n = Err('nay')
    assert isinstance(o, OkErr)
    assert isinstance(n, OkErr)
    assert not isinstance(1, OkErr)


def test_error_context() -> None:
    n = Err('nay')
    with pytest.raises(UnwrapError) as exc_info:
        n.unwrap()
    exc = exc_info.value
    assert exc.result is n


def test_slots() -> None:
    """
    Ok and Err have slots, so assigning arbitrary attributes fails.
    """
    o = Ok('yay')
    n = Err('nay')
    with pytest.raises(AttributeError):
        o.some_arbitrary_attribute = 1  # type: ignore[attr-defined]
    with pytest.raises(AttributeError):
        n.some_arbitrary_attribute = 1  # type: ignore[attr-defined]
