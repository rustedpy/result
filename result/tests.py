# -*- coding: utf-8 -*-
# Pytest test suite

import pytest

from result import Result, Ok, Err


@pytest.mark.parametrize('instance', [
    Ok(1),
    Result.Ok(1),
])
def test_ok_factories(instance):
    assert instance._value == 1
    assert instance.is_ok() is True


@pytest.mark.parametrize('instance', [
    Err(2),
    Result.Err(2),
])
def test_err_factories(instance):
    assert instance._value == 2
    assert instance.is_err() is True


def test_eq():
    assert Ok(1) == Ok(1)
    assert Err(1) == Err(1)
    assert Ok(1) != Err(1)
    assert Ok(1) != Ok(2)
    assert not (Ok(1) != Ok(1))
    assert Ok(1) != "abc"
    assert Ok("0") != Ok(0)


def test_hash():
    assert len({Ok(1), Err("2"), Ok(1), Err("2")}) == 2
    assert len({Ok(1), Ok(2)}) == 2
    assert len({Ok("a"), Err("a")}) == 2


def test_repr():
    assert Ok(u"£10") == eval(repr(Ok(u"£10")))
    assert Ok("£10") == eval(repr(Ok("£10")))


def test_ok():
    res = Ok('haha')
    assert res.is_ok() is True
    assert res.is_err() is False
    assert res.value == 'haha'


def test_err():
    res = Err(':(')
    assert res.is_ok() is False
    assert res.is_err() is True
    assert res.value == ':('


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
    assert top_level.is_ok() is True
    assert top_level.ok() is True

    class_method = Result.Ok()
    assert class_method.is_ok() is True
    assert class_method.ok() is True


def test_no_constructor():
    """
    Constructor should not be used directly.
    """
    with pytest.raises(RuntimeError):
        Result(is_ok=True, value='yay')
