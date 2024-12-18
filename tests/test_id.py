# tests/test_id.py
import pytest
import io
from c4py import ID, Digest, Encoder, identify, NIL_ID, VOID_ID, MAX_ID
from c4py.errors import ErrBadChar, ErrBadLength

def test_id_parse():
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

def test_digest_creation():
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

    # Too long input should return None
    long_data = bytes([1] * 65)
    digest = Digest(long_data)
    assert digest is None

def test_encoder():
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

def test_identify_file(temp_file):
    """Test identifying a file"""
    path, content = temp_file
    with open(path, 'rb') as f:
        id_obj = identify(f)
    
    # Test the same content with string IO
    str_io = io.BytesIO(content.encode())
    id_obj2 = identify(str_io)
    
    assert id_obj == id_obj2
    assert isinstance(id_obj, ID)

def test_constants():
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

def test_digest_sum():
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

def test_digest_edge_cases():
    """Test edge cases in Digest handling"""
    # Test empty digest
    empty_digest = Digest(b'')
    assert len(empty_digest) == 64
    assert all(b == 0 for b in empty_digest)
    
    # Test oversized input
    oversized = bytes([1] * 65)
    assert Digest(oversized) is None

def test_id_basic_comparisons():
    """Test edge cases in ID comparison"""
    id1 = ID.parse("c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1")
    
    # Test comparison with None
    assert id1 is not None
    assert not (id1 < None)
    
    # Test equality with same ID
    id2 = ID.parse("c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1")
    assert id1 == id2

def test_nil_id_handling():
    """Test handling of nil IDs"""
    from c4py.id import NIL_ID
    assert NIL_ID is not None
    # Test nil ID string representation
    assert len(str(NIL_ID)) == 90
    assert str(NIL_ID).startswith('c4')

def test_digest_sum_edge_cases():
    """Test edge cases in digest sum operation"""
    from c4py.id import Digest
    # Create two identical digests
    d1 = Digest(bytes([1] * 64))
    d2 = Digest(bytes([1] * 64))
    # Sum should return either digest when they're identical
    assert d1.sum(d2) == d1

def test_encoder_error_handling():
    """Test encoder error conditions"""
    from c4py import Encoder
    encoder = Encoder()
    # Test reset after write
    encoder.write(b'test')
    encoder.reset()
    # Verify reset worked by checking ID
    id1 = encoder.id()
    encoder.write(b'test')
    id2 = encoder.id()
    assert id1 != id2

# Update test_id_comparison_edge_cases
def test_id_nil_comparisons():
    """Test edge cases in ID comparison"""
    from c4py.id import NIL_ID
    
    # Compare with None
    assert not (NIL_ID < None)
    assert NIL_ID is not None
    
    # Compare with same ID
    id1 = NIL_ID
    id2 = NIL_ID
    assert id1 == id2
    assert not (id1 < id2)
    assert not (id2 < id1)