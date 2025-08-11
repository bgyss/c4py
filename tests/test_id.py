# tests/test_id.py
import pytest
import io
from typing import Tuple
from c4py import ID, Digest, Encoder, identify, NIL_ID, VOID_ID, MAX_ID
from c4py.errors import ErrBadChar, ErrBadLength


def test_id_parse() -> None:
    """Test parsing valid and invalid C4 IDs"""
    # Valid ID
    valid_id = "c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1"
    id_obj = ID.parse(valid_id)
    assert str(id_obj) == valid_id

    # Invalid length
    with pytest.raises(ErrBadLength):
        ID.parse("c4abc")

    # Invalid character
    with pytest.raises(ErrBadChar):
        ID.parse("c4" + "0" * 88)  # '0' is not in the C4 charset

    # Not starting with c4
    with pytest.raises(ErrBadChar):
        ID.parse("d4" + "1" * 88)


def test_digest_creation() -> None:
    """Test creating digests with different inputs"""
    # Valid 64-byte digest
    data = bytes([1] * 64)
    digest = Digest(data)
    assert len(digest) == 64
    assert digest == data

    # Short input should be padded
    short_data = bytes([1] * 32)
    digest = Digest(short_data)
    assert len(digest) == 64
    expected = bytes([0] * 32) + short_data
    assert digest == expected

    # Too long input should raise ValueError
    long_data = bytes([1] * 65)
    with pytest.raises(ValueError):
        Digest(long_data)


def test_encoder() -> None:
    """Test the Encoder class"""
    encoder = Encoder()

    # Test writing and getting ID
    test_data = b"Hello, World!"
    encoder.write(test_data)
    id1 = encoder.id()

    # Test reset and re-writing
    encoder.reset()
    encoder.write(test_data)
    id2 = encoder.id()

    assert id1 == id2
    assert isinstance(id1, ID)


def test_identify_file(temp_file: Tuple[str, str]) -> None:
    """Test identifying a file"""
    path, content = temp_file
    with open(path, "rb") as f:
        id_obj = identify(f)

    # Test the same content with string IO
    str_io = io.BytesIO(content.encode())
    id_obj2 = identify(str_io)

    assert id_obj == id_obj2
    assert isinstance(id_obj, ID)


def test_constants() -> None:
    """Test the predefined constants"""
    assert NIL_ID is not None
    assert VOID_ID is not None
    assert MAX_ID is not None

    # NIL_ID should be the ID of empty input
    empty_io = io.BytesIO(b"")
    assert identify(empty_io) == NIL_ID

    # VOID_ID should be the ID of 64 zero bytes
    assert len(VOID_ID.digest()) == 64
    assert all(b == 0 for b in VOID_ID.digest())

    # MAX_ID should be the ID of 64 0xFF bytes
    assert len(MAX_ID.digest()) == 64
    assert all(b == 0xFF for b in MAX_ID.digest())


def test_digest_sum() -> None:
    """Test the sum operation of digests"""
    d1 = Digest(bytes([1] * 64))
    d2 = Digest(bytes([2] * 64))
    d3 = d1.sum(d2)

    assert isinstance(d3, Digest)
    assert len(d3) == 64

    # Sum should be commutative
    d4 = d2.sum(d1)
    assert d3 == d4

    # Sum with self should return self
    assert d1.sum(d1) == d1


def test_digest_edge_cases() -> None:
    """Test edge cases in Digest handling"""
    # Test empty digest
    empty_digest = Digest(b"")
    assert len(empty_digest) == 64
    assert all(b == 0 for b in empty_digest)

    # Test oversized input
    oversized = bytes([1] * 65)
    with pytest.raises(ValueError):
        Digest(oversized)


def test_id_basic_comparisons() -> None:
    """Test edge cases in ID comparison"""
    id1 = ID.parse(
        "c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1"
    )

    # Test comparison with None
    assert id1 is not None
    assert not (id1 < None)

    # Test equality with same ID
    id2 = ID.parse(
        "c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1"
    )
    assert id1 == id2


def test_nil_id_handling() -> None:
    """Test handling of nil IDs"""
    from c4py.id import NIL_ID

    assert NIL_ID is not None
    # Test nil ID string representation
    assert len(str(NIL_ID)) == 90
    assert str(NIL_ID).startswith("c4")


def test_digest_sum_edge_cases() -> None:
    """Test edge cases in digest sum operation"""
    from c4py.id import Digest

    # Create two identical digests
    d1 = Digest(bytes([1] * 64))
    d2 = Digest(bytes([1] * 64))
    # Sum should return either digest when they're identical
    assert d1.sum(d2) == d1


