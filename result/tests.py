# Pytest test suite

import pytest

from result import Result, Ok, Err


@pytest.mark.parametrize('instance', [
    Ok(1),
    Result.Ok(1),
])
def test_ok_factories(instance):
    instance._value == 1
    instance.is_ok() is True


@pytest.mark.parametrize('instance', [
    Err(2),
    Result.Err(2),
])
def test_err_factories(instance):
    instance._value == 2
    instance.is_err() is True


def test_eq():
    assert Ok(1) == Ok(1)
    assert Err(1) == Err(1)
    assert Ok(1) != Err(1)
    assert Ok(1) != Ok(2)
    assert Ok(1) != "abc"
    assert Ok("0") != Ok(0)


def test_hash():
    assert len({Ok(1), Err("2"), Ok(1), Err("2")}) == 2
    assert len({Ok(1), Ok(2)}) == 2
    assert len({Ok("a"), Err("a")}) == 2


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


def test_no_arg_ok():
    top_level = Ok()
    top_level.is_ok() is True
    top_level.ok() is True

    class_method = Result.Ok()
    class_method.is_ok() is True
    class_method.ok() is True


def test_no_constructor():
    """
    Constructor should not be used directly.
    """
    with pytest.raises(RuntimeError):
        Result(is_ok=True, value='yay')
