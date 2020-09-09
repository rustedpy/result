from random import random
import re


def get_user_input() -> str:
    if random() > 0.5:
        raise IOError('Could not read input')
    return 'my name is alice'


def extract_name_from_input(inp: str) -> str:
    p = re.compile('my name is (\\w+)')
    m = p.match(inp)
    if m is None:
        raise ValueError('Input is invalid')
    return m.group(1)


def authorize_user(user: str) -> bool:
    return user == 'alice'


try:
    inp = get_user_input()
    try:
        if authorize_user(extract_name_from_input(inp)):
            print('Hi! Welcome to the secret club')
        else:
            print('Stop! You are not authorized to enter.')
    except ValueError as e:
        print('Something went wrong while trying to extract name from input', e)
except IOError as e:
    print('Something went wrong while trying to read user input', e)
