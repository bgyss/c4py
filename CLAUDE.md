# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

c4py is a Python implementation of the C4 ID system - a content-addressable identifier system using SHA-512 hashing and Base58 encoding. It provides both a Python library and command-line interface for generating C4 identifiers from files, streams, and raw bytes.

## Development Environment Setup

This project uses `uv` for dependency management and virtual environment handling:

```bash
# Install dependencies and create virtual environment
uv sync --dev

# Activate virtual environment (if needed)
. .venv/bin/activate
```

## Common Development Commands

### Testing
```bash
# Run all tests with coverage
pytest --cov=c4py --cov-report=xml

# Run tests without coverage
pytest

# Run specific test file
pytest tests/test_id.py

# Run specific test function
pytest tests/test_id.py::test_id_parsing
```

### Code Quality and Linting
```bash
# Run ruff linting (check only)
ruff check .

# Run ruff with auto-fix
ruff check . --fix

# Format code with ruff
ruff format .

# Run mypy type checking
mypy .

# Run all style checks (legacy tools also available)
black .
isort .
```

### Package Management
```bash
# Install new dependency
uv add <package-name>

# Install new development dependency  
uv add --dev <package-name>

# Update all dependencies
uv sync --upgrade
```

## Code Architecture

### Core Components

**src/c4py/id.py** - Core C4 ID implementation:
- `ID` class: Represents a C4 identifier with Base58 encoding/decoding
- `Digest` class: 64-byte SHA-512 digest with summation capabilities  
- `Encoder` class: Streaming hash encoder for generating C4 IDs
- Constants: `NIL_ID`, `VOID_ID`, `MAX_ID` for special cases

**src/c4py/cli.py** - Command-line interface:
- File and directory processing with recursive scanning
- Multiple output formats (basic, verbose, metadata)
- Stdin processing support
- Error handling and exit codes

**src/c4py/errors.py** - Custom exception classes:
- `ErrBadChar`: Invalid character in C4 ID string
- `ErrBadLength`: Incorrect C4 ID length  
- `ErrNil`/`ErrInvalidTree`: Runtime validation errors

### Key Design Patterns

- **Base58 Encoding**: Uses custom charset excluding ambiguous characters (0, O, I, l)
- **Streaming Processing**: `Encoder` class allows incremental hashing of large files
- **Digest Summation**: Merkle-tree style combining of digests for directory structures
- **CLI Architecture**: Click-based command interface with comprehensive option handling

### Testing Structure

Tests are organized by module in the `tests/` directory:
- `test_id.py`: Core ID, Digest, and Encoder functionality
- `test_cli.py`: Command-line interface testing
- `test_errors.py`: Exception handling validation
- `conftest.py`: Shared pytest fixtures and configuration

## Project Configuration

- **Python Versions**: Supports 3.8-3.12
- **Build System**: Uses `hatchling` backend
- **Package Manager**: `uv` for fast dependency resolution
- **CI/CD**: GitHub Actions with Python matrix testing and codecov integration
- **Code Style**: Black-compatible formatting (88 char line length) with ruff
- **Type Checking**: mypy with strict configuration requiring type annotations