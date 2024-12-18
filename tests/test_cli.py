# tests/test_cli.py
import pytest
from click.testing import CliRunner
import os
from c4py.cli import main

@pytest.fixture
def runner():
    """Fixture for invoking command-line interfaces"""
    return CliRunner()

def test_cli_version(runner):
    """Test version flag output"""
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    assert 'c4py' in result.output
    assert '0.1.0' in result.output

def test_cli_help(runner):
    """Test help output"""
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output

def test_cli_file_identification(runner, temp_file):
    """Test CLI file identification"""
    path, _ = temp_file
    
    # Test basic output (just ID)
    result = runner.invoke(main, [path])
    assert result.exit_code == 0
    output = result.output.strip()
    assert len(output) == 90, f"Expected 90-char ID, got: {len(output)} chars"
    assert output.startswith('c4'), f"ID should start with 'c4', got: {output[:2]}"
    
    # Test verbose output
    result_verbose = runner.invoke(main, ['--verbose', path])
    assert result_verbose.exit_code == 0
    output_verbose = result_verbose.output.strip()
    parts = output_verbose.split(': ')
    assert len(parts) == 2, f"Expected ID: path format, got: {output_verbose}"
    assert parts[0] == output, "IDs should match between verbose and non-verbose output"

def test_cli_recursive(runner, temp_dir):
    """Test CLI recursive directory scanning"""
    # Create some test files
    for i in range(3):
        path = os.path.join(temp_dir, f'test{i}.txt')
        with open(path, 'w') as f:
            f.write(f'Content {i}')
    
    # Test basic recursive output
    result = runner.invoke(main, ['-R', temp_dir])
    assert result.exit_code == 0
    output_lines = result.output.strip().split('\n')
    assert len(output_lines) == 3, f"Expected 3 lines of output, got: {result.output}"
    
    # Each line should be just a C4 ID
    for line in output_lines:
        assert len(line) == 90, f"Expected 90-char ID, got: {len(line)} chars"
        assert line.startswith('c4'), f"ID should start with 'c4', got: {line[:2]}"
    
    # Test verbose recursive output
    result_verbose = runner.invoke(main, ['-R', '--verbose', temp_dir])
    assert result_verbose.exit_code == 0
    output_lines_verbose = result_verbose.output.strip().split('\n')
    assert len(output_lines_verbose) == 3

def test_path_first_format(runner, temp_file):
    """Test path-first formatting option"""
    path, _ = temp_file
    result = runner.invoke(main, ['--verbose', '--path-first', path])
    assert result.exit_code == 0
    output = result.output.strip()
    assert output.startswith(path), "Output should start with path when using --path-first"