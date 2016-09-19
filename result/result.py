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

    def __eq__(self, other):
        return self._type == other._type and self._val == other._val


    @classmethod
    def Ok(cls, value=True):
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

    def and_then(self, function, **kwargs):
        """
        Return the error if this is an `Err` type. Return `function` calls return value otherwise.
        """
        if self._type == 'error':
            return self
        return function(self._val, **kwargs)

    def or_else(self, function, **kwargs):
        """
        Return the error if this is an `Ok` type. Return `function` calls return value otherwise.
        """
        if self._type == 'ok':
            return self
        return function(self._val, **kwargs)

    @property
    def value(self):
        """
        Return the inner value. This might be either the ok or the error type.
        """
        return self._val

    # TODO: Implement __iter__ for destructuring


def Ok(value=True):
    """
    Shortcut function to create a new Result.
    """
    return Result.Ok(value)


def Err(error):
    """
    Shortcut function to create a new Result.
    """
    return Result.Err(error)
