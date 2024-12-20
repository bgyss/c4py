# src/c4/__init__.py
from .id import ID, Digest, Encoder, encode, identify, NIL_ID, VOID_ID, MAX_ID
from .errors import (
    ErrBadChar, 
    ErrBadLength,
    ErrNil,
    ErrInvalidTree
)

__all__ = [
    'ID',
    'Digest',
    'Encoder',
    'encode',
    'identify',
    'NIL_ID',
    'VOID_ID',
    'MAX_ID',
    'ErrBadChar',
    'ErrBadLength',
    'ErrNil',
    'ErrInvalidTree'
]

