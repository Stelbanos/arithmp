"""Arithmp: Command-line interface for the Arithmp package."""

from pathlib import Path

import click

from .parser import Parser, ParserException


@click.command()
@click.argument("filepath", type=click.Path(exists=True, path_type=Path))
def mainn(filepath: Path) -> None:
    """
    Main entry point for the Arithmp command-line interface.
    """
    parser = Parser()
    try:
        if (result := parser.parse(filepath, filepath.read_text())) is not None:
            click.echo(result)
    except ParserException as e:
        click.echo(
            f"Error in script '{filepath}' at line {e.context.line} column {e.context.column} '{e.context.source}': {e}'"
        )


@click.command()
@click.option("-c", required=False, nargs=1)
@click.argument("arg", type=click.UNPROCESSED, nargs=-1)
def main(c: str, arg: str) -> None:
    if c is not None:
        parser = Parser()
        if (result := parser.parse(None, c)) is not None:
            click.echo(result)
    else:
        print("error")


if __name__ == "__main__":
    main()
