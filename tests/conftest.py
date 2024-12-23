# tests/conftest.py
import pytest
import os
import tempfile
from typing import Generator, Tuple


@pytest.fixture
def temp_file() -> Generator[Tuple[str, str], None, None]:
    """Creates a temporary file with content and returns (path, content)"""
    fd, path = tempfile.mkstemp()
    content = "This is test content"
    with os.fdopen(fd, "w") as f:
        f.write(content)
    yield path, content
    os.unlink(path)


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Creates a temporary directory and returns its path"""
    path = tempfile.mkdtemp()
    yield path
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.unlink(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)
