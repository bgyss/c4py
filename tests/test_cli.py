# tests/test_cli.py
import pytest
from click.testing import CliRunner
import os
from c4py.cli import main
from c4py import NIL_ID

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

def test_cli_file_not_found(runner):
    """Test handling of non-existent files"""
    result = runner.invoke(main, ['nonexistent_file.txt'])
    assert result.exit_code != 0
    assert "does not exist" in result.output
    assert "nonexistent_file.txt" in result.output

def test_cli_stdin_handling(runner):
    """Test handling of stdin input"""
    # Test with stdin data
    result = runner.invoke(main, input='test data')
    assert result.exit_code == 0
    assert len(result.output.strip()) == 90  # Should be a valid C4 ID

def test_cli_directory_errors(runner, temp_dir):
    """Test directory processing error handling"""
    # Create a directory with insufficient permissions
    restricted_dir = os.path.join(temp_dir, 'restricted')
    os.mkdir(restricted_dir)
    os.chmod(restricted_dir, 0o000)  # Remove all permissions
    
    try:
        result = runner.invoke(main, ['-R', restricted_dir])
        assert result.exit_code != 0
        assert "not readable" in result.output
    finally:
        os.chmod(restricted_dir, 0o755)  # Restore permissions for cleanup

def test_cli_metadata_output(runner, temp_file):
    """Test metadata output functionality"""
    path, _ = temp_file
    result = runner.invoke(main, ['--metadata', '--verbose', path])
    assert result.exit_code == 0
    # Get file size
    file_size = os.path.getsize(path)
    # Check for file size in output
    assert str(file_size) in result.output

def test_cli_stdin_with_errors(runner):
    """Test CLI stdin handling with error conditions"""
    # Test with empty input
    result = runner.invoke(main, input='')
    assert result.exit_code == 0
    assert result.output.strip() == str(NIL_ID)
    
    # Test with binary input
    result = runner.invoke(main, input=bytes([0xFF] * 100))
    assert result.exit_code == 0
    assert len(result.output.strip()) == 90

def test_cli_metadata_formatting(runner, temp_file):
    """Test different metadata formatting options"""
    path, _ = temp_file
    
    # Test path-first formatting with metadata
    result = runner.invoke(main, ['--metadata', '--path-first', path])
    assert result.exit_code == 0
    assert path in result.output.split('\n')[0]
    
    # Test ID-first formatting with metadata
    result = runner.invoke(main, ['--metadata', path])
    assert result.exit_code == 0
    assert 'ID:' in result.output

def test_cli_recursive_depth_limit(runner, temp_dir):
    """Test recursive processing with depth limit"""
    # Create nested directory structure
    subdir = os.path.join(temp_dir, 'subdir')
    subsubdir = os.path.join(subdir, 'subsubdir')
    os.makedirs(subsubdir)
    
    # Create files at different depths
    with open(os.path.join(temp_dir, 'root.txt'), 'w') as f:
        f.write('root')
    with open(os.path.join(subdir, 'level1.txt'), 'w') as f:
        f.write('level1')
    with open(os.path.join(subsubdir, 'level2.txt'), 'w') as f:
        f.write('level2')
        
    # Test with depth=1
    result = runner.invoke(main, ['-R', '--depth', '1', temp_dir])
    assert result.exit_code == 0
    assert len(result.output.strip().split('\n')) == 2  # root + level1 only

def test_cli_metadata_error(runner, temp_dir):
    """Test metadata handling with inaccessible files"""
    file_path = os.path.join(temp_dir, 'test.txt')
    with open(file_path, 'w') as f:
        f.write('test')
    os.chmod(file_path, 0o000)
    
    try:
        result = runner.invoke(main, ['--metadata', file_path])
        assert result.exit_code != 0
    finally:
        os.chmod(file_path, 0o644)

def test_cli_non_terminal_input(runner):
    """Test CLI with non-terminal input"""
    with runner.isolated_filesystem():
        result = runner.invoke(main, input='test data\n')
        assert result.exit_code == 0
        assert len(result.output.strip()) == 90

def test_cli_directory_processing_error(runner, temp_dir):
    """Test directory processing with unreadable files"""
    # Create a file with no read permissions
    test_file = os.path.join(temp_dir, 'unreadable.txt')
    with open(test_file, 'w') as f:
        f.write('test content')
    
    # Create a readable file to ensure directory is processed
    readable_file = os.path.join(temp_dir, 'readable.txt')
    with open(readable_file, 'w') as f:
        f.write('readable content')
        
    os.chmod(test_file, 0o000)
    
    try:
        result = runner.invoke(main, ['-R', temp_dir])
        assert result.exit_code == 0  # Process should continue despite errors
        output_lines = result.output.strip().split('\n')
        assert len([line for line in output_lines if line.startswith('c4')]) == 1  # One valid ID
        assert any('Permission denied' in line for line in output_lines)  # Error message present
    finally:
        os.chmod(test_file, 0o644)

def test_cli_with_binary_input(runner):
    """Test CLI with binary input"""
    result = runner.invoke(main, input=b'\x00\xFF\x80')
    assert result.exit_code == 0
    assert len(result.output.strip()) == 90

def test_cli_multiple_files_error(runner, temp_dir):
    """Test handling multiple files with some errors"""
    # Create good file
    good_file = os.path.join(temp_dir, 'good.txt')
    with open(good_file, 'w') as f:
        f.write('good content')
    
    # Try to process good file and nonexistent file
    result = runner.invoke(main, [good_file, 'nonexistent.txt'])
    assert 'does not exist' in result.output
    assert len([line for line in result.output.strip().split('\n') if line.startswith('c4')]) == 1
