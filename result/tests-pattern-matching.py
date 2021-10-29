from result import Err, Ok, Result


def test_pattern_matching_on_ok_type() -> None:
    o: Result[str, int] = Ok('yay')
    match o:
        case Ok(f):
            f  # Avoids flake8 F841 unused variable
            assert True
        case Err(e):
            e
            assert False


def test_pattern_matching_on_err_type() -> None:
    n: Result[int, str] = Err('nay')
    match n:
        case Ok(f):
            f
            assert False
        case Err(e):
            e
            assert True
