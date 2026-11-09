"""Arithmp: Command-line interface for the Arithmp package."""

import sys
from pathlib import Path
from typing import cast

import click
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent

from .parser import Parser, ParserException


@click.command()
@click.argument("filepath", type=click.Path(exists=True, path_type=Path))
def mainnn(filepath: Path) -> None:
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


def _interactive() -> None:

    # interactive  mode if nothing is specified
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.history import FileHistory

    parser = Parser(argv=(sys.argv[0],))
    session = PromptSession(
        history=FileHistory(Path.home().joinpath(".arithmp_history")),
        completer=WordCompleter(lambda: list(parser.globals.keys())),
    )

    kb = KeyBindings()

    @kb.add("enter")
    def _(event: KeyPressEvent) -> None:
        event.current_buffer.validate_and_handle()

    @kb.add("escape", "enter")
    def _(event: KeyPressEvent) -> None:
        event.current_buffer.insert_text("\n")

    while True:
        expression = cast(
            str,
            session.prompt(
                ">>> ", multiline=True, prompt_continuation="... ", key_bindings=kb
            ),
        ).strip()
        if not expression:
            continue
        try:
            result = parser.parse(None, expression)
            if result is not None:
                click.echo(result)
        except SystemExit:
            break
        except ParserException as e:
            click.echo(
                f"Error at line {e.context.line} column {e.context.column} '{e.context.source}': {e}'"
            )


@click.command()
@click.option("-c", type=str, required=False)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def main(c: str, args: str) -> None:

    return _interactive()


if __name__ == "__main__":
    main()
