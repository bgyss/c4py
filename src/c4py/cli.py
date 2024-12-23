# src/c4py/cli.py
import os
import datetime
import sys
from typing import Optional, List
import click
from . import identify, ID


def get_file_metadata(path: str) -> dict:
    """Get metadata for a file"""
    stat = os.stat(path)
    return {
        "size": stat.st_size,
        "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "mode": stat.st_mode,
    }


def format_output(
    path: str, id_obj: ID, verbose: bool, path_first: bool, metadata: bool = False
) -> str:
    """Format the output according to CLI options"""
    if not verbose and not metadata:
        return str(id_obj)

    parts = []

    if metadata:
        meta = get_file_metadata(path)
        if path_first:
            parts.extend(
                [
                    path,
                    f"ID: {str(id_obj)}",
                    f"Size: {meta['size']} bytes",
                    f"Modified: {meta['modified']}",
                    f"Created: {meta['created']}",
                ]
            )
        else:
            parts.extend(
                [
                    f"ID: {str(id_obj)}",
                    f"Path: {path}",
                    f"Size: {meta['size']} bytes",
                    f"Modified: {meta['modified']}",
                    f"Created: {meta['created']}",
                ]
            )
        return "\n".join(parts)

    # Regular verbose output without metadata
    if path_first:
        return f"{path}: {str(id_obj)}"
    return f"{str(id_obj)}: {path}"


def identify_file(path: str) -> Optional[ID]:
    """Identify a single file"""
    try:
        with open(path, "rb") as f:
            return identify(f)
    except Exception as e:
        click.echo(f"Error processing {path}: {e}", err=True)
        return None


def process_directory(
    path: str, follow_links: bool, depth: int, absolute: bool
) -> List[tuple[str, ID]]:
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


@click.command()
@click.version_option(version="0.1.0", prog_name="c4py")
@click.option("--recursive", "-R", is_flag=True, help="Recursively identify all files")
@click.option("--absolute", "-a", is_flag=True, help="Output absolute paths")
@click.option("--links", "-L", is_flag=True, help="Follow symbolic links")
@click.option("--depth", "-d", type=int, default=0, help="Directory depth limit")
@click.option("--metadata", "-m", is_flag=True, help="Include metadata")
@click.option("--verbose", "-V", is_flag=True, help="Include filenames in output")
@click.option("--path-first", "-p", is_flag=True, help="Show path before ID in output")
@click.argument(
    "files", nargs=-1, type=click.Path(exists=False)
)  # Changed to exists=False to handle our own errors
def main(
    recursive: bool,
    absolute: bool,
    links: bool,
    depth: int,
    metadata: bool,
    verbose: bool,
    path_first: bool,
    files: tuple[str],
) -> None:
    """Generate C4 IDs for files and data."""
    # Handle stdin when no files provided
    if not files:
        if not sys.stdin.isatty():
            try:
                id_obj = identify(sys.stdin.buffer)
                if id_obj:
                    click.echo(str(id_obj))
            except Exception as e:
                click.echo(f"Error processing stdin: {e}", err=True)
                sys.exit(1)
        return

    # Process each file
    exit_status = 0
    for path in files:
        if not os.path.exists(path):
            click.echo(f"Error: Path '{path}' does not exist.", err=True)
            exit_status = 1
            continue

        try:
            if os.path.isdir(path) and recursive:
                results = process_directory(path, links, depth, absolute)
                for file_path, file_id in results:
                    click.echo(
                        format_output(file_path, file_id, verbose, path_first, metadata)
                    )
            else:
                file_id = identify_file(path)
                if file_id:
                    click.echo(
                        format_output(path, file_id, verbose, path_first, metadata)
                    )
        except Exception as e:
            click.echo(f"Error processing {path}: {e}", err=True)
            exit_status = 1

    if exit_status != 0:
        sys.exit(exit_status)
