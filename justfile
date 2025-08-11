# c4py development tasks

# Install development dependencies
install:
    uv sync --dev

# Run tests
test:
    pytest --cov=c4py --cov-report=xml

# Run tests without coverage
test-fast:
    pytest

# Run specific test file
test-file file:
    pytest {{file}}

# Check code with ruff
lint:
    ruff check .

# Format code with ruff
format:
    ruff format .

# Fix code issues automatically
fix:
    ruff check . --fix
    ruff format .

# Type check with mypy
typecheck:
    mypy .

# Run all quality checks
check: lint typecheck test

# Clean build artifacts
clean:
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info
    rm -rf .coverage
    rm -rf htmlcov/
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -delete

# Build the package
build:
    nix build

# Run the CLI tool
run *args:
    c4py {{args}}

# Enter development shell
shell:
    nix develop

# Show available commands
default:
    @just --list