# Pytest test suite

import pytest

from .result import Result, Ok, Err


@pytest.mark.parametrize('instance', [
    Ok(1),
    Result.Ok(1),
])
def test_ok_factories(instance):
    instance._val == 1
    instance.is_ok() is True


@pytest.mark.parametrize('instance', [
    Err(2),
    Result.Err(2),
])
def test_err_factories(instance):
    instance._val == 2
    instance.is_err() is True


def test_eq():
    assert Ok(1) == Ok(1)
    assert Err(1) == Err(1)
    assert Ok(1) != Err(1)
    assert Ok(1) != Ok(2)


def test_ok():
    res = Ok('haha')
    res.is_ok() is True
    res.is_err() is False
    res.value == 'haha'


def test_err():
    res = Err(':(')
    res.is_ok() is False
    res.is_err() is True
    res.value == ':('


def test_ok_method():
    o = Ok('yay')
    n = Err('nay')
    assert o.ok() == 'yay'
    assert n.ok() is None


def test_err_method():
    o = Ok('yay')
    n = Err('nay')
    assert o.err() is None
    assert n.err() == 'nay'


def test_and_ten():
    def sq(x):
        return Ok(x * x)

    assert Ok(2).and_then(sq) == Ok(4)
    assert Err(2).and_then(sq) == Err(2)
    assert Ok(2).and_then(lambda x, y, z: Ok(x * y * z), y=2, z=4) == Ok(16)
    assert Ok((1, 2, 3)).and_then(lambda (x, y, z): Ok(x * y * z)) == Ok(6)


def test_or_else():
    def sq(x):
        return Ok(x * x)

    assert Ok(2).or_else(sq) == Ok(2)
    assert Err(2).or_else(sq) == Ok(4)
    assert Err(2).or_else(lambda x, y, z: Ok(x * y * z), y=2, z=4) == Ok(16)
    assert Err((1, 2, 3)).or_else(lambda (x, y, z): Ok(x * y * z)) == Ok(6)


def test_no_constructor():
    """
    Constructor should not be used directly.
    """
    with pytest.raises(RuntimeError):
        Result()
