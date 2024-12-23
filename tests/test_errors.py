# tests/test_errors.py
from c4py.errors import ErrBadChar, ErrBadLength, ErrNil, ErrInvalidTree


def test_error_messages():
    """Test error message formatting"""
    # Test ErrBadChar
    err = ErrBadChar(5)
    assert str(err) == "non c4 id character at position 5"

    # Test ErrBadLength
    err = ErrBadLength(50)
    assert str(err) == "c4 ids must be 90 characters long, input length 50"

    # Test ErrNil
    err = ErrNil()
    assert str(err) == "unexpected nil id"

    # Test ErrInvalidTree
    err = ErrInvalidTree()
    assert str(err) == "invalid tree data"
