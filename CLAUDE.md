# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

c4py is a Python implementation of the C4 ID system - a content-addressable identifier system using SHA-512 hashing and Base58 encoding. It provides both a Python library and command-line interface for generating C4 identifiers from files, streams, and raw bytes.

## Development Environment Setup

This project supports both Nix flakes and traditional Python development environments:

### Nix Flake (Recommended)

The project includes a comprehensive Nix flake for reproducible development:

```bash
# Enter development environment with all tools (automatically sets up venv and activates it)
nix develop

# Or use direnv for automatic activation
direnv allow  # (if .envrc exists)

# Build the package
nix build

# Run the package directly
nix run . -- --help

# In the development shell, c4py command is available directly:
c4py --help
echo "test" | c4py
```

### Traditional Python Setup

```bash
# Install dependencies and create virtual environment
uv sync --dev

# Activate virtual environment (if needed)
. .venv/bin/activate
```

## Common Development Commands

### Just Task Runner (Nix Environment)

The Nix environment includes a `justfile` with convenient development tasks:

```bash
# Development workflow
just install      # Install dependencies with UV
just test         # Run tests with coverage
just test-fast    # Run tests without coverage
just lint         # Check code with ruff
just format       # Format code with ruff
just fix          # Auto-fix issues and format
just typecheck    # Type check with ty
just check        # Run all quality checks (lint + typecheck + test)

# Package management
just build        # Build package with Nix
just clean        # Clean build artifacts
just run <args>   # Run c4py CLI with arguments

# Environment
just shell        # Enter nix develop shell
just             # Show all available commands
```

### Direct Commands

#### Testing
```bash
# Run all tests with coverage using uv
uv run pytest --cov=c4py --cov-report=xml

# Run tests without coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_id.py

# Run specific test function
uv run pytest tests/test_id.py::test_id_parsing
```

#### Code Quality and Linting
```bash
# Run ruff linting (check only)
uv run ruff check .

# Run ruff with auto-fix
uv run ruff check . --fix

# Format code with ruff
uv run ruff format .

# Run ty type checking
uv run ty check .

# Run all style checks (legacy tools also available)
uv run black .
uv run isort .
```

#### Package Management
```bash
# Install new dependency
uv add <package-name>

# Install new development dependency  
uv add --dev <package-name>

# Update all dependencies
uv sync --upgrade
```

#### Nix-specific Commands
```bash
# Check flake configuration
nix flake check

# Build package
nix build

# Run package directly
nix run . -- <args>

# Update flake inputs
nix flake update
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

- **Python Versions**: Supports 3.8-3.12 (Nix flake uses 3.12)
- **Build System**: Uses `hatchling` backend
- **Package Manager**: `uv` for fast dependency resolution
- **Development Environment**: Nix flake with reproducible environment
- **Task Runner**: Just for common development tasks
- **CI/CD**: GitHub Actions with Python matrix testing and codecov integration
- **Code Style**: Ruff for linting and formatting (88 char line length)
- **Type Checking**: ty with strict configuration requiring type annotations

### Nix Flake Features

The `flake.nix` provides:
- **Reproducible Environment**: Python 3.12 with all dependencies
- **Development Shell**: Automatic venv setup with UV
- **Quality Checks**: Automated tests, linting, and type checking via `nix flake check`
- **Package Build**: Complete package build with `nix build`
- **CLI Access**: Direct CLI execution with `nix run`
- **Development Tools**: Git, GitHub CLI, Just task runner, and direnv support