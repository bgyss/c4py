# c4py

![Tests](https://github.com/SphereStudios/c4py/actions/workflows/python-tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/SphereStudios/c4py/graph/badge.svg?token=VJBE7X97JW)](https://codecov.io/gh/SphereStudios/c4py)

A Python implementation of the C4 ID system, providing both a library and command-line interface for generating and working with C4 identifiers.

## Features

- Generate C4 IDs from files, streams, and bytes
- Command-line interface for file and directory processing
- Support for recursive directory scanning
- Rich metadata output options
- Pure Python implementation with no external dependencies
- Comprehensive test coverage

## Installation

```bash
pip install c4py
```

## Python Library Usage

### Module Basic Usage

```python
from c4py import identify, ID, Encoder

# Generate ID from a file
with open('myfile.txt', 'rb') as f:
    id_obj = identify(f)
    print(id_obj)  # Prints the C4 ID

# Generate ID from bytes
encoder = Encoder()
encoder.write(b"Hello, World!")
id_obj = encoder.id()
print(id_obj)

# Parse existing C4 ID
id_obj = ID.parse("c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1")
```

### Working with Digests

```python
from c4py import Digest

# Create a digest from bytes
digest1 = Digest(bytes([1] * 64))
digest2 = Digest(bytes([2] * 64))

# Sum digests
combined = digest1.sum(digest2)

# Convert digest to ID
id_obj = digest1.id()
```

### Stream Processing

```python
from c4py import Encoder
import io

# Process a stream in chunks
encoder = Encoder()
stream = io.BytesIO(b"Large data...")

while True:
    chunk = stream.read(8192)  # Read in 8KB chunks
    if not chunk:
        break
    encoder.write(chunk)

id_obj = encoder.id()
```

## Command-Line Interface

### CLI Basic Usage

```bash
# Generate ID for a single file
c4py myfile.txt

# Generate IDs for multiple files
c4py file1.txt file2.txt

# Process stdin
echo "Hello, World!" | c4py
```

### Directory Processing

```bash
# Recursively process a directory
c4py -R /path/to/directory

# Limit recursion depth
c4py -R -d 2 /path/to/directory

# Follow symbolic links
c4py -R -L /path/to/directory
```

### Output Formatting

```bash
# Include file paths in output
c4py -V myfile.txt

# Show paths before IDs
c4py -V -p myfile.txt

# Include file metadata
c4py -m myfile.txt

# Use absolute paths
c4py -a myfile.txt
```

### Sample Output

Basic ID output:

```bash
$ c4py document.txt
c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1
```

Verbose output:

```bash
$ c4py -V document.txt
c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1: document.txt
```

Metadata output:

```bash
$ c4py -m document.txt
ID: c43zYcLni5LF9rR4Lg4B8h3Jp8SBwjcnyyeh4bc6gTPHndKuKdjUWx1kJPYhZxYt3zV6tQXpDs2shPsPYjgG81wZM1
Path: document.txt
Size: 1234 bytes
Modified: 2024-03-23T14:30:00
Created: 2024-03-23T14:29:55
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/c4py.git
cd c4py
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Style

The project uses:

- black for code formatting
- isort for import sorting
- mypy for type checking
- ruff for linting

Run all style checks:

```bash
black .
isort .
mypy .
ruff .
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -am 'Add awesome feature'`)
4. Push to the branch (`git push origin feature/awesome-feature`)
5. Create a Pull Request