def test_encoder_error_handling() -> None:
    """Test encoder error conditions"""
    from c4py import Encoder

    encoder = Encoder()
    # Test reset after write
    encoder.write(b"test")
    encoder.reset()
    # Verify reset worked by checking ID
    id1 = encoder.id()
    encoder.write(b"test")
    id2 = encoder.id()
    assert id1 != id2


# Update test_id_comparison_edge_cases
def test_id_nil_comparisons() -> None:
    """Test edge cases in ID comparison"""
    from c4py.id import NIL_ID

    # Compare with None
    assert NIL_ID is not None
    assert not (NIL_ID < None)

    # Compare with same ID
    id1 = NIL_ID
    id2 = NIL_ID
    assert id1 == id2
    assert not (id1 < id2)
    assert not (id2 < id1)


def test_id_edge_cases() -> None:
    """Test edge cases in ID creation and handling"""
    # Test ID with zero value
    zero_id = ID(0)
    assert str(zero_id) == ""

    # Test empty string parse
    with pytest.raises(ErrBadLength):
        ID.parse("")


def test_digest_comparison() -> None:
    """Test digest comparison operations"""
    d1 = Digest(bytes([1] * 64))
    d2 = Digest(bytes([2] * 64))

    # Test less than comparison
    assert d1 < d2
    assert not (d2 < d1)

    # Test equality
    d3 = Digest(bytes([1] * 64))
    assert d1 == d3
    assert not (d1 < d3)


def test_encoder_large_data() -> None:
    """Test encoder with large data chunks"""
    encoder = Encoder()

    # Write large chunk of data
    large_data = bytes([x % 256 for x in range(1000000)])
    written = encoder.write(large_data)
    assert written == len(large_data)

    # Get ID and verify it's valid
    id_obj = encoder.id()
    assert isinstance(id_obj, ID)
    assert len(str(id_obj)) == 90

    # Get digest and verify
    digest = encoder.digest()
    assert isinstance(digest, Digest)
    assert len(digest) == 64


def test_id_value_edge_cases() -> None:
    """Test ID creation with edge case values (line 61)"""
    # Create an ID with value 0, which should result in empty string
    id_obj = ID(0)
    assert str(id_obj) == ""

    # Test with a small positive value to ensure encoding works
    id_obj = ID(1)
    assert str(id_obj).startswith("c4")
    assert len(str(id_obj)) == 90


def test_digest_invalid_bytes() -> None:
    """Test Digest creation with invalid bytes (line 123)"""
    # Test with empty bytes
    empty_digest = Digest(b"")
    assert len(empty_digest) == 64
    assert all(b == 0 for b in empty_digest)

    # Test with bytes that are too long (line 123 case)
    too_long = bytes([1] * 65)
    with pytest.raises(ValueError):
        Digest(too_long)


def test_id_parse_invalid_char() -> None:
    """Test ID.parse with an invalid character in the ID string (line 61)"""
    test_id = "c4" + "1" * 87 + "0"  # "0" is not in the valid charset
    with pytest.raises(ErrBadChar) as exc:
        ID.parse(test_id)
    assert exc.value.pos == 89  # The invalid char is at position 89


def test_digest_overflow() -> None:
    """Test creating a digest that would overflow (line 123)"""
    # Create a large bytes object
    max_bytes = b"\xff" * 64
    digest = Digest(max_bytes)

    # Try to create a new ID from this digest
    id_obj = digest.id()
    assert isinstance(id_obj, ID)

    # Now try to create a new digest from this ID
    # This should hit line 123 as we manipulate the internal value
    result = id_obj.digest()
    assert isinstance(result, Digest)
    assert len(result) == 64


def test_id_equality_with_non_id() -> None:
    """Test ID equality comparison with non-ID objects (line 61)"""
    id_obj = ID.parse("c4" + "1" * 88)

    # Compare with non-ID objects should return NotImplemented
    result = id_obj.__eq__("string")
    assert result is NotImplemented

    result = id_obj.__eq__(42)
    assert result is NotImplemented

    result = id_obj.__eq__(None)
    assert result is NotImplemented

    # Compare with another ID should work normally
    other_id = ID.parse("c4" + "2" * 88)
    assert id_obj != other_id
    assert id_obj == id_obj


def test_encode_function() -> None:
    """Test the encode function (line 127)"""
    from c4py.id import encode
    import io

    # Test with some data
    test_data = b"test data for encoding"
    src = io.BytesIO(test_data)

    result = encode(src)
    assert isinstance(result, ID)

    # Should be the same as calling identify
    src2 = io.BytesIO(test_data)
    result2 = identify(src2)
    assert result == result2
