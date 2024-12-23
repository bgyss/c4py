# src/c4/errors.py
class ErrBadChar(Exception):
    def __init__(self, pos: int):
        self.pos = pos

    def __str__(self):
        return f"non c4 id character at position {self.pos}"


class ErrBadLength(Exception):
    def __init__(self, length: int):
        self.length = length

    def __str__(self):
        return f"c4 ids must be 90 characters long, input length {self.length}"


class ErrNil(Exception):
    def __str__(self):
        return "unexpected nil id"


class ErrInvalidTree(Exception):
    def __str__(self):
        return "invalid tree data"
