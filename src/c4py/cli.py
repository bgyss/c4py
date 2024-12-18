# src/c4py/cli.py
import os
import sys
from typing import Optional, List
import click
from . import identify, ID

def identify_file(path: str) -> Optional[ID]:
    """Identify a single file"""
    try:
        with open(path, 'rb') as f:
            return identify(f)
    except Exception as e:
        click.echo(f"Error processing {path}: {e}", err=True)
        return None

def process_directory(path: str, follow_links: bool, depth: int, absolute: bool) -> List[tuple[str, ID]]:
    """Process a directory recursively"""
    results = []
    
    try:
        for root, dirs, files in os.walk(path, followlinks=follow_links):
            # Check depth limit
            if depth > 0:
                rel_depth = len(os.path.relpath(root, path).split(os.sep))
                if rel_depth > depth:
                    continue
            
            for file in files:
                file_path = os.path.join(root, file)
                if absolute:
                    file_path = os.path.abspath(file_path)
                
                file_id = identify_file(file_path)
                if file_id:
                    results.append((file_path, file_id))
    except Exception as e:
        click.echo(f"Error processing directory {path}: {e}", err=True)
    
    return results

def format_output(path: str, id_obj: ID, verbose: bool, path_first: bool) -> str:
    """Format the output according to CLI options"""
    if not verbose:
        return str(id_obj)
    
    if path_first:
        return f"{path}: {str(id_obj)}"
    return f"{str(id_obj)}: {path}"

@click.command()
@click.version_option(version='0.1.0', prog_name='c4py')
@click.option('--recursive', '-R', is_flag=True, help='Recursively identify all files')
@click.option('--absolute', '-a', is_flag=True, help='Output absolute paths')
@click.option('--links', '-L', is_flag=True, help='Follow symbolic links')
@click.option('--depth', '-d', type=int, default=0, help='Directory depth limit')
@click.option('--metadata', '-m', is_flag=True, help='Include metadata')
@click.option('--verbose', '-V', is_flag=True, help='Include filenames in output')
@click.option('--path-first', '-p', is_flag=True, help='Show path before ID in output')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(recursive: bool, absolute: bool, links: bool, depth: int,
         metadata: bool, verbose: bool, path_first: bool, files: tuple[str]) -> None:
    """Generate C4 IDs for files and data.
    
    If no files are provided, reads from standard input.
    """
    if not files:
        if not sys.stdin.isatty():
            id_obj = identify(sys.stdin.buffer)
            if id_obj:
                click.echo(str(id_obj))
        else:
            ctx = click.get_current_context()
            click.echo(ctx.get_help())
        return

    for path in files:
        if os.path.isdir(path) and recursive:
            results = process_directory(path, links, depth, absolute)
            for file_path, file_id in results:
                click.echo(format_output(file_path, file_id, verbose, path_first))
        else:
            file_id = identify_file(path)
            if file_id:
                click.echo(format_output(path, file_id, verbose, path_first))

if __name__ == '__main__':
    main()