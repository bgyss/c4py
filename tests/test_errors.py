# tests/test_errors.py
from c4py.errors import ErrBadChar, ErrBadLength, ErrNil, ErrInvalidTree


def test_error_messages() -> None:
    """Test error message formatting"""
    # Test ErrBadChar
    err_bad_char = ErrBadChar(5)
    assert str(err_bad_char) == "non c4 id character at position 5"

    # Test ErrBadLength
    err_bad_length = ErrBadLength(50)
    assert str(err_bad_length) == "c4 ids must be 90 characters long, input length 50"

    # Test ErrNil
    err_nil = ErrNil()
    assert str(err_nil) == "unexpected nil id"

    # Test ErrInvalidTree
    err_invalid_tree = ErrInvalidTree()
    assert str(err_invalid_tree) == "invalid tree data"
