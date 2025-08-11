# src/c4/id.py
import hashlib
from typing import Optional, BinaryIO
from .errors import ErrBadChar, ErrBadLength

CHARSET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE = 58
PREFIX = b"c4"
ID_LEN = 90

# Build lookup tables
_lut = [0xFF] * 256
for i, c in enumerate(CHARSET):
    _lut[ord(c)] = i


class ID:
    def __init__(self, value: int):
        self._value = value

    @classmethod
    def parse(cls, src: str) -> "ID":
        if len(src) != ID_LEN:
            raise ErrBadLength(len(src))

        if not src.startswith("c4"):
            raise ErrBadChar(0)

        value = 0
        for i, c in enumerate(src[2:], 2):
            digit = _lut[ord(c)]
            if digit == 0xFF:
                raise ErrBadChar(i)
            value = value * BASE + digit

        return cls(value)

    def __str__(self) -> str:
        if self._value == 0:
            return ""

        value = self._value
        encoded = []
        while value > 0:
            value, mod = divmod(value, BASE)
            encoded.append(CHARSET[mod])

        padding = ID_LEN - 2 - len(encoded)
        result = ["c", "4"]
        result.extend(["1"] * padding)
        result.extend(reversed(encoded))

        return "".join(result)

    def digest(self) -> "Digest":
        raw_bytes = self._value.to_bytes(64, "big")
        return Digest(raw_bytes)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ID):
            return NotImplemented
        return self._value == other._value

    def __lt__(self, other: Optional["ID"]) -> bool:
        if other is None:
            return False
        return self._value < other._value


class Digest(bytes):
    def __new__(cls, data: bytes) -> "Digest":
        if len(data) > 64:
            raise ValueError("Data too long for digest")
        if len(data) < 64:
            # Pad with zeros
            data = bytes(64 - len(data)) + data
        return super().__new__(cls, data)

    def id(self) -> ID:
        value = int.from_bytes(self, "big")
        return ID(value)

    def sum(self, other: "Digest") -> "Digest":
        if self == other:
            return self

        if self < other:
            data = self + other
        else:
            data = other + self

        hasher = hashlib.sha512()
        hasher.update(data)
        return Digest(hasher.digest())


class Encoder:
    def __init__(self) -> None:
        self._hasher = hashlib.sha512()

    def write(self, data: bytes) -> int:
        self._hasher.update(data)
        return len(data)

    def id(self) -> ID:
        value = int.from_bytes(self._hasher.digest(), "big")
        return ID(value)

    def digest(self) -> Digest:
        return Digest(self._hasher.digest())

    def reset(self) -> None:
        self._hasher = hashlib.sha512()


def identify(src: BinaryIO) -> Optional[ID]:
    enc = Encoder()
    while True:
        chunk = src.read(8192)
        if not chunk:
            break
        enc.write(chunk)
    return enc.id()


def encode(src: BinaryIO) -> Optional[ID]:
    return identify(src)


# Initialize constants
with open("/dev/null", "rb") as f:
    NIL_ID = identify(f)
void_bytes = bytes(64)
VOID_ID = Digest(void_bytes).id()
max_bytes = bytes([0xFF] * 64)
MAX_ID = Digest(max_bytes).id()
