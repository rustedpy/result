# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals


class Result(object):
    """
    A simple `Result` type inspired by Rust.

    Not all methods (https://doc.rust-lang.org/std/result/enum.Result.html)
    have been implemented, only the ones that make sense in the Python context.
    You still don't get any type checking done.

    """
    def __init__(self, force=False):
        if force is not True:
            raise RuntimeError("Don't instantiate a Result directly. "
                               "Use the Ok(value) and Err(error) class methods instead.")

    @classmethod
    def Ok(cls, value):
        instance = cls(force=True)
        instance._val = value
        instance._type = 'ok'
        return instance

    @classmethod
    def Err(cls, error):
        instance = cls(force=True)
        instance._val = error
        instance._type = 'error'
        return instance

    def is_ok(self):
        return self._type == 'ok'

    def is_err(self):
        return self._type == 'error'

    def ok(self):
        """
        Return the value if it is an `Ok` type. Return `None` if it is an `Err`.
        """
        return self._val if self.is_ok() else None

    def err(self):
        """
        Return the error if this is an `Err` type. Return `None` otherwise.
        """
        return self._val if self.is_err() else None

    @property
    def value(self):
        """
        Return the inner value. This might be either the ok or the error type.
        """
        return self._val

    # TODO: Implement __iter__ for destructuring


def Ok(value):
    """
    Shortcut function to create a new Result.
    """
    return Result.Ok(value)


def Err(error):
    """
    Shortcut function to create a new Result.
    """
    return Result.Err(error)
