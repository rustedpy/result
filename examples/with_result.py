from enum import Enum
from random import random
from result import Result, Ok, Err
import re


class AppError(Enum):
    IOError = 1
    InvalidInput = 2
    AuthorizationError = 3


def get_user_input() -> Result[str, AppError]:
    return Ok('my name is alice')


def extract_name_from_input(inp: str) -> Result[str, AppError]:
    p = re.compile('my name is (\\w+)')
    m = p.match(inp)
    if m is None:
        return Err(AppError.InvalidInput)
    return Ok(m.group(1))


def authorize_user(user: str) -> Result[bool, AppError]:
    if random() > 0.5:
        return Err(AppError.AuthorizationError)
    return Ok(user == 'alice')


auth_check = (get_user_input()
    .and_then(extract_name_from_input)
    .and_then(authorize_user))  # type: Result[bool, AppError]

if isinstance(auth_check, Ok):
    authorized = auth_check.ok()
    if authorized:
        print('Hi! Welcome to the secret club')
    else:
        print('Stop! You are not authorized to enter.')
else:
    print('Something went wrong', auth_check.err())
