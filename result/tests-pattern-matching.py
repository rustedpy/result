# -*- coding: utf-8 -*-
# Pytest test suite
from result import Result, Ok, Err


def test_pattern_matching_on_ok_type():
    o: Result[str, int] = Ok('yay')
    match o:
        case Ok(f):
            assert True
        case Err(e):
            assert False


def test_pattern_matching_on_err_type():
    e: Result[int, str] = Err('nay')
    match e:
        case Ok(f):
            assert False
        case Err(e):
            assert True
